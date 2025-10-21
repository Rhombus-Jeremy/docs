#!/usr/bin/env python3
"""
Improve endpoint navigation by adding better icons and organizing with accordion groups.
Groups endpoints by action type (Create, Read, Update, Delete, etc.) for cleaner navigation.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

# Configuration
ENDPOINT_DIR = Path("docs/api-reference/endpoint")
DOCS_JSON = Path("docs/docs.json")
BACKUP_JSON = Path("docs/docs.json.backup")

# Icon mapping based on action type
ACTION_ICONS = {
    'create': 'square-plus',
    'add': 'user-plus',
    'upload': 'cloud-arrow-up',
    'generate': 'wand-magic-sparkles',
    'calibrate': 'sliders',
    'initiate': 'play',
    'trigger': 'bolt',

    'get': 'eye',
    'find': 'magnifying-glass',
    'search': 'magnifying-glass',
    'list': 'list',
    'getall': 'list-check',
    'findall': 'list-check',

    'update': 'pen-to-square',
    'edit': 'pen',
    'modify': 'pen',
    'assign': 'arrow-right-arrow-left',
    'remove': 'user-minus',
    'revoke': 'ban',
    'suspend': 'pause',
    'unsuspend': 'play',

    'delete': 'trash-can',
    'erase': 'eraser',

    'unlock': 'lock-open',
    'lock': 'lock',
    'revert': 'arrow-rotate-left',
}

# Category-specific icons
CATEGORY_ICONS = {
    'access-control': 'key',
    'camera': 'video',
    'door': 'door-open',
    'user': 'user',
    'event': 'calendar',
    'alert': 'bell',
    'sensor': 'sensor',
    'webhook': 'webhook',
    'location': 'map-pin',
    'org': 'building',
    'oauth': 'shield-halved',
    'face-recognition': 'face-smile',
    'badge-reader': 'id-card',
    'doorbell': 'bell',
    'climate': 'temperature-half',
    'export': 'file-export',
    'report': 'chart-line',
    'developer': 'code',
    'integration': 'plug',
    'keypad': 'keyboard',
    'button': 'circle-dot',
    'device': 'microchip',
    'component': 'puzzle-piece',
}

def get_action_from_path(path: str) -> str:
    """Extract action from file path."""
    filename = Path(path).stem
    # Remove category prefix
    parts = filename.split('-', 1)
    if len(parts) > 1:
        action_part = parts[1]
    else:
        action_part = parts[0]

    # Extract first word which is usually the action
    action = re.match(r'^([a-z]+)', action_part.lower())
    if action:
        return action.group(1)
    return 'other'

def get_icon_for_endpoint(category: str, action: str) -> str:
    """Determine the best icon for an endpoint based on category and action."""
    # First check for action-specific icon
    for key, icon in ACTION_ICONS.items():
        if action.startswith(key):
            return icon

    # Fall back to category icon
    for key, icon in CATEGORY_ICONS.items():
        if key in category:
            return icon

    return 'circle-dot'

def update_endpoint_icon(file_path: Path, new_icon: str) -> bool:
    """Update the icon in an endpoint MDX file."""
    try:
        content = file_path.read_text()

        # Update icon in frontmatter
        updated_content = re.sub(
            r'icon: "[^"]*"',
            f'icon: "{new_icon}"',
            content
        )

        if updated_content != content:
            file_path.write_text(updated_content)
            return True
        return False
    except Exception as e:
        print(f"  ⚠️  Error updating {file_path}: {e}")
        return False

def categorize_endpoints(pages: List[str]) -> Dict[str, List[str]]:
    """Categorize endpoints by action type for accordion groups."""
    categories = {
        'Create & Add': [],
        'Get & Find': [],
        'Update & Modify': [],
        'Delete & Remove': [],
        'Other Operations': []
    }

    for page in pages:
        # Get the full filename to check for action keywords
        filename = Path(page).stem.lower()

        # Check for action keywords in the filename
        if any(word in filename for word in ['create', 'add', 'upload', 'generate', 'initiate', 'calibrate']):
            categories['Create & Add'].append(page)
        elif any(word in filename for word in ['get', 'find', 'search', 'list']):
            categories['Get & Find'].append(page)
        elif any(word in filename for word in ['update', 'edit', 'modify', 'assign', 'remove', 'revoke', 'suspend', 'unsuspend']):
            categories['Update & Modify'].append(page)
        elif any(word in filename for word in ['delete', 'erase']):
            categories['Delete & Remove'].append(page)
        else:
            categories['Other Operations'].append(page)

    # Remove empty categories
    return {k: v for k, v in categories.items() if v}

def process_endpoint_icons():
    """Update all endpoint icons based on their action type."""
    print("🎨 Updating endpoint icons...\n")

    updated_count = 0

    for category_dir in sorted(ENDPOINT_DIR.iterdir()):
        if not category_dir.is_dir() or category_dir.name.startswith('.'):
            continue

        category_name = category_dir.name
        print(f"📁 Processing {category_name}...")

        for mdx_file in sorted(category_dir.glob("*.mdx")):
            action = get_action_from_path(str(mdx_file))
            new_icon = get_icon_for_endpoint(category_name, action)

            if update_endpoint_icon(mdx_file, new_icon):
                updated_count += 1

        print(f"   Updated icons for {category_name}")

    print(f"\n✅ Updated icons in {updated_count} endpoint files")

def create_accordion_navigation():
    """Create accordion-style navigation groups for better organization."""
    print("\n📚 Reorganizing navigation with accordion groups...\n")

    # Backup existing docs.json
    with open(DOCS_JSON, 'r') as f:
        docs_data = json.load(f)

    with open(BACKUP_JSON, 'w') as f:
        json.dump(docs_data, f, indent=2)
    print(f"✅ Backed up docs.json to {BACKUP_JSON}")

    # Find the API reference tab
    api_tab = None
    for tab in docs_data['navigation']['tabs']:
        if tab['tab'] == 'API reference':
            api_tab = tab
            break

    if not api_tab:
        print("❌ Could not find 'API reference' tab in docs.json")
        return

    # Keep the introduction group
    intro_group = {
        "group": "API documentation",
        "pages": ["api-reference/introduction"]
    }

    # Process each category group and add accordion subgroups
    new_groups = [intro_group]

    for group in api_tab['groups'][1:]:  # Skip intro group
        category_name = group['group']
        pages = group['pages']

        # If category has many endpoints, organize into accordion groups
        if len(pages) > 10:
            categorized = categorize_endpoints(pages)

            # Create main group with accordion property
            new_group = {
                "group": category_name,
                "pages": []
            }

            # Add sub-groups for each action category
            for action_category, action_pages in categorized.items():
                if action_pages:
                    new_group['pages'].append({
                        "group": action_category,
                        "pages": action_pages
                    })

            new_groups.append(new_group)
        else:
            # Keep small categories as-is
            new_groups.append(group)

    # Update the API reference groups
    api_tab['groups'] = new_groups

    # Write updated docs.json
    with open(DOCS_JSON, 'w') as f:
        json.dump(docs_data, f, indent=2)

    print(f"✅ Updated navigation with accordion groups")

    # Show summary
    print(f"\n📊 Navigation structure:")
    print(f"   Total groups: {len(new_groups)}")
    accordion_count = sum(1 for g in new_groups if any(isinstance(p, dict) for p in g.get('pages', [])))
    print(f"   Groups with accordions: {accordion_count}")

def main():
    """Main execution function."""
    print("🔨 Improving endpoint navigation and icons\n")

    # Update all endpoint icons
    process_endpoint_icons()

    # Create accordion navigation structure
    create_accordion_navigation()

    print("\n🎉 Navigation improvement complete!")
    print("\n💡 Next steps:")
    print("   1. Review docs/docs.json for the new navigation structure")
    print("   2. Refresh your browser to see the updated icons and accordion groups")
    print("   3. If there are issues, restore from docs.json.backup")

if __name__ == "__main__":
    main()
