#!/usr/bin/env python3
import aws_cdk as cdk

from stacks.s3_stack import S3Stack
from stacks.sqs_stack import SQSStack
from stacks.app_foundation_stack import AppFoundationStack

app = cdk.App()
S3Stack(app, "S3Stack")
SQSStack(app, "SQSStack")
AppFoundationStack(app, "AppFoundationStack")

app.synth()
