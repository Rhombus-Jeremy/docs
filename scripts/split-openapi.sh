#!/bin/bash

# Script to split large OpenAPI spec into smaller, AI-digestible files
# Organizes endpoints by tag/category and extracts relevant schemas
# Usage: ./scripts/split-openapi.sh (run from docs/ directory)
#    or: ./docs/scripts/split-openapi.sh (run from project root)

set -e

# Determine if we're in docs/ or project root
if [ -f "docs.json" ]; then
    # We're in docs/ directory
    BASE_DIR="."
elif [ -f "docs/docs.json" ]; then
    # We're in project root
    BASE_DIR="docs"
else
    echo "❌ Error: Could not find docs.json. Please run from docs/ directory or project root."
    exit 1
fi

INPUT_FILE="$BASE_DIR/api-reference/openapi.json"
OUTPUT_DIR="$BASE_DIR/api-reference/openapi-split"
SCHEMAS_DIR="$OUTPUT_DIR/schemas"

echo "🔪 Splitting OpenAPI spec into smaller files..."

# Create output directories
mkdir -p "$OUTPUT_DIR"
mkdir -p "$SCHEMAS_DIR"

# Extract base information (info, servers, security, etc.)
echo "📋 Extracting base configuration..."
jq '{
  openapi: .openapi,
  info: .info,
  servers: .servers,
  security: .security,
  "x-samples-languages": .["x-samples-languages"]
}' "$INPUT_FILE" > "$OUTPUT_DIR/_base.json"

# Get all unique tags
TAGS=$(jq -r '[.paths | to_entries[] | .value | to_entries[] | .value.tags[]?] | unique | .[]' "$INPUT_FILE")

# Create index file
echo "📊 Creating index..."
jq '{
  title: .info.title,
  version: .info.version,
  totalEndpoints: (.paths | length),
  totalSchemas: (.components.schemas | length),
  categories: [.paths | to_entries[] | .value | to_entries[] | .value.tags[]?] | unique | sort
}' "$INPUT_FILE" > "$OUTPUT_DIR/_index.json"

# Counter for progress
TOTAL_TAGS=$(echo "$TAGS" | wc -l | tr -d ' ')
CURRENT=0

echo "📁 Splitting into $TOTAL_TAGS category files..."

# Process each tag
echo "$TAGS" | while IFS= read -r tag; do
    CURRENT=$((CURRENT + 1))

    # Create filename from tag (lowercase, replace spaces with hyphens)
    FILENAME=$(echo "$tag" | tr '[:upper:]' '[:lower:]' | sed 's/ /-/g' | sed 's/webservice//g' | sed 's/--/-/g' | sed 's/-$//g')
    OUTPUT_FILE="$OUTPUT_DIR/${FILENAME}.json"

    echo "  [$CURRENT/$TOTAL_TAGS] Processing: $tag → ${FILENAME}.json"

    # Extract paths for this tag and collect referenced schemas
    jq --arg tag "$tag" '
    {
      tag: $tag,
      description: ("API endpoints for " + $tag),
      paths: (
        .paths | to_entries | map(
          select(.value | to_entries[] | .value.tags[]? == $tag)
        ) | from_entries
      ),
      endpoints: [
        .paths | to_entries[] |
        select(.value | to_entries[] | .value.tags[]? == $tag) |
        {
          path: .key,
          methods: [.value | to_entries[] | select(.value.tags[]? == $tag) | .key]
        }
      ],
      endpointCount: [
        .paths | to_entries[] |
        select(.value | to_entries[] | .value.tags[]? == $tag) |
        .value | to_entries[] | select(.value.tags[]? == $tag)
      ] | length,
      referencedSchemas: [
        .paths | to_entries[] |
        select(.value | to_entries[] | .value.tags[]? == $tag) |
        .value | .. | .["$ref"]? | select(. != null) |
        select(startswith("#/components/schemas/")) |
        gsub("#/components/schemas/"; "")
      ] | unique | sort
    }
    ' "$INPUT_FILE" > "$OUTPUT_FILE"

    # Extract schemas for this category
    SCHEMA_FILE="$SCHEMAS_DIR/${FILENAME}-schemas.json"

    # Get all referenced schemas for this tag and extract them
    jq --arg tag "$tag" '
    . as $root |
    [
      .paths | to_entries[] |
      select(.value | to_entries[] | .value.tags[]? == $tag) |
      .value | .. | .["$ref"]? | select(. != null) |
      select(startswith("#/components/schemas/")) |
      gsub("#/components/schemas/"; "")
    ] | unique as $refs |
    {
      tag: $tag,
      schemas: (
        $root.components.schemas |
        to_entries |
        map(select(.key as $k | $refs | index($k))) |
        from_entries
      ),
      schemaCount: (
        $root.components.schemas |
        to_entries |
        map(select(.key as $k | $refs | index($k))) |
        length
      )
    }
    ' "$INPUT_FILE" > "$SCHEMA_FILE"
done

# Create a README for the split directory
cat > "$OUTPUT_DIR/README.md" << 'EOF'
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
EOF

# Generate statistics
echo ""
echo "✅ Split complete! Statistics:"
echo "   📁 Output directory: $OUTPUT_DIR"
echo "   📄 Category files: $(find "$OUTPUT_DIR" -maxdepth 1 -name "*.json" ! -name "_*" | wc -l | tr -d ' ')"
echo "   📦 Schema files: $(find "$SCHEMAS_DIR" -name "*.json" | wc -l | tr -d ' ')"
echo ""
echo "💡 Use _index.json to navigate categories"
echo "📖 See $OUTPUT_DIR/README.md for usage guide"
