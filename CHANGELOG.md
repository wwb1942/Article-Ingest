# Changelog

All notable changes to this repository will be documented in this file.

The format is loosely based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

- Ongoing documentation and packaging polish.

## [v0.1.8] - 2026-03-13

### Fixed

- increased CTA pill text contrast so the button labels remain readable on the GitHub repo page
- switched pill text from pale-on-pale to dark-on-light with a subtle shadow

## [v0.1.7] - 2026-03-13

### Fixed

- tightened the README banner layout to keep all text inside a strict right-side safe area
- shortened the banner copy to avoid clipping on the GitHub repository page

## [v0.1.6] - 2026-03-13

### Fixed

- replaced the README SVG banner with a rasterized PNG banner for stable GitHub rendering
- removed cross-renderer font metric drift from the repo landing image

## [v0.1.5] - 2026-03-13

### Fixed

- adjusted README banner typography and spacing for more stable GitHub rendering
- widened and centered CTA pills to avoid text crowding

## [v0.1.4] - 2026-03-13

### Added

- README banner artwork for a stronger public landing page
- repository-facing visual polish for the public GitHub page

## [v0.1.3] - 2026-03-13

### Added

- GitHub Actions CI workflow for syntax and CLI help validation
- CI badge in README

### Fixed

- CI runtime now installs the required `requests` dependency before running the CLI help check

## [v0.1.2] - 2026-03-13

### Added

- SECURITY.md with a private reporting preference
- SUPPORT.md with support and issue guidance
- GitHub issue templates for bugs and feature requests
- Pull request template for cleaner contributions

## [v0.1.1] - 2026-03-13

### Added

- Refined README with use-cases, non-goals, quick links, and example output shapes
- Added clearer installation notes and repository navigation


## [v0.1.0] - 2026-03-13

### Added

- Initial public standalone repository for the `Article-Ingest` OpenClaw skill
- `SKILL.md` skill contract and workflow guidance
- `scripts/article_ingest.py` extraction script
- `references/output-templates.md` digest and knowledge-card templates
- Packaged release artifact: `dist/article-ingest.skill`
- MIT license
