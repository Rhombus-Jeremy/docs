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

# Split OpenAPI spec into category files for AI tools
./scripts/split-openapi.sh

# Update AI assistant context files (llms.txt and llms-full.txt)
python3 scripts/update-llms-files.py

# Generate individual endpoint MDX files (legacy, not actively used)
python3 scripts/generate-endpoint-docs.py

# Improve endpoint navigation structure (legacy)
python3 scripts/improve-endpoint-navigation.py

# Update docs.json navigation structure (legacy)
python3 scripts/update-docs-navigation.py

# Add service-level navigation (legacy)
python3 scripts/add-service-level-navigation.py
```

## High-Level Architecture

### Documentation Generation Model

This project uses a **hybrid documentation model** that combines:

1. **Auto-generated API Reference**: All 846+ API endpoints are rendered directly from `openapi.json` via Mintlify's native OpenAPI support. There are **no individual MDX files per endpoint** - the entire API reference is generated on-the-fly from the OpenAPI specification.

2. **Hand-crafted Guides**: Implementation guides, tutorials, and conceptual documentation are written as MDX files in directories like `implementations/` and `low-code-no-code/`.

3. **Automated Synchronization**: GitHub Actions workflows update the OpenAPI spec nightly at 2 AM UTC, ensuring the API documentation stays current with production without manual intervention.

### Key Architectural Decisions

**OpenAPI-Driven API Docs**: The decision to render all API endpoints from `openapi.json` rather than maintaining individual MDX files means:
- Changes to the API automatically appear in docs when `openapi.json` is updated
- No need to manually update 846+ individual endpoint files
- Consistent formatting across all API endpoints
- The `api-reference/endpoint/` directory exists but is empty (kept for potential future custom docs)

**Split OpenAPI Specs**: The `api-reference/openapi-split/` directory contains category-specific OpenAPI files (e.g., `access-control.json`, `camera.json`). This architecture enables:
- AI tools with token limits to load only relevant API categories
- Faster context loading for targeted development work
- Better performance when working with specific API domains

**Navigation via `docs.json` References**: API endpoints are referenced in navigation using the pattern `"api-reference/openapi.json post /api/endpoint/path"`. This creates a direct link between the navigation structure and the OpenAPI spec without requiring intermediate MDX files.

## Project Structure

```
docs/
├── docs.json                     # Mintlify configuration (navigation, theme, colors)
├── index.mdx                     # Homepage with getting started content
├── quickstart.mdx               # Quick start guide for first API call
├── changelog.mdx                # Update history with RSS feed support
├── documentation-mcp.mdx        # MCP server documentation
├── development.mdx              # Local development guide
├── implementations/             # Implementation examples
│   ├── streaming-video.mdx     # Video streaming overview
│   ├── video-player.mdx        # Video player implementation
│   ├── advanced-implementation.mdx  # Advanced video features
│   └── webhook-listener.mdx    # Webhook integration example
├── low-code-no-code/           # No-code integration guides
│   ├── zapier.mdx             # Zapier integration
│   └── make.mdx               # Make.com integration
├── snippets/                   # Reusable MDX components
│   └── snippet-intro.mdx      # Common intro snippets
├── api-reference/              # API documentation
│   ├── openapi.json            # Full OpenAPI spec (auto-updated nightly)
│   ├── openapi-split/          # Split specs by category for AI tools
│   └── endpoint/               # (Empty - kept for future custom docs)
├── scripts/                    # Automation scripts
│   ├── update-openapi.sh       # Fetch & update OpenAPI spec
│   ├── split-openapi.sh        # Split spec into category files
│   ├── update-llms-files.py    # Update AI context files
│   └── *.py                    # Legacy navigation/generation scripts
├── .github/workflows/          # GitHub Actions
│   ├── update-openapi.yml      # Nightly OpenAPI spec updates (2 AM UTC)
│   └── update-llms-files.yml   # Nightly AI context updates (3 AM UTC)
├── .windsurf/                 # Windsurf IDE rules
│   └── rules.md               # Writing standards & requirements
└── .claude/                   # Claude Code project memory
    └── mintlify-implementation-reference.md  # Mintlify best practices
```

## Configuration

### Mintlify Configuration (`docs.json`)
- **Location**: `docs/docs.json` (~1800 lines, 26,633 tokens - very large file)
- **Theme**: Mint theme with blue color scheme (#2563EB primary)
- **Navigation**: Tab-based structure with two main tabs:
  - "Guides" tab: Getting started, implementation examples, low-code integrations
  - "API reference" tab: Organized by service area with logical subgroups
- **API Endpoint Organization**: Grouped by category (Access Control, Camera, Climate, etc.) with subgroups:
  - Create & Add
  - Get & Find
  - Update & Modify
  - Delete & Remove
  - Other Operations
- **Favicon**: `/favicon.svg`

**Important**: When working with `docs.json`, avoid reading the entire file. Use `grep` or `Read` with offset/limit parameters to target specific sections. The navigation structure alone is ~1500 lines.

### Automated Workflows

#### OpenAPI Updates
- **GitHub Action**: Runs nightly at 2 AM UTC (`.github/workflows/update-openapi.yml`)
- **Workflow**: Fetches spec → Validates JSON → Splits into categories → Commits if changed
- **Manual execution**: Run `./scripts/update-openapi.sh` (then optionally `./scripts/split-openapi.sh`)
- **Output**: Updates both `openapi.json` and split files in `openapi-split/` directory
- **Source**: `https://api2.rhombussystems.com/api/openapi/public.json`

#### LLMs Context Updates
- **GitHub Action**: Runs nightly at 3 AM UTC (`.github/workflows/update-llms-files.yml`)
- **Workflow**: Analyzes structure → Generates llms.txt & llms-full.txt → Commits if changed
- **Manual execution**: Run `python3 scripts/update-llms-files.py`
- **Purpose**: Keeps AI assistant context files current with project structure
- **Output**: Two context files at different detail levels for AI tools

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
**Reusable**: `<Snippet>` for including content from `snippets/` directory

### Writing Standards
Reference the comprehensive rules in `.windsurf/rules.md` for detailed writing guidelines, component usage, and content structure requirements. Key points:
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
Navigation in `docs.json` uses direct OpenAPI references with the pattern:
```json
"api-reference/openapi.json post /api/endpoint/path"
```

**Critical**: There are no individual MDX files per endpoint. All API documentation is generated from the OpenAPI spec. The `api-reference/endpoint/` directory is empty and kept for potential future custom endpoint documentation.

When endpoint documentation updates automatically, it happens through the `openapi.json` update, not through individual file changes.

## AI Integration Features

### Context Files
- **llms.txt**: Lightweight context file (~500 lines) with project overview and structure
- **llms-full.txt**: Comprehensive context file with full documentation map
- Both files auto-updated nightly to reflect current documentation state
- Used by AI tools (Claude Code, Cursor, etc.) to understand project structure

### Split OpenAPI Specifications
- **Purpose**: Token-efficient API reference for AI tools
- **Location**: `openapi-split/` directory
- **Organization**: One file per API category (access-control.json, camera.json, etc.)
- **Usage**: When AI tools need specific API endpoints without loading full 846+ endpoint spec
- **Update**: Automatically regenerated when main `openapi.json` is updated

### MCP Server
- **Documentation**: See `documentation-mcp.mdx` for setup and usage
- **Purpose**: Enables AI assistants to directly access Rhombus API documentation
- **Integration**: Works with Claude Desktop and other MCP-compatible tools

### Mintlify Implementation Reference
- **Location**: `.claude/mintlify-implementation-reference.md`
- **Content**: Comprehensive Mintlify best practices from official docs (Context7)
- **Purpose**: Reference for implementing Mintlify features correctly
- **Source**: Trust Score 9.6, 336+ code snippets from official Mintlify documentation

## Deployment

Mintlify sites deploy automatically when changes are pushed to the default branch. The GitHub app integration handles the deployment pipeline.

**Live Documentation**: https://docs.rhombus.com

## Important Development Notes

### Working with the Codebase

**No package.json**: This is a Mintlify project without npm dependencies. Use the global `mint` CLI installed via `npm i -g mint`.

**Large config file**: `docs.json` is ~1800 lines (26,633 tokens). Avoid reading the entire file - use `grep` or `Read` with offset/limit for specific sections. The navigation array is particularly large.

**OpenAPI-driven endpoints**: All API endpoints rendered directly from `openapi.json`. Do not create individual MDX files for API endpoints unless absolutely necessary for custom documentation.

**Split OpenAPI specs**: Category-specific specs in `openapi-split/` are regenerated automatically. These are for AI tools with token limits - don't manually edit them.

**Manual docs**: Edit files in root `docs/` and subdirectories (`implementations/`, `low-code-no-code/`, etc.) for guides and conceptual documentation.

**Empty endpoint directory**: `api-reference/endpoint/` exists but is empty. It's kept for future custom endpoint docs if needed. The current architecture doesn't require it.

**Reusable snippets**: Common content in `snippets/` directory can be included via `<Snippet>` component. Use this for repeated content across multiple pages.

**Changelog with RSS**: `changelog.mdx` includes RSS feed support for update notifications.

### Testing & Validation

- Always test locally with `mint dev` before committing
- Use `mint broken-links` to validate internal links
- Verify MDX syntax compiles without errors in the dev server
- Test code examples are accurate and runnable
- Check that navigation changes appear correctly in local preview

### Content Best Practices

- All images must be wrapped in `<Frame>` components with descriptive alt text
- Include `x-auth-apikey` header in all API examples
- Reference live OpenAPI spec URL: `https://api2.rhombussystems.com/api/openapi/public.json`
- Use realistic example data, not placeholders like "your-api-key-here"
- Wrap images with descriptive alt text for accessibility

### API Documentation Standards

- All authentication examples must show the `x-auth-apikey` header
- Include both success and error response examples
- Document rate limiting and error handling best practices
- Reference the Rhombus Console (https://console.rhombussystems.com) for API key generation
- Emphasize API key security warnings in authentication documentation

### Navigation Updates

When adding new pages to `docs.json`:
1. Identify the correct tab and group for the page
2. Use relative paths from the `docs/` directory (e.g., `"implementations/new-guide"`)
3. For API endpoints, use the OpenAPI reference pattern: `"api-reference/openapi.json METHOD /path"`
4. Test navigation in local dev server before committing
5. Maintain alphabetical ordering within groups when appropriate

### Script Usage Patterns

**Active scripts** (use these):
- `./scripts/update-openapi.sh` - Updates OpenAPI spec from production
- `./scripts/split-openapi.sh` - Splits OpenAPI into category files
- `python3 scripts/update-llms-files.py` - Updates AI context files

**Legacy scripts** (historical, not actively used):
- `generate-endpoint-docs.py` - From before OpenAPI-driven architecture
- `improve-endpoint-navigation.py` - From before current navigation structure
- `update-docs-navigation.py` - From before current navigation structure
- `add-service-level-navigation.py` - From before current navigation structure

These legacy scripts are kept for reference but shouldn't be used in normal development.
