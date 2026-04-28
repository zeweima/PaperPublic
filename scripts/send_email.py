#!/usr/bin/env python3
"""Send a markdown digest via SMTP. Reads SMTP_PASSWORD from env or .env."""
import argparse
import os
import smtplib
import sys
from email.message import EmailMessage
from pathlib import Path

import yaml

try:
    import markdown as md_lib
except ImportError:
    md_lib = None

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config.yaml"


def load_password():
    pw = os.environ.get("SMTP_PASSWORD")
    if pw:
        return pw
    env_file = ROOT / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("SMTP_PASSWORD="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


def main():
    p = argparse.ArgumentParser()
    p.add_argument("digest", help="Path to markdown digest")
    p.add_argument("--subject", required=True)
    args = p.parse_args()

    cfg = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))["email"]
    body_md = Path(args.digest).read_text(encoding="utf-8")
    if md_lib:
        body_html = md_lib.markdown(body_md, extensions=["extra", "sane_lists"])
    else:
        body_html = "<pre>" + body_md.replace("<", "&lt;") + "</pre>"

    pw = load_password()
    if not pw:
        print("ERROR: SMTP_PASSWORD not set (env or .env)", file=sys.stderr)
        sys.exit(1)

    msg = EmailMessage()
    msg["Subject"] = args.subject
    msg["From"] = cfg["from_addr"]
    msg["To"] = ", ".join(cfg["recipients"])
    msg.set_content(body_md)
    msg.add_alternative(body_html, subtype="html")

    with smtplib.SMTP(cfg["smtp_host"], cfg["smtp_port"]) as s:
        s.starttls()
        s.login(cfg["smtp_user"], pw)
        s.send_message(msg)
    print(f"Sent '{args.subject}' to {len(cfg['recipients'])} recipient(s)")


if __name__ == "__main__":
    main()
