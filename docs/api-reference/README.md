# API Reference Documentation

This directory contains the API reference documentation for Rhombus Systems, automatically generated from our OpenAPI specification.

## OpenAPI Specification

The `openapi.json` file contains the complete API specification fetched from:

```text
https://api2.rhombussystems.com/api/openapi/public.json
```

## Automatic Updates

### Nightly Updates

The OpenAPI specification is automatically updated nightly at 2 AM UTC via GitHub Actions. The workflow:

1. Fetches the latest spec from the Rhombus API
2. Compares it with the current version
3. Commits and pushes changes if updates are detected
4. Provides a summary of the update process

### Manual Updates

To manually update the OpenAPI specification:

```bash
# Using the provided script
./scripts/update-openapi.sh

# Or directly with curl
curl -s https://api2.rhombussystems.com/api/openapi/public.json > docs/api-reference/openapi.json
```

### Workflow Configuration

The GitHub Action workflow is configured in `.github/workflows/update-openapi.yml` and can be:

- Triggered automatically on schedule (nightly)
- Triggered manually via GitHub Actions UI
- Customized for different update frequencies

## Documentation Generation

Mintlify automatically generates the API documentation pages from the OpenAPI specification. The generated documentation includes:

- Interactive API explorer
- Request/response examples
- Parameter documentation
- Authentication details
- Error codes and responses

## Files

- `openapi.json` - The OpenAPI 3.0.1 specification
- `introduction.mdx` - API overview and authentication guide
- `endpoint/` - Additional endpoint documentation (if needed)

## Troubleshooting

If the automatic updates fail:

1. Check the GitHub Actions logs
2. Verify the API endpoint is accessible
3. Ensure the returned JSON is valid OpenAPI format
4. Run the manual update script to test locally

For issues with the generated documentation, refer to the [Mintlify OpenAPI documentation](https://mintlify.com/docs/api-playground/openapi/setup).
