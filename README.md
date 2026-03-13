# Article-Ingest

An OpenClaw skill for extracting, cleaning, and summarizing long-form articles from multiple input sources.

It is designed for the common workflow of “send me an article, give me the useful bits, and optionally turn it into a reusable knowledge note.”

## What it supports

- WeChat `mp.weixin.qq.com` article links
- Generic web URLs
- Local `md` / `txt` / `html` files
- Pasted raw text / stdin
- Feishu docs via `feishu-doc` workflow integration

## Default output

Unless a custom format is requested, the skill is designed to produce:

1. 3-line summary
2. Core points
3. Judgment / worth-reading note
4. Whether it is worth remembering
5. Topic tags

## Quick examples

### Extract from a WeChat article

```bash
python3 scripts/article_ingest.py 'https://mp.weixin.qq.com/s/...' --format json
```

### Extract from a local markdown file

```bash
python3 scripts/article_ingest.py '/path/to/article.md' --format json
```

### Extract from pasted text / stdin

```bash
cat article.txt | python3 scripts/article_ingest.py --stdin --title 'Temporary title' --format json
```

### Show CLI help

```bash
python3 scripts/article_ingest.py --help
```

## Output formats

The extraction script supports:

- `json`
- `markdown`
- `text`

## Repository layout

- `SKILL.md` — skill contract, workflow guidance, and guardrails
- `scripts/article_ingest.py` — extraction entrypoint
- `references/output-templates.md` — digest and knowledge-card templates
- `dist/article-ingest.skill` — packaged skill artifact

## Release artifact

If you just want the packaged skill file, download it from the GitHub Releases page.

## Notes

- The repository display name is `Article-Ingest`, but the technical skill slug remains `article-ingest`.
- Keeping the slug lowercase avoids breaking skill references, file paths, and packaged artifact naming.
- This repository is a standalone export of the skill from a larger OpenClaw workspace.

## License

MIT
