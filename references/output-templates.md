# Output templates for Article-Ingest

Use these templates when the user does not specify a custom format.

## 1) Default digest template

```markdown
**文章主题**
<一句话点明主题>

**3 行摘要**
- <第 1 行>
- <第 2 行>
- <第 3 行>

**核心观点**
1. <观点 1>
2. <观点 2>
3. <观点 3>

**我的判断**
- 值不值得关注：<是/否/部分>
- 原因：<2-4 句>

**值不值得长期记住**
- <值得保留的长期方法论或结论>

**主题标签**
- <AI>
- <Agent>
- <OpenClaw>
- <RAG>
- <Coding>
```

## 2) Knowledge card template

Write to `knowledge/articles/YYYY-MM-DD-slug.md`.

```markdown
# <标题>

- Source: <URL or file>
- Author: <作者 / 公众号 / 发布方>
- Ingested at: <YYYY-MM-DD>
- Tags: <tag1>, <tag2>, <tag3>

## 3-line summary
- <line 1>
- <line 2>
- <line 3>

## Core points
1. <point 1>
2. <point 2>
3. <point 3>

## Judgment
- <why it matters>
- <what is still weak or uncertain>

## Worth remembering
- <durable lesson>

## Optional action items
- <action 1>
- <action 2>
```

## 3) Comparative digest template

```markdown
# Multi-article comparison

## Shared themes
- <theme>
- <theme>

## Differences
- <difference>
- <difference>

## Unique value by article
### Article A
- <value>

### Article B
- <value>

## Recommendation
- <what to keep long term>
```

## Tagging heuristics

Prefer a small, stable tag set.

- `AI` — general model, product, research, ecosystem
- `Agent` — orchestration, tool use, autonomy, workflow
- `OpenClaw` — OpenClaw product, skills, gateway, plugins, security, ecosystem
- `RAG` — retrieval, parsing, indexing, embeddings, memory
- `Coding` — AI coding, IDEs, code review, debugging, software delivery
- `Infra` — deployment, reliability, scaling, systems architecture
- `Security` — privacy, exposure, auth, secrets, attack surface

## What counts as worth remembering

Keep only durable points such as:

- reusable architecture patterns
- evaluation heuristics
- security lessons
- product positioning insights
- engineering trade-off rules

Avoid storing pure news facts unless they materially change future decisions.
