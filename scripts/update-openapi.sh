#!/bin/bash

# Script to manually update the OpenAPI specification from Rhombus API
# Usage: ./scripts/update-openapi.sh (run from docs/ directory)
#    or: ./docs/scripts/update-openapi.sh (run from project root)

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

API_URL="https://api2.rhombussystems.com/api/openapi/public.json"
OUTPUT_FILE="$BASE_DIR/api-reference/openapi.json"

echo "🔄 Fetching latest OpenAPI spec from Rhombus API..."
echo "📡 Source: $API_URL"

# Create backup of current spec
if [ -f "$OUTPUT_FILE" ]; then
    cp "$OUTPUT_FILE" "$OUTPUT_FILE.backup"
    echo "📋 Created backup: $OUTPUT_FILE.backup"
fi

# Download the latest spec
if curl -s "$API_URL" > "$OUTPUT_FILE"; then
    echo "✅ Successfully updated OpenAPI spec"
    
    # Validate it's valid JSON
    if jq empty "$OUTPUT_FILE" 2>/dev/null; then
        echo "✅ OpenAPI spec is valid JSON"
        
        # Show basic info about the spec
        TITLE=$(jq -r '.info.title // "Unknown"' "$OUTPUT_FILE")
        VERSION=$(jq -r '.info.version // "Unknown"' "$OUTPUT_FILE")
        PATHS_COUNT=$(jq '.paths | length' "$OUTPUT_FILE")
        
        echo "📊 API Info:"
        echo "   Title: $TITLE"
        echo "   Version: $VERSION"
        echo "   Endpoints: $PATHS_COUNT"
        
        # Remove backup if successful
        rm -f "$OUTPUT_FILE.backup"
    else
        echo "❌ Downloaded spec is not valid JSON, restoring backup"
        if [ -f "$OUTPUT_FILE.backup" ]; then
            mv "$OUTPUT_FILE.backup" "$OUTPUT_FILE"
        fi
        exit 1
    fi
else
    echo "❌ Failed to download OpenAPI spec"
    if [ -f "$OUTPUT_FILE.backup" ]; then
        mv "$OUTPUT_FILE.backup" "$OUTPUT_FILE"
    fi
    exit 1
fi

echo "🎉 OpenAPI spec update complete!"
