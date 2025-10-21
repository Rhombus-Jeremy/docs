#!/usr/bin/env python3
"""
Generate Mintlify endpoint documentation from OpenAPI split files.
Creates organized MDX files for all API endpoints with proper navigation.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any

# Configuration
SPLIT_DIR = Path("docs/api-reference/openapi-split")
ENDPOINT_DIR = Path("docs/api-reference/endpoint")
SCHEMAS_DIR = SPLIT_DIR / "schemas"

def sanitize_filename(name: str) -> str:
    """Convert endpoint path to valid filename."""
    # Remove /api/ prefix and convert to lowercase
    name = name.replace("/api/", "").lower()
    # Replace slashes with hyphens
    name = name.replace("/", "-")
    # Remove special characters
    name = re.sub(r'[^a-z0-9\-]', '', name)
    return name

def get_method_and_summary(endpoint_data: Dict) -> tuple:
    """Extract HTTP method and summary from endpoint data."""
    for method in ['get', 'post', 'put', 'delete', 'patch']:
        if method in endpoint_data:
            details = endpoint_data[method]
            return method.upper(), details.get('summary', ''), details.get('description', ''), details.get('deprecated', False)
    return 'POST', '', '', False

def generate_mdx_content(path: str, endpoint_data: Dict, category: str) -> str:
    """Generate MDX content for an endpoint."""
    method, summary, description, deprecated = get_method_and_summary(endpoint_data)

    # Use summary as title, fallback to path
    title = summary or path.replace('/api/', '')

    # Clean description or use summary
    desc = description or summary or f"API endpoint for {path}"
    if len(desc) > 160:
        desc = desc[:157] + "..."

    # Determine icon based on category
    icon_map = {
        'camera': 'camera',
        'access-control': 'lock',
        'user': 'user',
        'event': 'calendar',
        'location': 'map-pin',
        'door': 'door-open',
        'sensor': 'sensor',
        'video': 'video',
        'alert': 'bell',
        'org': 'building',
        'webhook': 'webhook',
        'oauth': 'key',
        'report': 'chart-bar'
    }

    icon = icon_map.get(category, 'circle-dot')

    # Build frontmatter
    frontmatter = f"""---
title: "{title}"
description: "{desc}"
openapi: "{method} {path}"
icon: "{icon}"
"""

    if deprecated:
        frontmatter += 'deprecated: true\n'

    frontmatter += "---\n\n"

    # Build content
    content = frontmatter

    # Add detailed description if available
    if description and description != summary:
        content += f"{description}\n\n"

    # Add deprecation notice
    if deprecated:
        content += '<Warning>\nThis endpoint is deprecated and may be removed in a future version.\n</Warning>\n\n'

    # Note about auto-generated docs
    content += '<Note>\nThe parameters and response fields below are automatically generated from the OpenAPI specification.\n</Note>\n'

    return content

def process_category_file(category_file: Path) -> Dict[str, str]:
    """Process a category JSON file and generate MDX files."""
    print(f"Processing: {category_file.name}")

    with open(category_file, 'r') as f:
        data = json.load(f)

    category = category_file.stem
    category_display = data.get('tag', category)
    paths = data.get('paths', {})

    if not paths:
        print(f"  ⚠️  No paths found in {category_file.name}")
        return {}

    # Create category directory
    category_dir = ENDPOINT_DIR / category
    category_dir.mkdir(parents=True, exist_ok=True)

    generated_files = {}
    endpoint_count = 0

    for path, methods in paths.items():
        # Generate filename from path
        filename = sanitize_filename(path) + ".mdx"
        filepath = category_dir / filename

        # Generate MDX content
        mdx_content = generate_mdx_content(path, methods, category)

        # Write file
        with open(filepath, 'w') as f:
            f.write(mdx_content)

        # Store path WITHOUT .mdx extension for navigation
        nav_path = str(filepath.relative_to('docs')).replace('.mdx', '')
        generated_files[path] = nav_path
        endpoint_count += 1

    print(f"  ✅ Generated {endpoint_count} endpoint(s) in {category}/")
    return generated_files

def generate_navigation_structure(all_endpoints: Dict[str, Dict[str, str]]) -> List[Dict]:
    """Generate navigation structure for docs.json."""
    nav_groups = []

    # Load category display names from index
    with open(SPLIT_DIR / "_index.json", 'r') as f:
        index_data = json.load(f)
        categories = index_data.get('categories', [])

    # Create mapping from filename to display name
    category_names = {}
    for cat in categories:
        filename = cat.lower().replace(' webservice', '').replace(' ', '-')
        category_names[filename] = cat.replace(' Webservice', '')

    for category, endpoints in sorted(all_endpoints.items()):
        display_name = category_names.get(category, category.replace('-', ' ').title())

        # Create pages list for this category
        pages = [path for path in sorted(endpoints.values())]

        if pages:
            nav_groups.append({
                "group": display_name,
                "pages": pages
            })

    return nav_groups

def main():
    """Main execution function."""
    print("🔨 Generating Mintlify endpoint documentation from OpenAPI split files\n")

    # Ensure directories exist
    ENDPOINT_DIR.mkdir(parents=True, exist_ok=True)

    # Find all category JSON files (exclude _base.json and _index.json)
    category_files = [
        f for f in SPLIT_DIR.glob("*.json")
        if not f.name.startswith("_")
    ]

    if not category_files:
        print("❌ No category files found in", SPLIT_DIR)
        return

    print(f"📁 Found {len(category_files)} category files\n")

    # Process each category
    all_endpoints = {}
    total_generated = 0

    for category_file in sorted(category_files):
        endpoints = process_category_file(category_file)
        if endpoints:
            all_endpoints[category_file.stem] = endpoints
            total_generated += len(endpoints)

    print(f"\n✅ Generated {total_generated} endpoint documentation pages")
    print(f"📁 Output directory: {ENDPOINT_DIR}")

    # Generate navigation structure
    print("\n📚 Generating navigation structure...")
    nav_structure = generate_navigation_structure(all_endpoints)

    nav_output_file = Path("docs/api-reference/endpoint/_navigation.json")
    with open(nav_output_file, 'w') as f:
        json.dump(nav_structure, f, indent=2)

    print(f"✅ Navigation structure saved to {nav_output_file}")
    print(f"   Copy this into the 'API reference' tab in docs/docs.json")

    # Show summary
    print("\n📊 Summary by Category:")
    for category, endpoints in sorted(all_endpoints.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"   {category}: {len(endpoints)} endpoints")

    print("\n🎉 Documentation generation complete!")
    print("\n💡 Next steps:")
    print("   1. Review generated files in docs/api-reference/endpoint/")
    print("   2. Update docs/docs.json with navigation from _navigation.json")
    print("   3. Run 'mint dev' to preview the documentation")

if __name__ == "__main__":
    main()
