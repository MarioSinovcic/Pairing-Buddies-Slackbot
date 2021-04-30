import boto3

class SecretsRetriever:
    def __init__(self):
        self.ssm = boto3.client('ssm', region_name='ap-southeast-2')

    def get_ssm_param(self, param_name: str, required: bool = True) -> str:
        """Get an encrypted AWS Systems Manger secret."""
        response = self.ssm.get_parameters(
            Names=[param_name],
            WithDecryption=True,
        )
        if not response['Parameters'] or not response['Parameters'][0] or not response['Parameters'][0]['Value']:
            if not required:
                return None
            raise Exception(
                f"Configuration error: missing AWS SSM parameter: {param_name}")
        return response['Parameters'][0]['Value']  