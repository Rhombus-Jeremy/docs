# Rhombus Developer Documentation Rules

## Project context

- This is the **Rhombus Developer Documentation** project built on the Mintlify platform
- We document the complete Rhombus Systems API with 846+ endpoints
- We use MDX files with YAML frontmatter for all documentation
- Navigation is configured in `docs.json` with tabs for Guides and API reference
- API documentation is auto-generated from OpenAPI spec and updated nightly
- We follow technical writing best practices for developer documentation

## Writing standards

- Use second person ("you") for instructions
- Write in active voice and present tense
- Start procedures with prerequisites
- Include expected outcomes for major steps
- Use descriptive, keyword-rich headings
- Keep sentences concise but informative

## Required page structure

Every page must start with frontmatter:

```yaml
---
title: "Clear, specific title"
description: "Concise description for SEO and navigation"
---
```

## Mintlify components

### Callouts

- `<Note>` for helpful supplementary information
- `<Warning>` for important cautions and breaking changes
- `<Tip>` for best practices and expert advice  
- `<Info>` for neutral contextual information
- `<Check>` for success confirmations

### Code examples

- When appropriate, include complete, runnable examples
- Use `<CodeGroup>` for multiple language examples
- Specify language tags on all code blocks
- Include realistic data, not placeholders
- Use `<RequestExample>` and `<ResponseExample>` for API docs

### Procedures

- Use `<Steps>` component for sequential instructions
- Include verification steps with `<Check>` components when relevant
- Break complex procedures into smaller steps

### Content organization

- Use `<Tabs>` for platform-specific content
- Use `<Accordion>` for progressive disclosure
- Use `<Card>` and `<CardGroup>` for highlighting content
- Wrap images in `<Frame>` components with descriptive alt text

## API documentation requirements

- Document all parameters with `<ParamField>`
- Show response structure with `<ResponseField>`
- Include both success and error examples
- Use `<Expandable>` for nested object properties
- Always include authentication examples with `x-auth-apikey` header
- Reference the live OpenAPI specification at `https://api2.rhombussystems.com/api/openapi/public.json`
- Use the base URL `https://api2.rhombussystems.com` for all examples

## Rhombus-specific standards

### API authentication

- All endpoints require the `x-auth-apikey` header
- Include security warnings about API key protection
- Reference the Rhombus Console for API key generation
- Always show authentication in code examples

### Endpoint organization

- Group endpoints by service area (Access Control, Camera, Climate, etc.)
- Use logical subgroups: Create & Add, Get & Find, Update & Modify, Delete & Remove, Other Operations
- Maintain consistent naming patterns across similar endpoints

### Security documentation

- Emphasize API key security in all authentication sections
- Include rate limiting information and best practices
- Document proper error handling for authentication failures
- Provide guidance on implementing exponential backoff

## Automation and maintenance

### OpenAPI specification updates

- API documentation is auto-generated from the live OpenAPI spec
- Nightly updates occur at 2 AM UTC via GitHub Actions
- Manual updates available via `scripts/update-openapi.sh`
- Changes are automatically detected and committed

### File structure

- Auto-generated API endpoints are in `api-reference/endpoint/`
- Manual documentation goes in appropriate sections (guides, essentials, ai-tools)
- OpenAPI spec is stored at `api-reference/openapi.json`
- Split specifications are in `api-reference/openapi-split/`

### Update process documentation

- Document the automation workflow in `api-reference/README.md`
- Include troubleshooting steps for failed updates
- Maintain backup copies of working configurations

## Quality standards

- Test all code examples before publishing
- Use relative paths for internal links
- Include alt text for all images
- Ensure proper heading hierarchy (start with h2)
- Check existing patterns for consistency
