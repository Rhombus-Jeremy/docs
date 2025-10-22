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
# Update OpenAPI spec from Rhombus API
./scripts/update-openapi.sh

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
│   └── endpoint/               # (Empty - kept for future custom docs)
├── scripts/                    # Automation scripts
│   └── update-openapi.sh       # Fetch & update OpenAPI spec
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
  - Workflow: Fetches spec → Validates JSON → Commits if changed
  - Manual: Run `./scripts/update-openapi.sh`
  - Note: All 846+ endpoints are rendered directly from openapi.json via Mintlify
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
- **Base URL**: `https://api2.rhombussystems.com`
- **Authentication**: All endpoints require `x-auth-apikey` header
- **Rendering**: All 846+ endpoints are rendered directly from openapi.json via Mintlify's native OpenAPI support

### Navigation Structure
- Navigation in `docs.json` uses direct OpenAPI references: `"api-reference/openapi.json post /api/endpoint/path"`
- No individual MDX files per endpoint - all generated from OpenAPI spec
- Endpoint documentation updates automatically when openapi.json is updated

## Deployment

Mintlify sites deploy automatically when changes are pushed to the default branch. The GitHub app integration handles the deployment pipeline.

## Important Development Notes

### Working with the Codebase
- **No package.json**: This is a Mintlify project without npm dependencies - use global `mint` CLI
- **Large config file**: `docs.json` is ~1800 lines - avoid reading entire file; use grep/offset for specific sections
- **OpenAPI-driven endpoints**: All API endpoints rendered directly from `openapi.json` - no individual MDX files
- **Manual docs**: Edit files in root docs/ and subdirectories (implementations/, low-code-no-code/, etc.)
- **Empty endpoint directory**: `api-reference/endpoint/` exists but is empty, kept for future custom endpoint docs

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