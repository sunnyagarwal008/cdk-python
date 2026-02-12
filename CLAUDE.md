# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an AWS CDK demo project written in Python that demonstrates infrastructure as code patterns including standard stacks and nested stacks.

## Development Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Activate virtual environment (if not already active)
source .venv/bin/activate
```

### CDK Commands
```bash
# Synthesize CloudFormation templates
cdk synth

# Deploy all stacks
cdk deploy --all

# Deploy specific stack
cdk deploy S3Stack

# List all stacks
cdk list

# Show differences between deployed and local
cdk diff

# Destroy all stacks
cdk destroy --all
```

## Architecture

### Entry Point
- `app.py` - Main CDK application that instantiates and synthesizes all stacks
- CDK configuration in `cdk.json` specifies `python3 app.py` as the app entry point

### Stack Organization

All stack definitions live in the `stacks/` directory:

1. **S3Stack** (`stacks/s3_stack.py`) - Simple stack creating a versioned S3 bucket with auto-delete enabled
2. **SQSStack** (`stacks/sqs_stack.py`) - Simple stack creating an SQS queue with custom retention and visibility timeout
3. **AppFoundationStack** (`stacks/app_foundation_stack.py`) - Demonstrates nested stack pattern with two child stacks:
   - `AppConfigNestedStack` - Creates SSM parameters for application configuration
   - `AppIamNestedStack` - Creates IAM role with SSM read permissions
   - Shows stack dependencies (IAM stack depends on Config stack)

### Nested Stack Pattern

The `AppFoundationStack` demonstrates how to:
- Create multiple `NestedStack` instances within a parent `Stack`
- Pass parameters (like `environment`) to nested stacks
- Define dependencies between nested stacks using `add_dependency()`
- Reference resources from nested stacks in parent stack outputs using properties like `config_stack.app_name_param.parameter_arn`

When creating new nested stacks:
1. Define nested stack classes that inherit from `NestedStack`
2. Instantiate them within a parent stack that inherits from `Stack`
3. Use `add_dependency()` to define explicit ordering when needed
4. Access nested stack resources via the nested stack instance properties

### Resource Naming

Resources use a mix of:
- Explicit resource names (e.g., `bucket_name="sunny-cdk-test-bucket"`)
- CDK-generated logical IDs (construct_id parameter)

### Removal Policies

Most resources use `RemovalPolicy.DESTROY` and `auto_delete_objects=True` for development/demo purposes, allowing clean teardown.
