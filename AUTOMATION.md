# Documentation Automation Guide

This document describes the automated workflows that keep the Rhombus Developer Documentation current and accurate.

## Overview

The documentation repository uses several automated workflows to maintain synchronization with the Rhombus API and provide up-to-date context for AI assistants.

## Automated Workflows

### 1. OpenAPI Specification Updates

**File**: `.github/workflows/update-openapi.yml`
**Schedule**: Daily at 2:00 AM UTC
**Purpose**: Keep API documentation synchronized with production API

#### What it does:
1. Fetches latest OpenAPI spec from `https://api2.rhombussystems.com/api/openapi/public.json`
2. Validates JSON format
3. Compares with existing specification
4. Commits changes if updates detected
5. Automatically triggers split process

#### Manual trigger:
```bash
./scripts/update-openapi.sh
```

#### Outputs:
- `api-reference/openapi.json` - Updated full specification
- `api-reference/openapi-split/*.json` - Category-specific files
- `api-reference/openapi-split/schemas/*.json` - Schema definitions

---

### 2. LLMs Context File Updates

**File**: `.github/workflows/update-llms-files.yml`
**Schedule**: Daily at 3:00 AM UTC (after OpenAPI updates)
**Purpose**: Provide current project context for AI assistants

#### What it does:
1. Analyzes current project structure
2. Extracts configuration from `docs.json`
3. Counts endpoints by category
4. Generates two context files:
   - `llms.txt` - Concise overview (~5.5KB)
   - `llms-full.txt` - Comprehensive reference (~21KB)
5. Commits changes if content differs

#### Triggered by changes to:
- `docs/docs.json` - Configuration changes
- `docs/api-reference/**` - API documentation updates
- `docs/implementations/**` - Implementation example changes
- Workflow/script modifications

#### Manual trigger:
```bash
python3 scripts/update-llms-files.py
```

#### Outputs:
- `llms.txt` - Quick reference for AI assistants
- `llms-full.txt` - Detailed project documentation

---

## Workflow Schedule

```
┌─────────────────────────────────────────────────┐
│  Daily Automation Schedule (UTC)               │
├─────────────────────────────────────────────────┤
│                                                 │
│  2:00 AM  ▶  Update OpenAPI Spec               │
│              ├─ Fetch from API                  │
│              ├─ Validate JSON                   │
│              ├─ Split into categories           │
│              └─ Commit changes                  │
│                                                 │
│  3:00 AM  ▶  Update LLMs Context Files         │
│              ├─ Analyze structure               │
│              ├─ Generate llms.txt               │
│              ├─ Generate llms-full.txt          │
│              └─ Commit changes                  │
│                                                 │
└─────────────────────────────────────────────────┘
```

## File Purposes

### llms.txt
**Size**: ~5.5KB
**Purpose**: Quick reference for AI assistants

**Contains**:
- Project overview and mission
- Technology stack (Mintlify, MDX)
- Essential development commands
- API integration details
- Component library reference
- Core service categories
- Branding guidelines

**Best for**:
- Initial context loading
- Quick reference queries
- Token-constrained scenarios

---

### llms-full.txt
**Size**: ~21KB
**Purpose**: Comprehensive project reference

**Contains**:
- Everything in llms.txt, plus:
- Detailed project structure tree
- Complete endpoint distribution
- Code examples in multiple languages
- Comprehensive component documentation
- Integration patterns and workflows
- Deployment procedures
- Troubleshooting guides

**Best for**:
- Complex implementation questions
- Architecture discussions
- Detailed technical guidance
- Complete project understanding

---

## Manual Updates

### When to run manually:

#### Update OpenAPI spec:
```bash
./scripts/update-openapi.sh
```

**When**:
- Before documenting new API features
- Testing latest endpoint changes
- Verifying API modifications

#### Update LLMs context:
```bash
python3 scripts/update-llms-files.py
```

**When**:
- After modifying `docs.json` navigation
- After structural refactoring
- Before major commits
- When AI assistants need fresh context

#### Complete update workflow:
```bash
# 1. Update OpenAPI spec
./scripts/update-openapi.sh

# 2. Update AI context
python3 scripts/update-llms-files.py

# 3. Review changes
git status
git diff llms.txt llms-full.txt

# 4. Commit
git add .
git commit -m "docs: update API spec and AI context"
git push
```

---

## Monitoring Automation

### GitHub Actions Dashboard
View workflow runs: `https://github.com/[org]/[repo]/actions`

### Check latest runs:
```bash
# View recent workflow runs
gh run list --workflow=update-openapi.yml --limit 5
gh run list --workflow=update-llms-files.yml --limit 5

# View specific run details
gh run view [run-id]
```

### Workflow summaries:
Each workflow creates a summary showing:
- ✅ Success/failure status
- 📅 Execution timestamp
- 📝 Files modified
- 📊 Changes detected
- 🔗 Relevant links

---

## Troubleshooting

### OpenAPI workflow fails

**Check API availability**:
```bash
curl -I https://api2.rhombussystems.com/api/openapi/public.json
```

**Restore from backup**:
```bash
cp api-reference/openapi.json.backup api-reference/openapi.json
```

**Validate local spec**:
```bash
jq empty api-reference/openapi.json
```

---

### LLMs workflow fails

**Check Python version**:
```bash
python3 --version  # Requires 3.11+
```

**Validate docs.json**:
```bash
jq empty docs.json
```

**Run script manually with debug**:
```bash
python3 -v scripts/update-llms-files.py
```

---

### Workflow not triggering

**Check cron schedule**:
- Workflows use UTC time
- Verify schedule in workflow YAML

**Manual trigger**:
```bash
# Via GitHub CLI
gh workflow run update-openapi.yml
gh workflow run update-llms-files.yml

# Or via GitHub UI
# Actions tab → Select workflow → Run workflow
```

---

## Best Practices

### For developers:

1. **Before major changes**: Run `python3 scripts/update-llms-files.py` to provide context
2. **After structure changes**: Update llms files manually
3. **Review workflow logs**: Check for failures after pushes
4. **Keep scripts updated**: Test locally before modifying workflows

### For AI assistants:

1. **Check llms.txt first**: Quick context without token overhead
2. **Reference llms-full.txt**: For detailed implementation guidance
3. **Note timestamps**: Files show last update time
4. **Verify accuracy**: Cross-reference with actual files when uncertain

### For maintenance:

1. **Monitor workflow success**: Set up notifications for failures
2. **Review commits**: Automated commits should have clear messages
3. **Update dependencies**: Keep actions and Python versions current
4. **Document changes**: Update this guide when modifying workflows

---

## Future Enhancements

Potential improvements to automation:

- [ ] Generate SDK documentation from OpenAPI spec
- [ ] Validate internal links after updates
- [ ] Create changelog from OpenAPI diffs
- [ ] Notify Slack/Discord of significant changes
- [ ] Generate API migration guides for breaking changes
- [ ] Create visual API coverage reports
- [ ] Monitor API endpoint health
- [ ] Generate TypeScript types from schemas

---

## Questions?

- **Documentation**: Check `CLAUDE.md` for development guidance
- **Scripts**: See `scripts/README.md` for detailed documentation
- **Support**: Visit https://rhombus.community
- **Issues**: Report at GitHub repository issues page

---

**Last Updated**: 2025-01-21
**Maintained By**: Rhombus Developer Documentation Team
