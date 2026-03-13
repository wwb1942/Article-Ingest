---
name: article-ingest
description: Ingest and summarize long-form articles from WeChat mp.weixin links, generic web URLs, Feishu docs, pasted text, and local markdown/txt/html files. Use when the user sends an article and wants automatic extraction, cleaning, a 3-line summary, core观点, judgment, topic classification, or archival into a reusable knowledge card.
---

# article-ingest

Turn messy article inputs into structured notes with minimal user effort.

## Quick start

1. Identify the source type.
2. Extract clean text.
3. Produce the default digest.
4. Archive only when the user asks to save, remember, or build a knowledge base entry.

## Source handling

### 1) WeChat or generic web URL

Use `scripts/article_ingest.py`.

Example:

```bash
python3 /root/.openclaw/workspace/skills/article-ingest/scripts/article_ingest.py \
  'https://mp.weixin.qq.com/s/...' --format json
```

Use the returned `title`, `author`, `description`, and `text` fields as the source of truth for summarization.

### 2) Local markdown / txt / html file

Use the same script with a local path.

```bash
python3 /root/.openclaw/workspace/skills/article-ingest/scripts/article_ingest.py \
  '/path/to/article.md' --format json
```

### 3) Pasted raw text

Either summarize directly or pipe the text into the script.

```bash
cat article.txt | python3 /root/.openclaw/workspace/skills/article-ingest/scripts/article_ingest.py \
  --stdin --title 'Temporary title' --format json
```

### 4) Feishu doc link

Activate the `feishu-doc` skill first, read the document, then continue with the same output contract below.

### 5) PDF / DOCX / screenshots

This MVP skill does not bundle a dedicated PDF/DOCX/OCR parser.

- If text is already extractable with available tools, extract first and continue.
- If extraction is poor or incomplete, ask the user for a better source: article link, Feishu doc, txt, markdown, or pasted text.

## Default output contract

Unless the user asks for another format, return:

1. **3-line summary**
2. **Core points**
3. **My judgment**
4. **Worth remembering?**
5. **Topic tags**

Use the templates in `references/output-templates.md` when you want a consistent format.

## Archive mode

Only archive when the user explicitly asks to save, remember, file, collect, or build a knowledge card.

Write a markdown note to:

```text
knowledge/articles/YYYY-MM-DD-slug.md
```

Include:

- title
- source URL or source file
- author / publisher if known
- 3-line summary
- core points
- judgment
- worth remembering
- topic tags
- optional action items

If the article contains a durable lesson that will help future work, also store a short long-term memory entry.

## Recommended workflow

### A. Fast digest

Use this when the user just wants to know what the article says.

1. Extract text.
2. Check whether extraction is complete enough.
3. Return the default output contract.
4. Clearly label any uncertainty caused by incomplete extraction.

### B. Knowledge-card mode

Use this when the user wants reusable notes.

1. Extract text.
2. Return the default digest.
3. Convert the digest into a knowledge card using `references/output-templates.md`.
4. Save it under `knowledge/articles/`.

### C. Comparative mode

Use this when the user sends multiple articles.

1. Extract each source separately.
2. Summarize each article in 2-4 bullets.
3. Compare overlap, disagreement, and unique value.
4. End with a recommendation: what is worth keeping long term.

## Guardrails

- Distinguish **source claims** from **your judgment**.
- If extraction is partial, say so explicitly.
- If a site blocks fetching, report the blockage quickly and ask for an easier source instead of stalling.
- Prefer concise output first; expand only when the user asks.
- When long external fetching stalls, report: `卡点 + 影响 + 选项`.

## Read this reference when needed

- `references/output-templates.md` — digest and knowledge-card templates
