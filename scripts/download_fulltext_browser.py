#!/usr/bin/env python3
"""Interactive browser-based fallback for hard-to-scrape publishers (Elsevier, ACS).

Why this exists: ScienceDirect and ACS use JS-based bot detection that even
real Chrome via Playwright can't bypass without user interaction. This script
runs a *visible* Chrome window via undetected-chromedriver and:

  1. Navigates to each pending Elsevier top pick
  2. If a "Press & Hold" / captcha challenge appears, prompts you to solve it
     manually in the open window, then continue
  3. Clicks the View PDF link → Chrome downloads it natively (with full session
     auth from the campus IP)
  4. Watches the downloads folder for the new PDF and moves it into
     papers/fulltext/<id>.pdf

Run when you have a couple of minutes to babysit captchas. Not part of /daily
(would block the midnight automation on input()). Skips papers already cached.

Usage:
  python scripts/download_fulltext_browser.py papers/raw/2026-04-27.filtered.json
  python scripts/download_fulltext_browser.py papers/raw/2026-04-27.filtered.json --publishers 10.1016 10.1021
  python scripts/download_fulltext_browser.py papers/raw/2026-04-27.filtered.json --max 5
"""
import argparse
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# undetected-chromedriver's __del__ runs during interpreter teardown on Windows
# and tries to call quit() on a process whose handle is already gone, raising
# `OSError: [WinError 6] The handle is invalid`. The error is harmless (work
# has finished) but noisy. Wrap __del__ to swallow it.
_original_uc_del = uc.Chrome.__del__
def _safe_uc_del(self):
    try:
        _original_uc_del(self)
    except (OSError, AttributeError, Exception):
        pass
uc.Chrome.__del__ = _safe_uc_del

ROOT = Path(__file__).resolve().parent.parent
FT_DIR = ROOT / "papers" / "fulltext"
DL_DIR = ROOT / ".browser-downloads"

# Default publishers handled by this script. DOI-prefix → publisher label.
PUBLISHER_MAP = {
    "10.1016/": "elsevier",
    "10.1021/": "acs",
}


def detect_chrome_major_version():
    """Find the major version of the installed Chrome by listing Application/<version>/.

    undetected-chromedriver's auto-download fetches the latest ChromeDriver,
    which can run ahead of the installed Chrome (e.g. ChromeDriver 148 vs Chrome
    147). Pinning `version_main` makes uc fetch the matching driver.
    """
    candidates = [
        r"C:\Program Files\Google\Chrome\Application",
        r"C:\Program Files (x86)\Google\Chrome\Application",
        os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application"),
    ]
    for app_dir in candidates:
        if not os.path.isdir(app_dir):
            continue
        versions = []
        for name in os.listdir(app_dir):
            if re.match(r"^\d+\.\d+\.\d+\.\d+$", name):
                versions.append(name)
        if versions:
            versions.sort(key=lambda v: tuple(int(x) for x in v.split(".")), reverse=True)
            return int(versions[0].split(".")[0])
    return None


def setup_driver(download_folder: Path):
    """Real Chrome via undetected-chromedriver, visible window, downloads
    routed to a known folder, PDFs forced to download (not preview).

    Auto-detects the installed Chrome major version and pins ChromeDriver to
    match — otherwise uc may pull a newer ChromeDriver than the user's Chrome.
    """
    download_folder = download_folder.resolve()
    download_folder.mkdir(parents=True, exist_ok=True)

    options = uc.ChromeOptions()
    prefs = {
        "download.default_directory": str(download_folder),
        "plugins.always_open_pdf_externally": True,
        "download.prompt_for_download": False,
        "directory_upgrade": True,
        "safebrowsing.enabled": True,
    }
    options.add_experimental_option("prefs", prefs)

    chrome_major = detect_chrome_major_version()
    kwargs = {"options": options, "use_subprocess": True}
    if chrome_major:
        kwargs["version_main"] = chrome_major
        print(f"  (using Chrome major version {chrome_major})")

    driver = uc.Chrome(**kwargs)
    driver.execute_cdp_cmd("Page.setDownloadBehavior", {
        "behavior": "allow",
        "downloadPath": str(download_folder),
    })
    return driver


def detect_bot_block(driver) -> bool:
    """Return True if ScienceDirect's bot block / captcha page is visible."""
    try:
        body = driver.find_element(By.TAG_NAME, "body").text
    except Exception:
        return False
    markers = (
        "Reference number:",
        "problem providing the content",
        "Press & Hold",
        "verifying you are a human",
        "Pardon Our Interruption",
    )
    return any(m.lower() in body.lower() for m in markers)


def prompt_with_timeout(prompt: str, timeout_seconds: int = 300) -> bool:
    """input() with a timeout. Returns True if user pressed Enter, False if timed out.

    On Windows, signal.SIGALRM isn't available so we use a thread-based timeout.
    """
    import threading
    result = [False]

    def get_input():
        try:
            input(prompt)
            result[0] = True
        except EOFError:
            pass

    t = threading.Thread(target=get_input, daemon=True)
    t.start()
    t.join(timeout=timeout_seconds)
    if t.is_alive():
        print(f"\n  (no input within {timeout_seconds}s — skipping this paper)")
        return False
    return result[0]


def wait_for_new_pdf(download_folder: Path, files_before: set, timeout: int = 60):
    """Poll the download folder for a new .pdf file (not a .crdownload partial).

    Returns the new Path or None on timeout.
    """
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            current = set(os.listdir(download_folder))
        except FileNotFoundError:
            time.sleep(0.5); continue
        new_files = current - files_before
        # Wait for crdownload to finish — only count complete .pdf files.
        complete = [f for f in new_files if f.lower().endswith(".pdf")]
        partial = [f for f in new_files if f.lower().endswith(".crdownload")]
        if complete:
            # Pick the newest, in case multiple
            paths = [download_folder / f for f in complete]
            paths.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            return paths[0]
        if partial:
            # In progress — keep waiting
            time.sleep(1.0)
            continue
        time.sleep(0.5)
    return None


def find_pii(driver) -> str | None:
    """Extract the ScienceDirect PII from the current URL or page metadata."""
    m = re.search(r"/pii/([A-Z0-9]+)", driver.current_url)
    if m:
        return m.group(1)
    return None


def find_view_pdf(driver, pii: str | None):
    """Locate the View PDF anchor and return (element, href) or (None, None).

    Selectors tried in order of robustness:
      1. Anchor with aria-label containing "View PDF" filtered by PII (most stable)
      2. Anchor whose href contains /pdfft (the actual PDF endpoint)
      3. Anchor whose visible text contains "View PDF"
    """
    selectors = []
    if pii:
        selectors.append((By.CSS_SELECTOR, f'a[aria-label*="View PDF"][href*="{pii}"]'))
    selectors.append((By.CSS_SELECTOR, 'a[href*="/pdfft"]'))
    selectors.append((By.XPATH, '//a[.//span[contains(text(),"View PDF")]]'))

    for by, sel in selectors:
        try:
            el = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((by, sel)))
            href = el.get_attribute("href")
            return el, href
        except TimeoutException:
            continue
        except Exception:
            continue
    return None, None


def download_one(driver, paper, publisher: str) -> tuple[bool, str]:
    """Drive the browser to download one paper. Returns (ok, message)."""
    pid = paper["id"]
    doi = (paper.get("doi") or "").replace("https://doi.org/", "")
    if not doi:
        return False, "no DOI"
    dest = FT_DIR / f"{pid}.pdf"
    if dest.exists() and dest.stat().st_size > 10_000:
        return True, "cached"

    files_before = set(os.listdir(DL_DIR))
    try:
        driver.get(f"https://doi.org/{doi}")
    except Exception as e:
        return False, f"navigation: {e}"

    # Allow the page (or block) to render
    time.sleep(4)

    if detect_bot_block(driver):
        print("\n  🛑 Bot block detected on " + driver.current_url)
        print("  → Solve the challenge in the browser window (Press & Hold / captcha).")
        ok = prompt_with_timeout("  → Press ENTER once the article page is visible (5 min timeout): ", 300)
        if not ok:
            return False, "captcha not solved"
        time.sleep(2)

    pii = find_pii(driver)
    if not pii and publisher == "elsevier":
        return False, "no ScienceDirect PII (paper may not be on ScienceDirect)"

    el, href = find_view_pdf(driver, pii)
    if el is None:
        return False, "View PDF link not found"

    # Capture href before clicking — clicking opens target=_blank in a new tab
    # which sometimes loses the download. Having the signed URL ready lets us
    # do a fallback driver.get() if the click doesn't trigger a download.
    try:
        el.click()
    except Exception:
        pass

    new_pdf = wait_for_new_pdf(DL_DIR, files_before, timeout=45)
    if not new_pdf and href:
        # Click didn't produce a download. Navigate the current tab to the
        # signed PDF URL — same browser session, same cookies, the download
        # pref forces it to save rather than render inline.
        print("  (click didn't download; trying direct navigate)")
        try:
            driver.get(href)
        except Exception as e:
            return False, f"direct-navigate: {e}"
        new_pdf = wait_for_new_pdf(DL_DIR, files_before, timeout=60)

    if not new_pdf:
        return False, "download did not appear after click + direct navigate"

    # Verify it's a real PDF
    with open(new_pdf, "rb") as f:
        head = f.read(5)
    if not head.startswith(b"%PDF"):
        new_pdf.unlink(missing_ok=True)
        return False, "downloaded file isn't a PDF"

    FT_DIR.mkdir(parents=True, exist_ok=True)
    shutil.move(str(new_pdf), dest)
    return True, f"{dest.stat().st_size // 1024} KB"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("filtered", help="Path to filtered JSON (output of paper-filterer)")
    p.add_argument("--publishers", nargs="+", default=["10.1016/"],
                   help="DOI prefixes to attempt (default: 10.1016/ Elsevier; add 10.1021/ for ACS)")
    p.add_argument("--max", type=int, default=0, help="Cap how many papers to attempt (0 = no cap)")
    p.add_argument("--all", action="store_true",
                   help="Try every filter-passer (default: top picks only)")
    args = p.parse_args()

    papers = json.loads(Path(args.filtered).read_text(encoding="utf-8-sig"))
    if not args.all:
        papers = [p for p in papers if p.get("top_pick")]

    # Filter to requested publisher prefixes and skip already-cached papers.
    pending = []
    for p in papers:
        doi = (p.get("doi") or "").replace("https://doi.org/", "")
        publisher = None
        for prefix in args.publishers:
            if doi.startswith(prefix):
                publisher = PUBLISHER_MAP.get(prefix, prefix.rstrip("/"))
                break
        if not publisher:
            continue
        cached = (FT_DIR / f"{p['id']}.pdf")
        if cached.exists() and cached.stat().st_size > 10_000:
            continue
        pending.append((p, publisher))

    pending.sort(key=lambda pp: -pp[0].get("score", 0))
    if args.max:
        pending = pending[: args.max]

    if not pending:
        print("Nothing to do — all matching papers already have full text or none match the publisher filter.")
        return

    print(f"\n{len(pending)} paper(s) to attempt. Chrome will open visibly.")
    print("Tip: when a captcha appears, solve it in the window and press Enter here.\n")

    DL_DIR.mkdir(parents=True, exist_ok=True)
    driver = setup_driver(DL_DIR)
    ok = failed = 0
    try:
        for paper, publisher in pending:
            pid = paper["id"]
            title_short = (paper.get("title") or "")[:65]
            print(f"\n[{publisher}] {pid}  {title_short!r}")
            success, msg = download_one(driver, paper, publisher)
            if success:
                ok += 1
                print(f"  ✓ {msg}")
            else:
                failed += 1
                print(f"  ✗ {msg}", file=sys.stderr)
    finally:
        # Quit explicitly, drop the reference, force GC now — keeps the noisy
        # WinError 6 from the uc.Chrome.__del__ finalizer from firing later
        # during interpreter shutdown.
        try:
            driver.quit()
        except Exception:
            pass
        driver = None
        import gc
        gc.collect()

    # Clean up any leftover partial downloads in the staging folder
    for f in DL_DIR.glob("*.crdownload"):
        try:
            f.unlink()
        except Exception:
            pass

    print(f"\nDone. {ok} downloaded, {failed} failed (of {len(pending)} attempted).")
    print(f"Saved to: {FT_DIR.relative_to(ROOT).as_posix()}/")


if __name__ == "__main__":
    main()
