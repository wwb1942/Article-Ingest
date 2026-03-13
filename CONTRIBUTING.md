# Contributing

Thanks for taking a look at `Article-Ingest`.

## Scope

This repository is currently maintained as a focused standalone export of an OpenClaw skill. The main contribution areas are:

- extraction robustness
- documentation improvements
- output template refinements
- packaging / release polish

## Before opening a PR

1. Keep the technical skill slug as `article-ingest` unless there is a deliberate migration plan.
2. Prefer minimal, reviewable changes.
3. If you change script behavior, include a clear usage example or note in the docs.
4. Do not commit secrets, tokens, or private datasets.

## Development notes

Useful checks:

```bash
python3 scripts/article_ingest.py --help
python3 -m py_compile scripts/article_ingest.py
```

## Pull requests

Please include:

- what changed
- why it changed
- how you verified it
- any compatibility risk or migration note

## Issues

If you file an issue, include the input type when possible:

- WeChat URL
- generic web URL
- local file
- pasted text / stdin
- Feishu doc workflow
