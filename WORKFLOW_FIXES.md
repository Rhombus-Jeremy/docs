# OpenAPI Workflow Fixes - Documentation

## Overview

This document details all the improvements made to the Update OpenAPI Spec GitHub Actions workflow to make it more robust, reliable, and production-ready.

## Issues Identified and Fixed

### 1. Working Directory Management ✅

**Problem:**
- Each step had to manually `cd docs`
- Inconsistent and error-prone
- Could fail if directory doesn't exist

**Solution:**
```yaml
jobs:
  update-openapi:
    defaults:
      run:
        working-directory: docs
```

**Benefit:** All steps automatically run in the `docs/` directory, cleaner code, less chance of path errors.

---

### 2. Timeout Protection ✅

**Problem:**
- No timeout set, workflow could hang indefinitely
- Wastes GitHub Actions minutes
- Hard to debug stuck workflows

**Solution:**
```yaml
jobs:
  update-openapi:
    timeout-minutes: 15
```

**Benefit:** Workflow will automatically fail after 15 minutes, preventing resource waste.

---

### 3. Git History Access ✅

**Problem:**
- Only fetched latest commit
- Couldn't properly compare changes
- Limited git operations available

**Solution:**
```yaml
- name: Checkout repository
  uses: actions/checkout@v4
  with:
    fetch-depth: 0
```

**Benefit:** Full git history available for comparisons and operations.

---

### 4. Split Script Failure Handling ✅

**Problem:**
- If split script failed, entire workflow failed
- Split is useful but not critical
- Should continue even if split has issues

**Solution:**
```yaml
- name: Split OpenAPI spec
  continue-on-error: true
```

**Benefit:** Workflow continues even if split fails, main spec still gets updated.

---

### 5. Changed Files Tracking ✅

**Problem:**
- No count of changed files
- Hard to see scope of updates
- Limited metadata in commits

**Solution:**
```yaml
CHANGED_COUNT=$(git diff --name-only api-reference/ | wc -l)
echo "changed_count=$CHANGED_COUNT" >> $GITHUB_OUTPUT
```

**Benefit:** Commit messages now include file count, better visibility into changes.

---

### 6. Concurrent Update Prevention ✅

**Problem:**
- No pull before push
- Could fail if another workflow ran simultaneously
- Would lose updates or cause conflicts

**Solution:**
```bash
# Pull latest changes to avoid conflicts
git pull --rebase origin main || true
```

**Benefit:** Workflow handles concurrent updates gracefully.

---

### 7. Push Retry Logic ✅

**Problem:**
- Single push attempt
- Network issues would cause failure
- No recovery mechanism

**Solution:**
```bash
for i in {1..3}; do
  if git push origin main; then
    echo "✅ Successfully pushed changes"
    break
  else
    if [ $i -lt 3 ]; then
      echo "⚠️  Push failed, retrying in 5 seconds... (attempt $i/3)"
      sleep 5
      git pull --rebase origin main
    else
      echo "❌ Failed to push after 3 attempts"
      exit 1
    fi
  fi
done
```

**Benefit:** Network issues don't cause immediate failure, 3 retry attempts with automatic rebase.

---

### 8. Summary Generation Fix ✅

**Problem:**
- Used `git diff --name-only HEAD~1` which fails if no commit
- Summary wouldn't show when workflow succeeded but no changes
- Could crash the summary step

**Solution:**
```bash
# Show files from this run (not comparing to HEAD~1)
git diff --name-only HEAD api-reference/ 2>/dev/null | head -30 >> $GITHUB_STEP_SUMMARY
```

**Benefit:** Summary always works, shows current state even without commits.

---

### 9. Summary Always Runs ✅

**Problem:**
- Summary only ran if all previous steps succeeded
- No visibility into failures
- Hard to debug what went wrong

**Solution:**
```yaml
- name: Create summary
  if: always()
```

**Benefit:** Summary generated even if previous steps fail, better debugging.

---

## Complete Workflow Features

### Robustness
- ✅ 15-minute timeout prevents hanging
- ✅ Retry logic for git operations (3 attempts)
- ✅ Automatic pull/rebase before push
- ✅ Continue on non-critical failures
- ✅ Full error handling with rollback

### Reliability
- ✅ HTTP status code validation
- ✅ JSON validation before commit
- ✅ Backup and restore on failure
- ✅ Works in docs/ directory by default
- ✅ Full git history access

### Observability
- ✅ Detailed progress logging
- ✅ API spec info extraction
- ✅ Changed files count
- ✅ Comprehensive summaries
- ✅ Always-running summary step

### Automation
- ✅ Nightly schedule (2 AM UTC)
- ✅ Manual trigger support
- ✅ Automatic split after fetch
- ✅ Only commits when changes detected
- ✅ Rich commit messages with metadata

---

## Testing the Workflow

### Manual Trigger (Recommended for Testing)

**Via GitHub UI:**
1. Go to repository Actions tab
2. Select "Update OpenAPI Spec"
3. Click "Run workflow"
4. Select branch: `main`
5. Click "Run workflow" button

**Via GitHub CLI:**
```bash
gh workflow run update-openapi.yml
```

**Check run status:**
```bash
gh run list --workflow=update-openapi.yml --limit 5
```

**View specific run:**
```bash
gh run view <run-id>
```

---

### Automatic Trigger

The workflow runs automatically every night at 2 AM UTC.

**Next scheduled run:**
Check the Actions tab or use:
```bash
gh api repos/{owner}/{repo}/actions/workflows/update-openapi.yml
```

---

## Monitoring

### Success Indicators

✅ **Workflow succeeds with changes:**
- Green checkmark in Actions tab
- Commit shows in git history
- Summary shows files updated
- api-reference/ directory updated

✅ **Workflow succeeds without changes:**
- Green checkmark in Actions tab
- No new commit
- Summary shows "No changes detected"
- Shows current spec details

### Failure Indicators

❌ **Fetch fails:**
- HTTP error in logs
- Backup restored
- Workflow exits early
- No commit created

❌ **Validation fails:**
- JSON parsing error
- Backup restored
- Workflow exits early
- No commit created

❌ **Push fails (after 3 retries):**
- Git push error
- Commit created locally
- Not pushed to remote
- Summary shows failure

### Viewing Logs

1. Go to repository Actions tab
2. Click on workflow run
3. Click on job "update-openapi"
4. Expand step to view logs
5. Check summary at bottom of run page

---

## Expected Behavior

### When Changes Exist

```
1. Fetch spec ✅ (200 OK)
2. Validate JSON ✅
3. Extract metadata ✅ (Rhombus API v1.0, 849 endpoints)
4. Split spec ✅ (60 categories)
5. Detect changes ✅ (121 files changed)
6. Pull latest ✅
7. Commit ✅
8. Push ✅
9. Summary ✅
```

### When No Changes

```
1. Fetch spec ✅ (200 OK)
2. Validate JSON ✅
3. Extract metadata ✅
4. Split spec ✅
5. Detect changes ℹ️ (no changes)
6. Skip commit/push
7. Summary ✅ (shows current state)
```

### When Fetch Fails

```
1. Fetch spec ❌ (HTTP 500/timeout)
2. Restore backup ✅
3. Exit with error ❌
4. Summary ✅ (shows failure)
```

---

## Troubleshooting

### Workflow Not Running

**Check:**
- Is the schedule correct? (Cron syntax)
- Is the workflow file in `.github/workflows/`?
- Does the branch have Actions enabled?

**Fix:**
```bash
# Verify workflow file
cat .github/workflows/update-openapi.yml | grep -A 2 "schedule:"

# Check if Actions are enabled (via GitHub UI)
# Settings → Actions → General → Allow all actions
```

---

### Workflow Fails to Fetch

**Symptoms:**
- HTTP error in logs
- "Failed to download OpenAPI spec"

**Check:**
```bash
# Test API manually
curl -I https://api2.rhombussystems.com/api/openapi/public.json

# Should return: HTTP/2 200
```

**Possible causes:**
- API temporarily down
- Network issues
- Rate limiting

---

### Workflow Fails to Push

**Symptoms:**
- Commit created but not pushed
- "Failed to push after 3 attempts"

**Causes:**
- Branch protection rules
- Another workflow pushed simultaneously
- Permission issues

**Fix:**
```bash
# Check branch protection
# Settings → Branches → Branch protection rules

# Ensure Actions have write permission
# Settings → Actions → General → Workflow permissions
# Select: Read and write permissions
```

---

### Split Step Fails

**Symptoms:**
- Warning about split failure
- Workflow continues (this is expected)

**Impact:**
- Main openapi.json still updated ✅
- Split files may be outdated ⚠️

**Fix:**
```bash
# Run split manually
cd docs
bash scripts/split-openapi.sh

# Commit if needed
git add api-reference/openapi-split/
git commit -m "chore: update split OpenAPI files"
git push
```

---

## Performance Metrics

### Typical Run Time

- **With changes**: 2-3 minutes
- **Without changes**: 1-2 minutes
- **Timeout limit**: 15 minutes

### Network Usage

- **Download size**: ~2-5 MB (OpenAPI spec)
- **Upload size**: Varies based on changes

### GitHub Actions Minutes

- **Cost**: ~3 minutes per run
- **Monthly**: ~90 minutes (30 days × 3 minutes)
- **Annual**: ~1,095 minutes

---

## Maintenance

### Updating the Workflow

1. Edit `.github/workflows/update-openapi.yml`
2. Test changes locally if possible
3. Commit and push
4. Manually trigger to verify
5. Monitor next automatic run

### Changing Schedule

```yaml
on:
  schedule:
    # Change time (24-hour UTC format)
    - cron: '0 3 * * *'  # 3 AM UTC instead of 2 AM
```

### Disabling Workflow

**Temporarily:**
- GitHub UI → Actions → Select workflow → Disable

**Permanently:**
```bash
# Delete or rename file
mv .github/workflows/update-openapi.yml .github/workflows/update-openapi.yml.disabled
```

---

## Best Practices

1. **Monitor first few runs** after any changes
2. **Check summaries** to understand what changed
3. **Review commits** to ensure accuracy
4. **Test manually** before relying on automation
5. **Keep scripts updated** (update-openapi.sh, split-openapi.sh)
6. **Document any changes** to workflow or scripts

---

## Related Files

- **Workflow**: `.github/workflows/update-openapi.yml`
- **Update script**: `scripts/update-openapi.sh`
- **Split script**: `scripts/split-openapi.sh`
- **Documentation**: `AUTOMATION.md`, `scripts/README.md`
- **Output files**: `api-reference/openapi.json`, `api-reference/openapi-split/`

---

## Questions?

- Check `AUTOMATION.md` for comprehensive automation guide
- Check `scripts/README.md` for script documentation
- Visit https://rhombus.community for support
- Report issues at GitHub repository

---

**Last Updated**: 2025-01-21
**Status**: Production Ready ✅
**Tested**: Yes, locally and via GitHub Actions
