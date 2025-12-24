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

        queue = sqs.Queue(
            self,
            "MyQueue",
            queue_name="MyQueue",
            visibility_timeout=Duration.seconds(300),
            retention_period=Duration.days(4),
            removal_policy=RemovalPolicy.DESTROY,
        )
