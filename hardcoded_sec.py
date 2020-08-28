import json
import boto3

def lambda_handler(event, context):
    ec2_client = boto3.client('ec2')
    security_groups = ec2_client.describe_security_groups()
    try:
        for key, value in security_groups.items():
            for index in range(len(value)):
                result = value[index].get('IpPermissions')
                for j in range(len(result)):
                    port = result[j].get('FromPort')
                    ip_range = result[j].get('IpRanges')
                    name = result[j].get('GroupName')
                    group_id = result[j].get('GroupId')
                    if port == 22 and ip_range == [{'CidrIp': '0.0.0.0/0'}]:
                        ec2_client.revoke_security_group_ingress(
#                            CidrIp='0.0.0.0/0',
                            GroupId='sg-00fe41e943c1de5f1',
                            GroupName='lambdatest',
                            IpPermissions=[
                                {
                                    'FromPort': 22,
                                    'ToPort' : 22,
                                    'IpProtocol': 'tcp',
                                    'IpRanges': [{'CidrIp' : '0.0.0.0/0'}]
                                }
                            ]
                        )
    except KeyError:
        print('An error occured!')
