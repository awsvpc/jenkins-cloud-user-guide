import boto3
import time

def wait_for_deploy_tag(instance_id):
    ec2_client = boto3.client('ec2')
    start_time = time.time()
    while time.time() - start_time < 2700:  # 45 minutes timeout
        response = ec2_client.describe_instances(InstanceIds=[instance_id])
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                for tag in instance['Tags']:
                    if tag['Key'] == 'Deploy' and tag['Value'] == 'Completed':
                        return True
        time.sleep(60)  # Check every minute
    return False  # Timeout reached, deploy tag not found or not completed

def find_management_ip(instance_id):
    if not wait_for_deploy_tag(instance_id):
        print("Deploy tag not found or not completed within 45 minutes. Skipping management IP lookup.")
        return None
    
    ec2_client = boto3.client('ec2')
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            for network_interface in instance['NetworkInterfaces']:
                subnet_id = network_interface['SubnetId']
                subnet_info = ec2_client.describe_subnets(SubnetIds=[subnet_id])
                for subnet in subnet_info['Subnets']:
                    for tag in subnet['Tags']:
                        if tag['Key'] == 'tier' and tag['Value'] == 'management':
                            management_ip = network_interface['PrivateIpAddress']
                            print("Queried IP:", management_ip)
                            return management_ip
    return None

# Example usage:
instance_id = 'your_instance_id_here'
management_ip = find_management_ip(instance_id)
if management_ip:
    print("Management IP:", management_ip)
else:
    print("No management IP found.")
