# Rhombus Developer Documentation

Official developer documentation for the Rhombus API. Built with Mintlify for a modern, interactive documentation experience.

## 📚 About

This repository contains the complete developer documentation for Rhombus Systems, including:

- **846+ API Endpoints**: Comprehensive coverage of all Rhombus API endpoints
- **Implementation Guides**: Real-world examples for video streaming, webhooks, and access control
- **Interactive Components**: Code examples, tabs, expandable sections, and more
- **Auto-Generated Content**: Nightly synchronization with production API via OpenAPI specification
- **AI Integration**: MCP server support, context files, and AI tool compatibility

## 🚀 Quick Start

### Prerequisites

- Node.js 19 or higher
- [Mintlify CLI](https://www.npmjs.com/package/mint)

### Local Development

1. **Install Mintlify CLI globally**:
   ```bash
   npm i -g mint
   ```

2. **Navigate to the docs directory**:
   ```bash
   cd docs
   ```

3. **Start the development server**:
   ```bash
   mint dev
   ```

4. **View your local preview**:
   Open `http://localhost:3000` in your browser

5. **Use a custom port** (if needed):
   ```bash
   mint dev --port 3333
   ```

## 📖 Documentation Structure

```
docs/
├── docs.json                 # Main configuration
├── index.mdx                 # Homepage
├── quickstart.mdx           # Getting started guide
├── changelog.mdx            # Update history with RSS
├── documentation-mcp.mdx    # MCP server guide
├── implementations/         # Implementation examples
├── low-code-no-code/       # Zapier and no-code guides
├── api-reference/          # API documentation
│   ├── openapi.json        # Full OpenAPI spec
│   ├── openapi-split/      # Split specs for AI tools
│   └── endpoint/           # Generated endpoint docs
├── scripts/                # Automation scripts
│   ├── update-openapi.sh   # Update OpenAPI spec
│   ├── split-openapi.sh    # Split spec into categories
│   └── update-llms-files.py # Update AI context files
└── .github/workflows/      # Automated workflows
```

## 🛠️ Common Commands

### Development

```bash
# Start local development server
mint dev

# Update Mintlify CLI to latest version
mint update

# Validate all links
mint broken-links
```

### Maintenance

```bash
# Update OpenAPI specification from Rhombus API
./scripts/update-openapi.sh

# Split OpenAPI spec into category files
./scripts/split-openapi.sh

# Update AI assistant context files
python3 scripts/update-llms-files.py
```

## 🤖 Automated Workflows

This repository includes several GitHub Actions workflows that run automatically:

### Update OpenAPI Spec
- **Schedule**: Daily at 2:00 AM UTC
- **Purpose**: Fetches latest API spec from production
- **File**: `.github/workflows/update-openapi.yml`
- **Output**: Updates `api-reference/openapi.json` and split files

### Update LLMs Context Files
- **Schedule**: Daily at 3:00 AM UTC
- **Purpose**: Updates AI assistant context files
- **File**: `.github/workflows/update-llms-files.yml`
- **Output**: Updates `llms.txt` and `llms-full.txt`

## 📝 Content Guidelines

### Adding New Pages

1. Create an `.mdx` file in the appropriate directory
2. Add frontmatter with `title`, `description`, and optional `icon`
3. Add the page to `docs.json` navigation
4. Use Mintlify components for rich content

### Frontmatter Format

```yaml
---
title: "Page Title"
description: "Brief description for SEO"
icon: "icon-name"
---
```

### Available Components

- **Callouts**: `<Note>`, `<Tip>`, `<Warning>`, `<Info>`, `<Check>`
- **Structure**: `<Steps>`, `<Tabs>`, `<AccordionGroup>`, `<Card>`, `<CardGroup>`
- **Code**: `<CodeGroup>`, `<RequestExample>`, `<ResponseExample>`
- **API**: `<ParamField>`, `<ResponseField>`, `<Expandable>`
- **Media**: `<Frame>` (for images), `<video>`, `<iframe>`

## 🔗 Important Links

- **Live Documentation**: [https://docs.rhombus.com](https://docs.rhombus.com)
- **Rhombus API**: [https://api2.rhombussystems.com](https://api2.rhombussystems.com)
- **OpenAPI Spec**: [https://api2.rhombussystems.com/api/openapi/public.json](https://api2.rhombussystems.com/api/openapi/public.json)
- **Developer Community**: [https://rhombus.community](https://rhombus.community)
- **Rhombus Console**: [https://console.rhombussystems.com](https://console.rhombussystems.com)

## 🤝 Contributing

### Reporting Issues

Found a bug or have a suggestion? Report it at:
- **Community**: [https://rhombus.community](https://rhombus.community)
- **Support**: [support@rhombus.com](mailto:support@rhombus.com)

### Making Changes

1. Create a feature branch
2. Make your changes
3. Test locally with `mint dev`
4. Run `mint broken-links` to validate
5. Submit a pull request

## 📚 Documentation Resources

- **CLAUDE.md**: Guidance for Claude Code AI assistant
- **AUTOMATION.md**: Complete automation workflow documentation
- **WORKFLOW_FIXES.md**: OpenAPI workflow troubleshooting guide
- **scripts/README.md**: Detailed script documentation

## 🔧 Troubleshooting

### Development Server Not Starting

```bash
# Update Mintlify CLI
mint update

# Ensure you're in the correct directory
cd docs

# Try with verbose output
mint dev --verbose
```

### Page Loads as 404

- Verify the page exists in `docs.json` navigation
- Check file path matches navigation entry
- Ensure `.mdx` extension is correct

### Broken Links

```bash
# Check for broken links
mint broken-links

# View specific broken links
mint broken-links --verbose
```

### OpenAPI Update Issues

```bash
# Test API availability
curl -I https://api2.rhombussystems.com/api/openapi/public.json

# Manual update
./scripts/update-openapi.sh

# Check workflow logs
gh run list --workflow=update-openapi.yml
```

## 📊 Project Statistics

- **API Endpoints**: 846+
- **Documentation Pages**: 100+
- **API Categories**: 60+
- **Update Frequency**: Daily (automated)
- **Languages Supported**: cURL, Python, JavaScript, Go

## 🎯 Features

### For Developers
- ✅ Complete API reference with all endpoints
- ✅ Interactive code examples in multiple languages
- ✅ Real-world implementation guides
- ✅ Webhook integration examples
- ✅ Video player setup with HLS streaming

### For AI Tools
- ✅ MCP server integration
- ✅ Claude Code compatibility
- ✅ Cursor editor support
- ✅ Auto-generated context files (llms.txt)
- ✅ Split OpenAPI specs for token efficiency

### For Maintainers
- ✅ Automated OpenAPI sync
- ✅ Automated context file updates
- ✅ Link validation
- ✅ GitHub Actions workflows
- ✅ Comprehensive error handling

## 📞 Support

- **Developer Community**: [rhombus.community](https://rhombus.community)
- **Email Support**: [support@rhombus.com](mailto:support@rhombus.com)
- **Technical Docs**: This repository
- **API Console**: [console.rhombussystems.com](https://console.rhombussystems.com)

## 📄 License

See [LICENSE](LICENSE) file for details.

## 🏢 About Rhombus

Rhombus is a security platform built on an API-first architecture since 2016. Everything in our system can be done via the Rhombus API - the same endpoints power our mobile apps, web console, and firmware.

Visit [rhombus.com](https://rhombus.com) to learn more.
