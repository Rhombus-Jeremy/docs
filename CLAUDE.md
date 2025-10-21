# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **Mintlify documentation site** for Rhombus Developer Documentation. The repository contains MDX documentation pages structured for the Mintlify platform, which builds static documentation sites with rich interactive components.

## Development Commands

### Essential Commands
```bash
# Install Mintlify CLI globally
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
```

## Project Structure

```
docs/                           # Main documentation directory
├── docs.json                  # Mintlify configuration file
├── index.mdx                  # Homepage
├── quickstart.mdx            # Quick start guide
├── development.mdx           # Local development guide
├── essentials/               # Core documentation guides
│   ├── settings.mdx         # Site customization
│   ├── navigation.mdx       # Navigation setup
│   ├── markdown.mdx         # MDX writing guide
│   ├── code.mdx            # Code samples
│   ├── images.mdx          # Image handling
│   └── reusable-snippets.mdx
├── ai-tools/                 # AI tool integration guides
│   ├── cursor.mdx           # Cursor editor setup
│   ├── claude-code.mdx      # Claude Code setup
│   └── windsurf.mdx         # Windsurf setup
├── api-reference/           # API documentation
│   ├── introduction.mdx     # API intro
│   ├── openapi.json         # Rhombus OpenAPI spec
│   └── endpoint/            # API endpoint examples
├── snippets/                # Reusable content snippets
└── images/                  # Documentation assets
```

## Configuration

### Mintlify Configuration (`docs.json`)
- **Theme**: Mint theme with custom green color scheme
- **Navigation**: Tab-based with "Guides" and "API reference" sections
- **Auto-sync**: OpenAPI spec from `https://api2.rhombussystems.com/api/openapi/public.json`
- **Contextual actions**: Copy, view in IDE, AI tool integration

### Automated Workflows
- **OpenAPI Updates**: GitHub Action runs nightly at 2 AM UTC to fetch latest API spec
- **Manual Updates**: Run `./scripts/update-openapi.sh` to update spec manually

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
Reference the comprehensive Cursor rules in `docs/ai-tools/cursor.mdx` for detailed writing guidelines, component usage, and content structure requirements.

## API Integration

### OpenAPI Specification
- **Source**: Rhombus API (`api2.rhombussystems.com`)
- **File**: `docs/api-reference/openapi.json`
- **Updates**: Automated nightly via GitHub Actions
- **Manual update**: Use `scripts/update-openapi.sh`

The OpenAPI spec is automatically integrated into the Mintlify site for interactive API documentation.

## Deployment

Mintlify sites deploy automatically when changes are pushed to the default branch. The GitHub app integration handles the deployment pipeline.

## Important Notes

- All images should be wrapped in `<Frame>` components
- Use proper MDX component syntax throughout documentation
- Test locally with `mint dev` before committing changes
- The site uses a custom green theme matching Rhombus branding
- API documentation auto-generates from the OpenAPI specification