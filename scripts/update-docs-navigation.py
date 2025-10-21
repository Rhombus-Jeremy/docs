#!/usr/bin/env python3
"""
Update docs.json with generated endpoint navigation structure.
Merges the generated navigation while preserving other configuration.
"""

import json
from pathlib import Path

# File paths
DOCS_JSON = Path("docs/docs.json")
NAV_JSON = Path("docs/api-reference/endpoint/_navigation.json")
BACKUP_JSON = Path("docs/docs.json.backup")

def main():
    print("🔄 Updating docs.json with endpoint navigation...\n")

    # Backup existing docs.json
    with open(DOCS_JSON, 'r') as f:
        docs_data = json.load(f)

    with open(BACKUP_JSON, 'w') as f:
        json.dump(docs_data, f, indent=2)
    print(f"✅ Backed up docs.json to {BACKUP_JSON}")

    # Load generated navigation
    with open(NAV_JSON, 'r') as f:
        endpoint_nav = json.load(f)
    print(f"✅ Loaded {len(endpoint_nav)} endpoint categories from _navigation.json")

    # Find the API reference tab
    api_tab = None
    for tab in docs_data['navigation']['tabs']:
        if tab['tab'] == 'API reference':
            api_tab = tab
            break

    if not api_tab:
        print("❌ Could not find 'API reference' tab in docs.json")
        return

    # Keep the introduction group, add all generated endpoints
    intro_group = {
        "group": "API documentation",
        "pages": ["api-reference/introduction"]
    }

    # Update the API reference groups
    api_tab['groups'] = [intro_group] + endpoint_nav

    print(f"✅ Updated API reference tab with {len(endpoint_nav)} endpoint groups")

    # Write updated docs.json
    with open(DOCS_JSON, 'w') as f:
        json.dump(docs_data, f, indent=2)

    print(f"✅ Updated {DOCS_JSON}")
    print(f"\n📊 Navigation structure:")
    print(f"   Total groups: {len(api_tab['groups'])}")

    # Count total pages
    total_pages = sum(len(group['pages']) for group in api_tab['groups'])
    print(f"   Total endpoint pages: {total_pages}")

    print("\n🎉 Navigation update complete!")
    print("\n💡 Next steps:")
    print("   1. Review docs/docs.json")
    print("   2. Run 'mint dev' to preview the documentation")
    print("   3. If there are issues, restore from docs.json.backup")

if __name__ == "__main__":
    main()
