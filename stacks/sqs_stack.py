from aws_cdk import (
    Stack,
    Duration,
    RemovalPolicy,
    aws_sqs as sqs,
)
from constructs import Construct


class SQSStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Get context values from cdk.json
        queue_name = self.node.try_get_context("queueName")
        retention_days = self.node.try_get_context("queueRetentionDays")

        queue = sqs.Queue(
            self,
            "MyQueue2",
            queue_name=queue_name,
            visibility_timeout=Duration.seconds(500),
            retention_period=Duration.days(retention_days),
            removal_policy=RemovalPolicy.DESTROY,
        )
