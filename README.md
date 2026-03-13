# article-ingest

OpenClaw skill for ingesting and summarizing long-form articles from multiple sources.

## What it supports

- WeChat `mp.weixin.qq.com` articles
- Generic web URLs
- Local `md` / `txt` / `html` files
- Pasted raw text / stdin
- Feishu docs via `feishu-doc` integration

## Default output

- 3-line summary
- Core viewpoints
- Judgment / worth-reading note
- Whether it is worth remembering
- Topic tags

## Repository layout

- `SKILL.md` — skill entry and usage guidance
- `scripts/article_ingest.py` — ingestion script
- `references/output-templates.md` — output templates
- `dist/article-ingest.skill` — packaged skill artifact

## Notes

This repository contains the skill itself as a standalone export from a larger OpenClaw workspace.
