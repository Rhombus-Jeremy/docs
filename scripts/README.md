# Documentation Automation Scripts

This directory contains automation scripts for maintaining the Rhombus Developer Documentation.

## Scripts Overview

### 🔄 update-openapi.sh
**Purpose**: Manually update the OpenAPI specification from Rhombus API

**Usage**:
```bash
./scripts/update-openapi.sh
```

**Features**:
- Fetches latest spec from `https://api2.rhombussystems.com/api/openapi/public.json`
- Creates automatic backup before updating
- Validates JSON format
- Shows spec statistics (title, version, endpoint count)
- Automatically triggers OpenAPI splitting
- Includes rollback on failure

**Automation**: Also runs nightly via GitHub Actions at 2 AM UTC

---

### 🔪 split-openapi.sh
**Purpose**: Split large OpenAPI spec into smaller, AI-digestible category files

**Usage**:
```bash
./scripts/split-openapi.sh
```

**Features**:
- Splits `openapi.json` into category-specific files
- Extracts base configuration (`_base.json`)
- Creates category index (`_index.json`)
- Generates schema files per category
- Organizes by API tags (Access Control, Camera, Climate, etc.)

**Output**:
- Category files: `api-reference/openapi-split/*.json`
- Schema files: `api-reference/openapi-split/schemas/*-schemas.json`
- README: `api-reference/openapi-split/README.md`

**Why**: Large OpenAPI files (846+ endpoints) can exceed token limits for AI tools. Split files enable focused analysis.

---

### 🤖 update-llms-files.py
**Purpose**: Generate and update AI assistant context files (llms.txt and llms-full.txt)

**Usage**:
```bash
python3 scripts/update-llms-files.py
```

**Features**:
- Analyzes current project structure
- Extracts metadata from `docs.json`
- Counts endpoints by category
- Generates two context files:
  - `llms.txt` - Concise overview (~5.5KB)
  - `llms-full.txt` - Comprehensive reference (~21KB)

**What it analyzes**:
- Navigation structure and tabs
- Endpoint categories and counts
- Color scheme and branding
- File structure and organization
- Development workflows

**Automation**: Runs nightly via GitHub Actions at 3 AM UTC (after OpenAPI updates)

**Manual trigger**: Run when making structural changes to ensure AI assistants have current context

---

## GitHub Actions Workflows

### 📅 update-openapi.yml
**Schedule**: Daily at 2:00 AM UTC
**Triggers**:
- Scheduled (cron)
- Manual dispatch

**Process**:
1. Fetch latest OpenAPI spec
2. Check for changes
3. Commit if changed
4. Create summary report

---

### 📅 update-llms-files.yml
**Schedule**: Daily at 3:00 AM UTC
**Triggers**:
- Scheduled (cron)
- Manual dispatch
- Changes to `docs.json`, `api-reference/`, `implementations/`

**Process**:
1. Run `update-llms-files.py`
2. Check for changes
3. Commit if changed
4. Create summary with diff

---

## Development Workflow

### When to run manually:

**update-openapi.sh**:
- Before making API documentation changes
- When you need the absolute latest API spec
- Testing new endpoints

**split-openapi.sh**:
- After updating OpenAPI spec (usually automatic)
- When regenerating split files

**update-llms-files.py**:
- After structural changes to `docs.json`
- After adding new documentation sections
- Before committing major refactors
- When AI assistants need updated context

### Integration with git workflow:

```bash
# Full documentation update workflow
./scripts/update-openapi.sh      # Update API spec
python3 scripts/update-llms-files.py  # Update AI context
git status                       # Review changes
git add .                        # Stage changes
git commit -m "docs: update API spec and context"
git push                         # Deploy
```

---

## Script Dependencies

### update-openapi.sh
- `curl` - HTTP client
- `jq` - JSON processor
- `bash` - Shell environment

### split-openapi.sh
- `jq` - JSON processor
- `bash` - Shell environment

### update-llms-files.py
- Python 3.11+
- Standard library only (no external dependencies)
- Modules: `json`, `os`, `re`, `pathlib`, `datetime`, `typing`

---

## Output Files

### OpenAPI Files
- `api-reference/openapi.json` - Full specification
- `api-reference/openapi-split/_base.json` - Base config
- `api-reference/openapi-split/_index.json` - Category index
- `api-reference/openapi-split/*.json` - Category files
- `api-reference/openapi-split/schemas/*.json` - Schema definitions

### LLMs Context Files
- `llms.txt` - Concise project overview for AI assistants
- `llms-full.txt` - Comprehensive reference with examples

---

## Troubleshooting

### OpenAPI update fails
```bash
# Check API availability
curl -I https://api2.rhombussystems.com/api/openapi/public.json

# Restore backup if needed
cp api-reference/openapi.json.backup api-reference/openapi.json
```

### Split script fails
```bash
# Verify jq is installed
jq --version

# Check OpenAPI file is valid JSON
jq empty api-reference/openapi.json
```

### LLMs script fails
```bash
# Check Python version
python3 --version  # Should be 3.11+

# Verify docs.json exists and is valid
jq empty docs.json

# Run with verbose output
python3 -v scripts/update-llms-files.py
```

---

## Adding New Scripts

When adding new automation scripts:

1. **Create the script** in `scripts/` directory
2. **Make executable**: `chmod +x scripts/your-script.sh`
3. **Document it** in this README
4. **Add workflow** in `.github/workflows/` if automated
5. **Test manually** before committing
6. **Update CLAUDE.md** with new commands

---

## Best Practices

- ✅ Always test scripts locally before pushing
- ✅ Include error handling and rollback mechanisms
- ✅ Provide clear output and progress indicators
- ✅ Document all dependencies and requirements
- ✅ Use descriptive commit messages for automated commits
- ✅ Check git status after running scripts
- ✅ Keep scripts focused on a single responsibility

---

## Questions or Issues?

- Check script output for error messages
- Review GitHub Actions logs for automated runs
- Consult `CLAUDE.md` for development guidance
- Visit https://rhombus.community for support
