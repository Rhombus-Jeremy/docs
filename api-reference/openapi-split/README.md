# Split OpenAPI Documentation

This directory contains the Rhombus OpenAPI specification split into smaller, more manageable files for AI processing and human review.

## Structure

### Base Files
- **_base.json** - Core OpenAPI configuration (info, servers, security)
- **_index.json** - Summary of all categories and endpoint counts

### Category Files
Each API category has its own file (e.g., `access-control.json`, `camera.json`) containing:
- All endpoints for that category
- List of referenced schemas
- Endpoint count and methods

### Schema Files
The `schemas/` directory contains extracted schema definitions for each category:
- Only includes schemas referenced by that category's endpoints
- Reduces file size for focused analysis

## Usage for AI

When analyzing specific API functionality:
1. Check `_index.json` to find the relevant category
2. Open the category file (e.g., `camera.json`) to see endpoints
3. Reference the corresponding schema file (e.g., `schemas/camera-schemas.json`) for data structures

## Regeneration

This directory is automatically regenerated when running:
```bash
./scripts/update-openapi.sh
```

The split happens after fetching the latest spec from the Rhombus API.
