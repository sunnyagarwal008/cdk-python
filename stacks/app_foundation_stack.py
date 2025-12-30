from aws_cdk import (
    Stack,
    NestedStack,
    CfnOutput,
    aws_ssm as ssm,
    aws_iam as iam,
)
from constructs import Construct


class AppConfigNestedStack(NestedStack):
    """Nested stack that creates SSM parameters for app configuration (free tier)."""

    def __init__(self, scope: Construct, construct_id: str, environment: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # SSM Parameters are free (standard tier)
        self.app_name_param = ssm.StringParameter(
            self,
            "AppNameParam",
            parameter_name=f"/{environment}/app/name",
            string_value="MyNestedStackApp",
            description="Application name parameter",
        )

        self.environment_param = ssm.StringParameter(
            self,
            "EnvironmentParam",
            parameter_name=f"/{environment}/app/environment",
            string_value=environment,
            description="Environment name parameter",
        )


class AppIamNestedStack(NestedStack):
    """Nested stack that creates IAM role and policies for the app (free)."""

    def __init__(self, scope: Construct, construct_id: str, environment: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # IAM roles and policies are free
        self.app_role = iam.Role(
            self,
            "AppRole",
            role_name=f"{environment}-nested-stack-demo-role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Demo role created by nested stack",
        )

        # Add a basic policy (free)
        self.app_role.add_to_policy(
            iam.PolicyStatement(
                effect=iam.Effect.ALLOW,
                actions=["ssm:GetParameter", "ssm:GetParameters"],
                resources=["*"],
            )
        )


class AppFoundationStack(Stack):
    """Parent stack that provisions app foundation resources using nested stacks.
    
    This stack creates two nested stacks:
    1. AppConfigNestedStack - Creates SSM parameters for app configuration (free)
    2. AppIamNestedStack - Creates IAM role and policies for the app (free)
    
    All resources in this stack are free-tier and incur no cost.
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        environment = "dev"

        # Create nested stacks
        config_stack = AppConfigNestedStack(
            self,
            "ConfigNestedStack",
            environment=environment,
        )

        iam_stack = AppIamNestedStack(
            self,
            "IamNestedStack",
            environment=environment,
        )

        # Add dependency: IAM stack depends on Config stack
        iam_stack.add_dependency(config_stack)

        # Outputs from parent stack
        CfnOutput(
            self,
            "AppNameParamArn",
            value=config_stack.app_name_param.parameter_arn,
            description="ARN of the app name SSM parameter",
        )

        CfnOutput(
            self,
            "AppRoleArn",
            value=iam_stack.app_role.role_arn,
            description="ARN of the IAM role created by nested stack",
        )
