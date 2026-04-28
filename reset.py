# import shutil, json, pathlib
# root = pathlib.Path('papers')
# for d in ['raw', 'notes', 'fulltext', 'daily', 'weekly', 'monthly']:
#     shutil.rmtree(root / d, ignore_errors=True)
# (root / 'runs.jsonl').unlink(missing_ok=True)
# state = {'last_daily': None, 'last_weekly': None, 'last_monthly': None,
#          'seen_ids': [], 'seen_dois': []}
# (root / 'state.json').write_text(json.dumps(state, indent=2))
# print('reset done')