# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Mintlify documentation site** for Rhombus Developer Documentation. The repository contains MDX documentation pages structured for the Mintlify platform, which builds static documentation sites with rich interactive components.

The documentation covers the Rhombus API (846+ endpoints) for security platform integration including cameras, access control, environmental sensors, and analytics.

## Development Commands

### Essential Commands
```bash
# Install Mintlify CLI globally (required for local development)
npm i -g mint

# Start local development server (runs on http://localhost:3000)
mint dev

# Use custom port if 3000 is occupied
mint dev --port 3333

# Update Mintlify CLI to latest version
mint update

# Validate all links in documentation
mint broken-links
```

### Scripts
```bash
# Update OpenAPI spec from Rhombus API (includes automatic split)
./scripts/update-openapi.sh

# Split OpenAPI spec into smaller category files
./scripts/split-openapi.sh

# Update AI assistant context files (llms.txt and llms-full.txt)
python3 scripts/update-llms-files.py
```

## Project Structure

```
docs/
├── docs.json                     # Mintlify configuration (navigation, theme, colors)
├── index.mdx                     # Homepage with getting started content
├── quickstart.mdx               # Quick start guide for first API call
├── documentation-mcp.mdx        # MCP server documentation
├── development.mdx              # Local development guide
├── implementations/             # Implementation examples
│   ├── video-player.mdx        # Video streaming implementation
│   ├── advanced-implementation.mdx
│   └── webhook-listener.mdx    # Webhook integration example
├── low-code-no-code/           # No-code integration guides
│   └── zapier.mdx             # Zapier integration
├── api-reference/              # API documentation
│   ├── openapi.json            # Full OpenAPI spec (auto-updated nightly)
│   ├── openapi-split/          # Split specs by category for AI processing
│   │   ├── _base.json         # Base OpenAPI config
│   │   ├── _index.json        # Category index
│   │   ├── *.json             # Category-specific endpoint files
│   │   └── schemas/           # Schema definitions per category
│   └── endpoint/               # Auto-generated MDX endpoint docs
│       ├── access-control/
│       ├── camera/
│       ├── climate/
│       └── [other categories]/
├── scripts/                    # Automation scripts
│   ├── update-openapi.sh      # Fetch & update OpenAPI spec
│   └── split-openapi.sh       # Split spec into category files
├── .github/workflows/          # GitHub Actions
│   └── update-openapi.yml     # Nightly OpenAPI spec updates
└── .windsurf/                 # Windsurf IDE rules
    └── rules.md               # Writing standards & requirements
```

## Configuration

### Mintlify Configuration (`docs.json`)
- **Location**: `docs/docs.json` (26,633 tokens - very large file)
- **Theme**: Mint theme with blue color scheme (#2563EB primary)
- **Navigation**: Tab-based structure
  - "Guides" tab: Getting started, implementation examples, low-code integrations
  - "API reference" tab: Organized by service area with logical subgroups
- **API Endpoint Organization**: Grouped by category (Access Control, Camera, Climate, etc.) with subgroups:
  - Create & Add
  - Get & Find
  - Update & Modify
  - Delete & Remove
  - Other Operations
- **Favicon**: `/favicon.svg`

### Automated Workflows
- **OpenAPI Updates**: GitHub Action runs nightly at 2 AM UTC (`.github/workflows/update-openapi.yml`)
  - Workflow: Fetches spec → Validates JSON → Commits if changed → Splits into category files
  - Manual: Run `./scripts/update-openapi.sh` (includes validation and splitting)
- **LLMs Context Updates**: GitHub Action runs nightly at 3 AM UTC (`.github/workflows/update-llms-files.yml`)
  - Workflow: Analyzes structure → Generates llms.txt & llms-full.txt → Commits if changed
  - Manual: Run `python3 scripts/update-llms-files.py`
  - Purpose: Keeps AI assistant context files current with project structure

## Content Guidelines

### File Structure
All documentation pages must start with YAML frontmatter:
```yaml
---
title: "Page Title"
description: "Brief description of page content"
icon: "icon-name"  # Optional
---
```

### Mintlify Components
The documentation uses extensive Mintlify-specific MDX components:

**Callouts**: `<Note>`, `<Tip>`, `<Warning>`, `<Info>`, `<Check>`
**Structure**: `<Steps>`, `<Tabs>`, `<AccordionGroup>`, `<Card>`, `<CardGroup>`
**Code**: `<CodeGroup>`, `<RequestExample>`, `<ResponseExample>`
**API**: `<ParamField>`, `<ResponseField>`, `<Expandable>`
**Media**: `<Frame>` (for images), `<video>`, `<iframe>`

### Writing Standards
Reference the comprehensive rules in `docs/.windsurf/rules.md` for detailed writing guidelines, component usage, and content structure requirements. Key points:
- Use second person ("you") and active voice
- Start with prerequisites, include expected outcomes
- Test all code examples before publishing
- Use relative paths for internal links
- Maintain consistent naming patterns

## API Integration

### OpenAPI Specification
- **Source**: `https://api2.rhombussystems.com/api/openapi/public.json`
- **Full spec**: `docs/api-reference/openapi.json` (updated nightly)
- **Split specs**: `docs/api-reference/openapi-split/` (for AI/human review)
- **Base URL**: `https://api2.rhombussystems.com`
- **Authentication**: All endpoints require `x-auth-apikey` header

### Split OpenAPI Architecture
The large OpenAPI spec is split into smaller files for easier AI processing:
- `_base.json`: Core OpenAPI configuration (info, servers, security)
- `_index.json`: Summary of categories and endpoint counts
- Category files (e.g., `camera.json`, `access-control.json`): Endpoints grouped by service
- `schemas/`: Directory with schema definitions per category

**When analyzing API functionality**: Check `_index.json` to find the category, then reference the specific category file and its schema file.

## Deployment

Mintlify sites deploy automatically when changes are pushed to the default branch. The GitHub app integration handles the deployment pipeline.

## Important Development Notes

### Working with the Codebase
- **No package.json**: This is a Mintlify project without npm dependencies - use global `mint` CLI
- **Large config file**: `docs.json` is 26,633 tokens - avoid reading entire file; use grep/offset for specific sections
- **Auto-generated endpoints**: Files in `api-reference/endpoint/` are generated - don't edit directly
- **Manual docs**: Edit files in root docs/ and subdirectories (implementations/, low-code-no-code/, etc.)

### Testing & Validation
- Always test locally with `mint dev` before committing
- Use `mint broken-links` to validate internal links
- Verify MDX syntax compiles without errors
- Test code examples are accurate and runnable

### Content Best Practices
- All images must be wrapped in `<Frame>` components
- Include `x-auth-apikey` header in all API examples
- Reference live OpenAPI spec URL: `https://api2.rhombussystems.com/api/openapi/public.json`
- Use realistic example data, not placeholders
- Wrap images with descriptive alt text for accessibility

### API Documentation Standards
- All authentication examples must show both `x-auth-scheme` and `x-auth-apikey` headers
- Include both success and error response examples
- Document rate limiting and error handling best practices
- Reference the Rhombus Console for API key generation
- Emphasize API key security warnings