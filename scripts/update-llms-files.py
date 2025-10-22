#!/usr/bin/env python3
"""
Update llms.txt and llms-full.txt with current project structure and metadata.

This script analyzes the project structure, documentation files, and configuration
to generate comprehensive context files for AI assistants.
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple


class LLMSFileGenerator:
    """Generates llms.txt and llms-full.txt files from project analysis."""

    def __init__(self, docs_dir: str = "docs"):
        self.docs_dir = Path(docs_dir)
        self.base_dir = self.docs_dir if self.docs_dir.exists() else Path(".")

    def count_endpoints_in_nav(self, nav_data: dict) -> Dict[str, int]:
        """Count endpoints by category from navigation structure."""
        endpoint_counts = {}

        def traverse(obj, current_category=None):
            if isinstance(obj, dict):
                # Check if this is a group with a name
                if "group" in obj:
                    current_category = obj["group"]
                    endpoint_counts[current_category] = 0

                # Check if this is a pages array
                if "pages" in obj and isinstance(obj["pages"], list):
                    for page in obj["pages"]:
                        if isinstance(page, str) and current_category:
                            endpoint_counts[current_category] += 1
                        elif isinstance(page, dict):
                            traverse(page, current_category)

                # Traverse all dict values
                for value in obj.values():
                    traverse(value, current_category)

            elif isinstance(obj, list):
                for item in obj:
                    traverse(item, current_category)

        traverse(nav_data)
        return endpoint_counts

    def analyze_docs_json(self) -> Dict:
        """Analyze docs.json for configuration and structure."""
        docs_json_path = self.base_dir / "docs.json"

        if not docs_json_path.exists():
            return {
                "total_endpoints": 0,
                "categories": [],
                "theme": {},
                "navigation_tabs": []
            }

        with open(docs_json_path, 'r') as f:
            config = json.load(f)

        # Count endpoints from navigation
        endpoint_counts = self.count_endpoints_in_nav(config.get("navigation", {}))

        # Extract navigation tabs
        tabs = []
        if "navigation" in config and "tabs" in config["navigation"]:
            for tab in config["navigation"]["tabs"]:
                tab_info = {"name": tab.get("tab", "Unknown")}
                if "groups" in tab:
                    tab_info["groups"] = [
                        g.get("group") if isinstance(g, dict) else str(g)
                        for g in tab["groups"]
                    ]
                tabs.append(tab_info)

        return {
            "name": config.get("name", "Rhombus Developer Documentation"),
            "theme": config.get("theme", "mint"),
            "colors": config.get("colors", {}),
            "total_endpoints": sum(endpoint_counts.values()),
            "endpoint_categories": endpoint_counts,
            "navigation_tabs": tabs
        }

    def count_files_by_type(self) -> Dict[str, int]:
        """Count documentation files by type."""
        counts = {
            "mdx": 0,
            "json": 0,
            "scripts": 0,
            "workflows": 0
        }

        # Count MDX files
        if (self.base_dir / "api-reference" / "endpoint").exists():
            counts["mdx"] = len(list((self.base_dir / "api-reference" / "endpoint").rglob("*.mdx")))

        # Count split OpenAPI files
        if (self.base_dir / "api-reference" / "openapi-split").exists():
            split_dir = self.base_dir / "api-reference" / "openapi-split"
            counts["json"] = len([f for f in split_dir.glob("*.json") if not f.name.startswith("_")])

        # Count scripts
        if (self.base_dir / "scripts").exists():
            counts["scripts"] = len(list((self.base_dir / "scripts").glob("*.*")))

        # Count workflows
        if (self.base_dir / ".github" / "workflows").exists():
            counts["workflows"] = len(list((self.base_dir / ".github" / "workflows").glob("*.yml")))

        return counts

    def get_api_categories(self) -> List[Tuple[str, int]]:
        """Get API categories and their endpoint counts."""
        endpoint_dir = self.base_dir / "api-reference" / "endpoint"

        if not endpoint_dir.exists():
            return []

        categories = []
        for category_dir in sorted(endpoint_dir.iterdir()):
            if category_dir.is_dir():
                count = len(list(category_dir.glob("*.mdx")))
                if count > 0:
                    # Format category name nicely
                    name = category_dir.name.replace("-", " ").title()
                    categories.append((name, count))

        return categories

    def read_frontmatter(self, file_path: Path) -> Dict:
        """Extract YAML frontmatter from MDX file."""
        try:
            with open(file_path, 'r') as f:
                content = f.read()

            # Extract frontmatter between --- markers
            match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if match:
                frontmatter = {}
                for line in match.group(1).split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        frontmatter[key.strip()] = value.strip().strip('"\'')
                return frontmatter
        except Exception:
            pass
        return {}

    def generate_llms_txt(self) -> str:
        """Generate concise llms.txt content."""
        config = self.analyze_docs_json()
        file_counts = self.count_files_by_type()

        content = f"""# Rhombus Developer Documentation

This is a Mintlify documentation site for Rhombus security platform API documentation. The project provides comprehensive developer resources for integrating with Rhombus cameras, sensors, access control systems, and analytics.

## Project Overview

**Platform**: Mintlify documentation framework
**Purpose**: Developer documentation for Rhombus REST API
**Target Audience**: Developers building integrations with Rhombus security platform
**API Coverage**: {config['total_endpoints']}+ endpoints across cameras, access control, environmental monitoring, events, and integrations

## Key Features

- **Comprehensive API Reference**: Auto-generated from OpenAPI specification
- **Interactive Documentation**: Mintlify components for rich user experience
- **Automated Updates**: Nightly sync with production API specification
- **Developer Resources**: Quick start guides, code examples, best practices
- **Multi-language Support**: Examples in cURL, Python, JavaScript, Go

## Architecture

### Core Structure
```
├── docs.json                 # Mintlify configuration
├── index.mdx                 # Homepage with API overview
├── quickstart.mdx           # Getting started guide
├── development.mdx          # Local development setup
├── api-reference/           # API documentation
│   ├── README.md           # API reference overview
│   ├── openapi.json        # Rhombus OpenAPI spec ({config['total_endpoints']} endpoints)
│   └── endpoint/           # Generated endpoint documentation
├── implementations/         # Implementation examples
├── scripts/                # Automation scripts
└── .github/workflows/      # CI/CD automation
```

### Navigation Structure
"""

        # Add navigation tabs
        for tab in config['navigation_tabs']:
            content += f"- **{tab['name']} Tab**: "
            if 'groups' in tab:
                content += ", ".join(tab['groups'])
            content += "\n"

        content += f"""
## Technical Implementation

### API Integration
- **Base URL**: `https://api2.rhombussystems.com`
- **Authentication**: API key via `x-auth-apikey` header
- **Rate Limits**: 1000 requests/hour, 100 requests/minute burst
- **OpenAPI Source**: `https://api2.rhombussystems.com/api/openapi/public.json`

### Automation
- **Nightly Updates**: GitHub Actions workflow updates OpenAPI spec at 2 AM UTC
- **Manual Updates**: `scripts/update-openapi.sh` for on-demand updates
- **Validation**: JSON validation and change detection

### Development Workflow
```bash
# Install Mintlify CLI
npm i -g mint

# Local development
mint dev                    # Runs on localhost:3000
mint dev --port 3333       # Custom port

# Maintenance
mint update                 # Update CLI
mint broken-links          # Validate links
./scripts/update-openapi.sh # Update API spec
```

## Content Guidelines

### File Structure
All MDX files require YAML frontmatter:
```yaml
---
title: "Page Title"
description: "Brief description"
icon: "icon-name"          # Optional
---
```

### Mintlify Components
- **Callouts**: `<Note>`, `<Tip>`, `<Warning>`, `<Info>`, `<Check>`
- **Structure**: `<Steps>`, `<Tabs>`, `<AccordionGroup>`, `<Card>`, `<CardGroup>`
- **Code**: `<CodeGroup>`, `<RequestExample>`, `<ResponseExample>`
- **API**: `<ParamField>`, `<ResponseField>`, `<Expandable>`
- **Media**: `<Frame>` for images, `<video>`, `<iframe>`

## API Categories

### Core Services
"""

        # Add top API categories
        categories = self.get_api_categories()
        core_services = [cat for cat in categories if cat[1] > 10][:5]
        for name, count in core_services:
            content += f"- **{name}**: {count} endpoints\n"

        content += f"""
### Events & Monitoring
"""
        event_categories = [cat for cat in categories if any(term in cat[0].lower() for term in ['event', 'alert', 'face', 'occupancy'])]
        for name, count in event_categories[:4]:
            content += f"- **{name}**: {count} endpoints\n"

        content += f"""
### Integrations
"""
        integration_categories = [cat for cat in categories if 'integration' in cat[0].lower()][:2]
        for name, count in integration_categories:
            content += f"- **{name}**: {count} endpoints\n"

        colors = config.get('colors', {})
        content += f"""
## Branding & Theme

### Color Scheme (2024 Rebrand)
- **Primary**: {colors.get('primary', '#2563EB')} (blue)
- **Light**: {colors.get('light', '#60A5FA')} (light blue)
- **Dark**: {colors.get('dark', '#1D4ED8')} (dark blue)

### Brand Identity
- Company name: "Rhombus" (dropped "Systems" in 2024 rebrand)
- Focus on trust, integrity, friendliness, and innovation
- Modern blue gradient replacing previous green theme

## Development Environment

### Prerequisites
- Node.js version 19 or higher
- Mintlify CLI installed globally
- Access to Rhombus Console for API key generation

### Local Development
1. Clone repository
2. Install Mintlify CLI: `npm i -g mint`
3. Run development server: `mint dev`
4. Access at `http://localhost:3000`

### Deployment
- Automatic deployment via Mintlify GitHub app integration
- Changes deploy to production on push to default branch
- No build step required - Mintlify handles compilation

## Key Files

### Configuration
- `docs.json`: Mintlify site configuration with navigation structure
- `.github/workflows/update-openapi.yml`: Automated API spec updates
- `scripts/update-openapi.sh`: Manual API spec update script

### Documentation
- `index.mdx`: Homepage with API overview and getting started
- `quickstart.mdx`: 5-minute quick start guide with code examples
- `development.mdx`: Local development setup instructions
- `api-reference/README.md`: API reference documentation process

### Assets
- `favicon.svg`: Site favicon
- `logo/`: Brand logos (dark/light variants)
- `images/`: Documentation screenshots and assets

This project serves as the primary developer resource for Rhombus API integration, providing comprehensive documentation, interactive examples, and automated maintenance of API specifications.
"""

        return content

    def generate_llms_full_txt(self) -> str:
        """Generate comprehensive llms-full.txt content."""
        config = self.analyze_docs_json()
        categories = self.get_api_categories()

        content = f"""# Rhombus Developer Documentation - Complete Reference

This is the comprehensive reference for the Rhombus Developer Documentation project, a Mintlify-based documentation site providing complete API documentation for the Rhombus security platform.

## Project Overview

### Mission & Purpose
The Rhombus Developer Documentation serves as the primary resource for developers integrating with Rhombus security infrastructure. It provides comprehensive API documentation, interactive examples, and development resources for building applications that leverage Rhombus cameras, sensors, access control systems, and analytics.

### Target Audience
- **API Developers**: Building integrations with Rhombus security platform
- **System Integrators**: Connecting Rhombus with existing security systems
- **Enterprise Developers**: Creating custom security applications
- **Partner Developers**: Building solutions on the Rhombus platform

### Platform Details
- **Framework**: Mintlify documentation platform
- **Language**: MDX (Markdown with JSX components)
- **Deployment**: Automatic via Mintlify GitHub app integration
- **API Coverage**: {config['total_endpoints']}+ endpoints across multiple service categories
- **Update Frequency**: Nightly automated sync with production API

## Technical Architecture

### Project Structure
```
docs/
├── .github/
│   └── workflows/
│       ├── update-openapi.yml          # Nightly API spec updates
│       └── update-llms-files.yml       # LLMs context file updates
├── .windsurf/
│   └── rules.md                        # Windsurf AI editor rules
├── api-reference/
│   ├── endpoint/                       # Generated API endpoint docs
"""

        # Add detailed category breakdown
        for name, count in sorted(categories, key=lambda x: x[1], reverse=True):
            slug = name.lower().replace(" ", "-")
            content += f"│   │   ├── {slug}/{'':20} # {name} endpoints ({count})\n"

        content += f"""│   ├── openapi-split/                 # Split OpenAPI spec files
│   │   ├── schemas/                   # API schema definitions
│   │   ├── _base.json                 # Base OpenAPI configuration
│   │   └── _index.json                # Category index
│   ├── README.md                      # API reference documentation
│   └── openapi.json                   # Complete OpenAPI specification
├── implementations/                   # Implementation examples
│   ├── video-player.mdx              # Video streaming implementation
│   ├── advanced-implementation.mdx   # Advanced patterns
│   └── webhook-listener.mdx          # Webhook integration
├── low-code-no-code/                 # No-code integration guides
│   └── zapier.mdx                    # Zapier integration
├── scripts/                          # Automation scripts
│   ├── update-openapi.sh             # Fetch & update OpenAPI spec
│   ├── split-openapi.sh              # Split spec into category files
│   └── update-llms-files.py          # Update LLMs context files
├── logo/                             # Brand assets
│   ├── dark.svg                      # Dark theme logo
│   └── light.svg                     # Light theme logo
├── images/                           # Documentation assets
├── .gitignore                        # Git ignore patterns
├── CLAUDE.md                         # Claude AI assistant guidance
├── LICENSE                           # Project license
├── README.md                         # Project overview
├── docs.json                         # Mintlify configuration
├── favicon.svg                       # Site favicon
├── index.mdx                         # Homepage
├── quickstart.mdx                    # Quick start guide
├── llms.txt                          # Concise AI context
└── llms-full.txt                     # Comprehensive AI context
```

### Configuration Details

#### Mintlify Configuration (`docs.json`)
```json
{{
  "$schema": "https://mintlify.com/docs.json",
  "theme": "{config['theme']}",
  "name": "{config['name']}",
  "colors": {json.dumps(config.get('colors', {}), indent=4)},
  "favicon": "/favicon.svg",
  "navigation": {{
    "tabs": [
"""

        for tab in config['navigation_tabs']:
            content += f"""      {{
        "tab": "{tab['name']}",
        "groups": {json.dumps(tab.get('groups', []))}
      }},
"""

        content += """    ]
  }
}
```

## API Documentation Structure

### Endpoint Distribution
"""

        # Group categories
        core_services = []
        events_monitoring = []
        integrations = []
        devices = []

        for name, count in categories:
            lower_name = name.lower()
            if any(term in lower_name for term in ['integration', 'alarm']):
                integrations.append((name, count))
            elif any(term in lower_name for term in ['event', 'alert', 'face', 'occupancy', 'proximity']):
                events_monitoring.append((name, count))
            elif any(term in lower_name for term in ['button', 'relay', 'sensor', 'badge', 'keypad', 'doorbell']):
                devices.append((name, count))
            else:
                core_services.append((name, count))

        if core_services:
            content += "\n### Core Services\n"
            for name, count in sorted(core_services, key=lambda x: x[1], reverse=True):
                content += f"- **{name}**: {count} endpoints\n"

        if events_monitoring:
            content += "\n### Events & Monitoring\n"
            for name, count in sorted(events_monitoring, key=lambda x: x[1], reverse=True):
                content += f"- **{name}**: {count} endpoints\n"

        if integrations:
            content += "\n### Integrations\n"
            for name, count in sorted(integrations, key=lambda x: x[1], reverse=True):
                content += f"- **{name}**: {count} endpoints\n"

        if devices:
            content += "\n### Device Management\n"
            for name, count in sorted(devices, key=lambda x: x[1], reverse=True):
                content += f"- **{name}**: {count} endpoints\n"

        content += f"""
## Development Workflow

### Local Development Setup
```bash
# Prerequisites
# - Node.js 19+
# - Git access to repository

# 1. Install Mintlify CLI
npm i -g mint

# 2. Clone and navigate to project
git clone [repository-url]
cd Developer-Documentation-Mintlify/docs

# 3. Start development server
mint dev                    # Default port 3000
mint dev --port 3333       # Custom port

# 4. Access local preview
open http://localhost:3000
```

### Maintenance Commands
```bash
# Update Mintlify CLI
mint update

# Validate documentation links
mint broken-links

# Update API specification manually
./scripts/update-openapi.sh

# Update LLMs context files
python3 scripts/update-llms-files.py
```

### Automated Workflows

#### Nightly OpenAPI Updates
**File**: `.github/workflows/update-openapi.yml`
**Schedule**: Daily at 2:00 AM UTC
**Process**:
1. Fetch latest OpenAPI spec from `https://api2.rhombussystems.com/api/openapi/public.json`
2. Compare with existing specification
3. Commit changes if updates detected
4. Split into category files for AI processing
5. Generate workflow summary

#### LLMs Context Updates
**File**: `.github/workflows/update-llms-files.yml`
**Schedule**: Daily at 3:00 AM UTC (after OpenAPI updates)
**Process**:
1. Analyze current project structure
2. Extract configuration and metadata
3. Generate updated llms.txt (concise)
4. Generate updated llms-full.txt (comprehensive)
5. Commit changes if content differs

## Content Creation Guidelines

### MDX File Structure
Every documentation page must include YAML frontmatter:
```yaml
---
title: "Descriptive Page Title"
description: "Brief, informative description for SEO and navigation"
icon: "icon-name"                    # Optional Mintlify icon
---

# Page Content
Content goes here using MDX syntax...
```

### Mintlify Component Library

#### Callout Components
```mdx
<Note>General information or context</Note>
<Tip>Helpful suggestions or best practices</Tip>
<Warning>Important cautions or potential issues</Warning>
<Info>Additional context or background information</Info>
<Check>Confirmation or success indicators</Check>
```

#### Structural Components
```mdx
<!-- Step-by-step processes -->
<Steps>
  <Step title="First Step">Content</Step>
  <Step title="Second Step">Content</Step>
</Steps>

<!-- Tabbed content -->
<Tabs>
  <Tab title="Tab 1">Content</Tab>
  <Tab title="Tab 2">Content</Tab>
</Tabs>

<!-- Collapsible sections -->
<AccordionGroup>
  <Accordion title="Section Title" icon="icon-name">
    Content
  </Accordion>
</AccordionGroup>

<!-- Card layouts -->
<CardGroup cols={{2}}>
  <Card title="Card Title" icon="icon-name" href="/link">
    Card description
  </Card>
</CardGroup>
```

#### Code Examples
```mdx
<!-- Multi-language code examples -->
<CodeGroup>
  ```bash cURL
  curl -X POST "https://api2.rhombussystems.com/api/endpoint" \\
    -H "x-auth-apikey: YOUR_API_KEY" \\
    -H "Content-Type: application/json" \\
    -d '{{"key": "value"}}'
  ```

  ```python Python
  import requests
  headers = {{"x-auth-apikey": "YOUR_API_KEY"}}
  response = requests.post(
      "https://api2.rhombussystems.com/api/endpoint",
      headers=headers,
      json={{"key": "value"}}
  )
  ```

  ```javascript JavaScript
  const response = await fetch('https://api2.rhombussystems.com/api/endpoint', {{
    method: 'POST',
    headers: {{
      'x-auth-apikey': 'YOUR_API_KEY',
      'Content-Type': 'application/json'
    }},
    body: JSON.stringify({{key: 'value'}})
  }});
  ```
</CodeGroup>
```

#### API Documentation Components
```mdx
<!-- Parameter documentation -->
<ParamField path="parameter_name" type="string" required>
  Parameter description
</ParamField>

<!-- Response field documentation -->
<ResponseField name="field_name" type="object">
  Response field description
</ResponseField>

<!-- Expandable sections -->
<Expandable title="Advanced Options">
  Additional configuration details
</Expandable>
```

#### Media Components
```mdx
<!-- Images (always wrap in Frame) -->
<Frame>
  <img src="/images/example.png" alt="Description" />
</Frame>

<!-- Videos -->
<video controls>
  <source src="/videos/demo.mp4" type="video/mp4" />
</video>

<!-- Embedded content -->
<iframe src="https://example.com" width="100%" height="400px" />
```

## API Integration Details

### Authentication System
```http
# All API requests require authentication header
x-auth-apikey: YOUR_API_KEY
x-auth-scheme: api-token

# Base URL for all endpoints
https://api2.rhombussystems.com
```

### Rate Limiting
- **Standard Limit**: 1000 requests per hour
- **Burst Limit**: 100 requests per minute
- **Headers**: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

### Error Handling
```json
{{
  "error": {{
    "code": "ERROR_CODE",
    "message": "Human-readable error message",
    "details": "Additional context or resolution steps"
  }}
}}
```

### Common HTTP Status Codes
- **200**: Success
- **400**: Bad Request (invalid parameters)
- **401**: Unauthorized (invalid API key)
- **403**: Forbidden (insufficient permissions)
- **404**: Not Found (resource doesn't exist)
- **429**: Too Many Requests (rate limit exceeded)
- **500**: Internal Server Error

## Brand Guidelines & Styling

### 2024 Rebrand Implementation
**Previous Branding** (Pre-2024):
- Company: "Rhombus Systems"
- Colors: Green theme (#16A34A primary)

**Current Branding** (2024+):
- Company: "Rhombus" (dropped "Systems")
- Colors: Blue theme ({config.get('colors', {}).get('primary', '#2563EB')} primary)
- Values: Trust, integrity, friendliness, innovation

### Color Palette
```css
:root {{
  --primary: {config.get('colors', {}).get('primary', '#2563EB')};      /* Blue */
  --light: {config.get('colors', {}).get('light', '#60A5FA')};       /* Light Blue */
  --dark: {config.get('colors', {}).get('dark', '#1D4ED8')};        /* Dark Blue */
}}
```

### Typography & Iconography
- **Icons**: Mintlify icon library
- **Fonts**: System fonts optimized for readability
- **Logo**: SVG format with dark/light variants

## File Management & Assets

### Image Guidelines
- **Format**: PNG for screenshots, SVG for logos/icons
- **Location**: `/images/` directory
- **Usage**: Always wrap in `<Frame>` component
- **Naming**: Descriptive, kebab-case filenames

### Logo Assets
- **Dark Theme**: `/logo/dark.svg`
- **Light Theme**: `/logo/light.svg`
- **Favicon**: `/favicon.svg`

### Documentation Assets
- **Screenshots**: Deployment confirmations, UI examples
- **Diagrams**: Architecture and workflow illustrations
- **Hero Images**: Landing page visuals (dark/light variants)

## Deployment & Publishing

### Automatic Deployment
- **Trigger**: Push to default branch
- **Platform**: Mintlify hosting infrastructure
- **Process**: Automatic build and deployment via GitHub app
- **URL**: Custom domain configured in Mintlify dashboard

### Deployment Validation
```bash
# Local validation before deployment
mint dev                    # Test locally
mint broken-links          # Validate all links
git add . && git commit    # Stage changes
git push origin main       # Deploy to production
```

### Monitoring & Maintenance
- **Analytics**: Built-in Mintlify analytics
- **Performance**: Automatic optimization and CDN
- **Updates**: Nightly API spec synchronization
- **Backups**: Git version control and automatic backups

## Integration Examples & Use Cases

### Common Integration Patterns

#### Live Video Streaming
```javascript
// 1. Get camera list
const cameras = await fetch('/api/camera/getMinimalCameraStateList', {{
  headers: {{'x-auth-apikey': API_KEY}}
}});

// 2. Create shared stream
const stream = await fetch('/api/camera/createSharedLiveVideoStream', {{
  method: 'POST',
  headers: {{'x-auth-apikey': API_KEY}},
  body: JSON.stringify({{cameraUuid: cameraId}})
}});

// 3. Use stream URL in video player
const streamUrl = stream.streamUrl;
```

#### Event-Driven Workflows
```python
# Real-time event monitoring
import requests

def monitor_events():
    response = requests.post(
        'https://api2.rhombussystems.com/api/event/getPolicyAlertsV2',
        headers={{'x-auth-apikey': API_KEY}},
        json={{'limit': 10, 'includeResolved': False}}
    )

    for event in response.json():
        process_security_event(event)
```

#### Access Management Integration
```python
# Sync users with HR system
def sync_user_access():
    # Create user in Rhombus
    user_data = {{
        'firstName': 'John',
        'lastName': 'Doe',
        'email': 'john.doe@company.com'
    }}

    response = requests.post(
        'https://api2.rhombussystems.com/api/user/createUser',
        headers={{'x-auth-apikey': API_KEY}},
        json=user_data
    )

    # Assign access credentials
    if response.status_code == 200:
        assign_access_credentials(response.json()['userUuid'])
```

## Support & Community Resources

### Developer Resources
- **API Reference**: Complete endpoint documentation
- **OpenAPI Specification**: Machine-readable API spec
- **Code Examples**: Multi-language integration samples
- **Implementation Guides**: Video player, webhooks, access control

### Community & Support
- **Developer Community**: https://rhombus.community
- **Technical Support**: https://rhombus.com/support
- **API Console**: https://console.rhombussystems.com
- **Documentation Updates**: Automatic nightly synchronization

### Troubleshooting Resources
- **Error Codes**: Comprehensive error documentation
- **Rate Limiting**: Usage monitoring and optimization
- **Authentication**: API key management and security
- **Integration Guides**: Step-by-step implementation examples

## Project Statistics

**Last Updated**: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}
**Total Endpoints**: {config['total_endpoints']}+
**Total Categories**: {len(categories)}
**Documentation Files**: Generated from OpenAPI specification
**Update Frequency**: Nightly automated synchronization

This comprehensive documentation serves as the authoritative resource for developers building on the Rhombus security platform, providing everything needed for successful API integration and application development.
"""

        return content

    def write_files(self):
        """Generate and write both llms.txt files."""
        print("🔄 Generating LLMs context files...")

        # Generate llms.txt
        print("📝 Generating llms.txt (concise version)...")
        llms_content = self.generate_llms_txt()
        llms_path = self.base_dir / "llms.txt"
        with open(llms_path, 'w') as f:
            f.write(llms_content)
        print(f"✅ Written: {llms_path} ({len(llms_content)} chars)")

        # Generate llms-full.txt
        print("📝 Generating llms-full.txt (comprehensive version)...")
        llms_full_content = self.generate_llms_full_txt()
        llms_full_path = self.base_dir / "llms-full.txt"
        with open(llms_full_path, 'w') as f:
            f.write(llms_full_content)
        print(f"✅ Written: {llms_full_path} ({len(llms_full_content)} chars)")

        print("\n🎉 LLMs context files updated successfully!")
        return True


def main():
    """Main execution function."""
    print("=" * 60)
    print("Rhombus Developer Documentation - LLMs File Generator")
    print("=" * 60)
    print()

    # Determine the docs directory
    if Path("docs").exists():
        docs_dir = "docs"
    else:
        docs_dir = "."

    print(f"📂 Working directory: {Path(docs_dir).absolute()}")
    print()

    # Generate files
    generator = LLMSFileGenerator(docs_dir)
    success = generator.write_files()

    if success:
        print("\n✨ All done! Files are ready for commit.")
        return 0
    else:
        print("\n❌ Failed to generate files.")
        return 1


if __name__ == "__main__":
    exit(main())
