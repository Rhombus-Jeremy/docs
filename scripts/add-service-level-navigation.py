#!/usr/bin/env python3
"""
Add top-level service groupings to organize API categories.
Groups 61+ categories into logical service sections for better navigation.
"""

import json
from pathlib import Path

# Configuration
DOCS_JSON = Path("docs/docs.json")
BACKUP_JSON = Path("docs/docs.json.backup")

# Top-level service groupings
SERVICE_GROUPS = {
    "Core Services": [
        "Access Control",
        "Camera",
        "Door",
        "Door Controller",
        "Doorbell Camera",
        "User",
        "Users",
        "Badge Reader",
        "Sensor",
        "Climate",
        "Button",
        "Relay",
        "Media Device",
    ],
    "Events & Monitoring": [
        "Event",
        "Events",
        "Event Search",
        "Alert Monitoring",
        "Face Recognition Event",
        "Face Recognition Matchmaker",
        "Face Recognition Person",
        "Proximity",
        "Occupancy",
    ],
    "Integrations": [
        "Access Control Integrations",
        "Service Management Integrations",
        "Incident Management Integrations",
        "IoT Integrations",
        "Storage Integrations",
        "Webhook Integrations",
        "Org Integrations",
        "Integrations",
    ],
    "Organization & Management": [
        "Organization",
        "Org",
        "Location",
        "Locations",
        "Customer",
        "Partner",
        "License",
        "Permission",
        "User Metadata",
    ],
    "Security & Access": [
        "OAuth",
        "Alarm Monitoring Keypad",
        "Guest Management Kiosk",
        "Lockdown Plan",
        "RapidSOS",
    ],
    "Media & Video": [
        "Video",
        "Export",
        "AudioGateway",
        "AudioPlayback",
        "TvOS Config",
    ],
    "Automation & Rules": [
        "Rules",
        "Rules Records",
        "Schedule",
        "Policies",
        "Policy",
    ],
    "Device Management": [
        "Device Config",
        "Component",
        "Components",
        "BLE",
    ],
    "Data & Reporting": [
        "Report",
        "Reports",
        "Search",
        "Logistics",
        "Vehicle",
        "Vehicles",
    ],
    "Developer & System": [
        "Developer",
        "Feature",
        "Help",
        "Upload",
    ],
}

def categorize_group(group_name: str) -> str:
    """Determine which service category a group belongs to."""
    for service, groups in SERVICE_GROUPS.items():
        if group_name in groups:
            return service
    return "Other Services"

def organize_with_service_groups():
    """Add top-level service groupings to the API reference navigation."""
    print("🎯 Adding top-level service groupings...\n")

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

    # Keep the introduction group separate
    intro_group = api_tab['groups'][0]
    existing_groups = api_tab['groups'][1:]

    # Organize groups into service categories
    service_structure = {}
    uncategorized = []

    for group in existing_groups:
        group_name = group['group']
        service = categorize_group(group_name)

        if service == "Other Services":
            uncategorized.append(group)
        else:
            if service not in service_structure:
                service_structure[service] = []
            service_structure[service].append(group)

    # Build new navigation structure with service-level groups
    new_groups = [intro_group]

    # Add each service group with its API categories as nested groups
    for service_name in SERVICE_GROUPS.keys():
        if service_name in service_structure:
            categories = service_structure[service_name]

            # Create top-level service group
            service_group = {
                "group": service_name,
                "pages": categories  # Nested groups
            }
            new_groups.append(service_group)

    # Add any uncategorized groups at the end
    if uncategorized:
        other_service_group = {
            "group": "Other Services",
            "pages": uncategorized
        }
        new_groups.append(other_service_group)

    # Update the API reference groups
    api_tab['groups'] = new_groups

    # Write updated docs.json
    with open(DOCS_JSON, 'w') as f:
        json.dump(docs_data, f, indent=2)

    print(f"✅ Updated navigation with service-level groupings")

    # Show summary
    print(f"\n📊 Service-level navigation structure:")
    print(f"   Total service groups: {len([g for g in new_groups if g['group'] != 'API documentation'])}")

    for group in new_groups[1:]:  # Skip intro
        service_name = group['group']
        category_count = len(group['pages'])
        print(f"   {service_name}: {category_count} categories")

    # Count total endpoints
    total_endpoints = 0
    for service_group in new_groups[1:]:
        for category in service_group['pages']:
            if isinstance(category, dict) and 'pages' in category:
                # This is a category with accordion sub-groups
                for item in category['pages']:
                    if isinstance(item, dict) and 'pages' in item:
                        # This is an accordion sub-group
                        total_endpoints += len(item['pages'])
                    elif isinstance(item, str):
                        # This is a direct endpoint page
                        total_endpoints += 1

    print(f"\n   Total endpoints: {total_endpoints}")

def main():
    """Main execution function."""
    print("🔨 Adding service-level navigation groupings\n")

    organize_with_service_groups()

    print("\n🎉 Service-level navigation complete!")
    print("\n💡 Next steps:")
    print("   1. Refresh your browser to see the new service-level organization")
    print("   2. Navigation now has 3 levels: Service → Category → Action Type")
    print("   3. If there are issues, restore from docs.json.backup")

if __name__ == "__main__":
    main()
