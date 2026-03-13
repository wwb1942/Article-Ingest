#!/usr/bin/env python3
"""Extract article text and metadata from URLs, local files, or stdin.

MVP features:
- WeChat mp.weixin article extraction
- Generic HTML extraction
- Local .txt/.md/.html ingestion
- stdin/raw text ingestion
- JSON, markdown, or plain-text output
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, asdict
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import List, Optional
from urllib.parse import urlparse

import requests

USER_AGENT = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.40"
)
TIMEOUT = 20


@dataclass
class ExtractionResult:
    source_type: str
    source: str
    title: str = ""
    author: str = ""
    description: str = ""
    text: str = ""
    extraction_method: str = ""
    warnings: List[str] | None = None
    char_count: int = 0
    line_count: int = 0

    def finalize(self) -> "ExtractionResult":
        self.text = normalize_text(self.text)
        self.char_count = len(self.text)
        self.line_count = len([ln for ln in self.text.splitlines() if ln.strip()])
        self.warnings = self.warnings or []
        return self


class BlockHTMLToText(HTMLParser):
    BLOCK_TAGS = {
        "article",
        "aside",
        "blockquote",
        "br",
        "dd",
        "div",
        "dl",
        "dt",
        "figcaption",
        "footer",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "header",
        "hr",
        "li",
        "main",
        "nav",
        "ol",
        "p",
        "pre",
        "section",
        "table",
        "td",
        "th",
        "tr",
        "ul",
    }

    def __init__(self, capture_root: Optional[tuple[str, str, str]] = None):
        super().__init__()
        self.capture_root = capture_root
        self.capture = capture_root is None
        self.depth = 0
        self.skip_stack: List[str] = []
        self.parts: List[str] = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if self.capture_root and not self.capture:
            root_tag, key, value = self.capture_root
            if tag == root_tag and attrs_dict.get(key) == value:
                self.capture = True
                self.depth = 1
                return
        if not self.capture:
            return
        if tag in {"script", "style", "noscript", "svg"}:
            self.skip_stack.append(tag)
            return
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")
        if self.capture_root and tag == self.capture_root[0]:
            self.depth += 1

    def handle_endtag(self, tag):
        if not self.capture:
            return
        if self.skip_stack and tag == self.skip_stack[-1]:
            self.skip_stack.pop()
            return
        if tag in self.BLOCK_TAGS:
            self.parts.append("\n")
        if self.capture_root and tag == self.capture_root[0]:
            self.depth -= 1
            if self.depth == 0:
                self.capture = False

    def handle_data(self, data):
        if not self.capture or self.skip_stack:
            return
        cleaned = data.strip()
        if cleaned:
            self.parts.append(cleaned)

    def get_text(self) -> str:
        return "".join(self.parts)


def normalize_text(text: str) -> str:
    text = unescape(text or "")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    lines = []
    seen = None
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            if lines and lines[-1] != "":
                lines.append("")
            continue
        if line == seen:
            continue
        lines.append(line)
        seen = line
    return "\n".join(lines).strip()


class HeadMetadataParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.title_parts: List[str] = []
        self.meta: List[dict[str, str]] = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = {str(k).lower(): str(v) for k, v in attrs if v is not None}
        if tag == "title":
            self.in_title = True
        elif tag == "meta":
            self.meta.append(attrs_dict)

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_parts.append(data)

    @property
    def title(self) -> str:
        return unescape("".join(self.title_parts)).strip()


def head_fragment(html: str, limit: int = 250_000) -> str:
    end = html.lower().find("</head>")
    if end != -1:
        return html[: end + len("</head>")]
    return html[:limit]


def parse_head(html: str) -> HeadMetadataParser:
    parser = HeadMetadataParser()
    parser.feed(head_fragment(html))
    return parser


def find_meta(html: str, attr_name: str, attr_value: str) -> str:
    attr_name = attr_name.lower()
    attr_value = attr_value.lower()
    parser = parse_head(html)
    for meta in parser.meta:
        if meta.get(attr_name, "").lower() == attr_value:
            return unescape(meta.get("content", "")).strip()
    return ""


def find_title(html: str) -> str:
    parser = parse_head(html)
    for attr_name, attr_value in [("property", "og:title"), ("name", "title")]:
        for meta in parser.meta:
            if meta.get(attr_name, "").lower() == attr_value:
                return unescape(meta.get("content", "")).strip()
    return parser.title


def strip_noise_lines(lines: List[str]) -> List[str]:
    banned_substrings = [
        "微信扫一扫",
        "轻触阅读原文",
        "继续滑动看下一个",
        "向上滑动看下一个",
        "赞赏作者",
        "阅读原文",
        "写留言",
        "留言",
        "分享",
        "收藏",
        "在看",
        "点赞",
    ]
    cleaned: List[str] = []
    for line in lines:
        line = line.strip()
        if not line:
            cleaned.append("")
            continue
        if line in {"原创"}:
            continue
        if any(token in line for token in banned_substrings):
            continue
        cleaned.append(line)
    return cleaned


def fetch_url(url: str) -> str:
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT)
    resp.raise_for_status()
    resp.encoding = resp.encoding or resp.apparent_encoding or "utf-8"
    return resp.text


def extract_wechat(url: str, html: str) -> ExtractionResult:
    parser = BlockHTMLToText(capture_root=("div", "id", "img-content"))
    parser.feed(html)
    text = normalize_text("\n".join(strip_noise_lines(parser.get_text().splitlines())))

    title = find_meta(html, "property", "og:title")
    if not title:
        match = re.search(r'<span class="js_title_inner">(.*?)</span>', html, re.S)
        title = unescape(match.group(1)).strip() if match else ""

    author = find_meta(html, "name", "author")
    description = find_meta(html, "name", "description")
    warnings: List[str] = []
    if len(text) < 400:
        warnings.append("Extracted text is short; the page may be truncated or heavily scripted.")

    return ExtractionResult(
        source_type="url",
        source=url,
        title=title,
        author=author,
        description=description,
        text=text,
        extraction_method="wechat-img-content",
        warnings=warnings,
    ).finalize()


def extract_generic_html(source: str, html: str, source_type: str) -> ExtractionResult:
    candidate = html
    for pattern in [
        r"<article\b.*?</article>",
        r"<main\b.*?</main>",
        r"<body\b.*?</body>",
    ]:
        match = re.search(pattern, html, re.I | re.S)
        if match:
            candidate = match.group(0)
            break

    parser = BlockHTMLToText()
    parser.feed(candidate)
    text = normalize_text(parser.get_text())
    warnings: List[str] = []
    if len(text) < 400:
        warnings.append("Extracted text is short; page layout or anti-bot protection may have limited the result.")

    return ExtractionResult(
        source_type=source_type,
        source=source,
        title=find_title(html),
        author=find_meta(html, "name", "author"),
        description=find_meta(html, "name", "description") or find_meta(html, "property", "og:description"),
        text=text,
        extraction_method="generic-html",
        warnings=warnings,
    ).finalize()


def read_local_file(path: Path) -> ExtractionResult:
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md", ".markdown"}:
        text = path.read_text(encoding="utf-8")
        title = path.stem.replace("-", " ").replace("_", " ").strip()
        return ExtractionResult(
            source_type="file",
            source=str(path),
            title=title,
            text=text,
            extraction_method="plain-text-file",
            warnings=[],
        ).finalize()
    if suffix in {".html", ".htm"}:
        html = path.read_text(encoding="utf-8")
        return extract_generic_html(str(path), html, "file")
    raise SystemExit(f"Unsupported file type for MVP extractor: {suffix or 'unknown'}")


def read_stdin_text(title: str = "") -> ExtractionResult:
    text = sys.stdin.read()
    return ExtractionResult(
        source_type="text",
        source="stdin",
        title=title,
        text=text,
        extraction_method="stdin",
        warnings=[],
    ).finalize()


def read_raw_text(raw: str, title: str = "") -> ExtractionResult:
    return ExtractionResult(
        source_type="text",
        source="inline",
        title=title,
        text=raw,
        extraction_method="inline-text",
        warnings=[],
    ).finalize()


def render_markdown(result: ExtractionResult) -> str:
    warnings = "\n".join(f"- {w}" for w in (result.warnings or [])) or "- none"
    return f"""# {result.title or 'Untitled'}

- Source type: {result.source_type}
- Source: {result.source}
- Author: {result.author or 'unknown'}
- Description: {result.description or 'n/a'}
- Method: {result.extraction_method}
- Characters: {result.char_count}
- Lines: {result.line_count}

## Warnings
{warnings}

## Text

{result.text}
"""


def render_text(result: ExtractionResult) -> str:
    head = [
        f"Title: {result.title or 'Untitled'}",
        f"Source type: {result.source_type}",
        f"Source: {result.source}",
        f"Author: {result.author or 'unknown'}",
        f"Method: {result.extraction_method}",
        f"Characters: {result.char_count}",
    ]
    if result.description:
        head.append(f"Description: {result.description}")
    if result.warnings:
        head.append("Warnings: " + " | ".join(result.warnings))
    return "\n".join(head) + "\n\n" + result.text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract article text from URL, file, stdin, or raw text")
    parser.add_argument("source", nargs="?", help="URL, local path, or raw inline text")
    parser.add_argument("--stdin", action="store_true", help="Read article text from stdin")
    parser.add_argument("--title", default="", help="Override or provide a title for stdin/raw text")
    parser.add_argument("--format", choices=["json", "markdown", "text"], default="json")
    parser.add_argument("--max-chars", type=int, default=0, help="Trim extracted text to this many characters")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.stdin:
        result = read_stdin_text(title=args.title)
    elif not args.source:
        raise SystemExit("Provide a source argument or use --stdin")
    elif re.match(r"^https?://", args.source):
        html = fetch_url(args.source)
        domain = urlparse(args.source).netloc
        if "mp.weixin.qq.com" in domain:
            result = extract_wechat(args.source, html)
        else:
            result = extract_generic_html(args.source, html, "url")
    else:
        path = Path(args.source)
        if path.exists():
            result = read_local_file(path)
        else:
            result = read_raw_text(args.source, title=args.title)

    if args.max_chars and len(result.text) > args.max_chars:
        result.text = result.text[: args.max_chars].rstrip() + "\n\n[TRUNCATED]"
        result.finalize()
        result.warnings = (result.warnings or []) + [f"Output truncated to {args.max_chars} characters."]

    if args.format == "json":
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
    elif args.format == "markdown":
        print(render_markdown(result))
    else:
        print(render_text(result))


if __name__ == "__main__":
    main()
