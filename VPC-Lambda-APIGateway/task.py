import boto3

ec2 = boto3.resource('ec2', region_name='us-east-1')
ec2_client = boto3.client('ec2', region_name='us-east-1')

# create VPC
vpc = ec2.create_vpc(
    CidrBlock='10.0.0.0/16'
)
vpc.create_tags(Tags=[
    {
        'Key':'Name',
        'Value': 'boto3_vpc_dont_delete'
    }
])
vpc.wait_until_available()


ec2_client.modify_vpc_attribute(
    VpcId=vpc.id, 
    EnableDnsSupport={'Value': True}
)

ec2_client.modify_vpc_attribute(
    VpcId=vpc.id,
    EnableDnsHostnames={'Value': True}
)

# create 2xPublic and 2xPrivate subnets 
subnet_1_public = vpc.create_subnet(
    CidrBlock='10.0.1.0/24',
    AvailabilityZone='us-east-1a'
)
subnet_2_public = vpc.create_subnet(
    CidrBlock='10.0.2.0/24',
    AvailabilityZone='us-east-1b'
)
subnet_3_private = vpc.create_subnet(
    CidrBlock='10.0.3.0/24',
    AvailabilityZone='us-east-1a'
)
subnet_4_private = vpc.create_subnet(
    CidrBlock='10.0.4.0/24',
    AvailabilityZone='us-east-1b'
)

subnet_1_public.meta.client.modify_subnet_attribute(SubnetId=subnet_1_public.id, MapPublicIpOnLaunch={"Value": True})
subnet_2_public.meta.client.modify_subnet_attribute(SubnetId=subnet_2_public.id, MapPublicIpOnLaunch={"Value": True})

# create tags for the subnets
subnet_1_public_tag = [subnet_1_public.id]
subnet_2_public_tag = [subnet_2_public.id]
subnet_3_private_tag = [subnet_3_private.id]
subnet_4_private_tag = [subnet_4_private.id]

ec2_client.create_tags(Resources=subnet_1_public_tag,Tags=[{'Key':'Name','Value':'boto3_public_subnet_1'}])
ec2_client.create_tags(Resources=subnet_2_public_tag,Tags=[{'Key':'Name','Value':'boto3_public_subnet_2'}])
ec2_client.create_tags(Resources=subnet_3_private_tag,Tags=[{'Key':'Name','Value':'boto3_private_subnet_1'}])
ec2_client.create_tags(Resources=subnet_4_private_tag,Tags=[{'Key':'Name','Value':'boto3_private_subnet_2'}])


# create igw for internet access and attach to vpc
igw = ec2.create_internet_gateway()
vpc.attach_internet_gateway(InternetGatewayId=igw.id)

# create route table and add public route
route_table = vpc.create_route_table()
public_route = route_table.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=igw.id)


# make subnet_1 and subnet_2 public and leave others private
route_table.associate_with_subnet(SubnetId=subnet_1_public.id)
route_table.associate_with_subnet(SubnetId=subnet_2_public.id)

# Private route table for private subnets
private_route_table = ec2.create_route_table(VpcId=vpc.id)
private_route_table.associate_with_subnet(SubnetId=subnet_3_private.id)
private_route_table.associate_with_subnet(SubnetId=subnet_4_private.id)

# allocate elastic IPs
allocation = ec2_client.allocate_address(
    Domain='vpc'
)

# create NAT gateway
nat_gw = ec2_client.create_nat_gateway(
    AllocationId=allocation['AllocationId'],
    SubnetId=subnet_1_public.id
)
nat_gw_id = nat_gw['NatGateway']['NatGatewayId']

# attach NAT to private subnets
ec2_client.create_route(RouteTableId=private_route_table.id,DestinationCidrBlock='0.0.0.0/0',NatGatewayId=nat_gw_id)

# create security group for bastion host
bastion_sec_group = ec2.create_security_group(
    GroupName='ssh_bastion',
    Description='allow ssh to bastion',
    VpcId=vpc.id
)

bastion_sec_data_ingress = ec2_client.authorize_security_group_ingress(
    GroupId=bastion_sec_group.id,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
)

bastion_sec_data_egress = ec2_client.authorize_security_group_ingress(
    GroupId=bastion_sec_group.id,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
        }
    ]
)

# create a security group for instances in private subnet
sec_group = ec2.create_security_group(
    GroupName='ssh_http_sg',
    Description='allow ssh http access',
    VpcId=vpc.id
)

sec_data = ec2_client.authorize_security_group_ingress(
    GroupId=sec_group.id,
    IpPermissions=[
        {
            'IpProtocol': 'tcp',
            'FromPort': 22,
            'ToPort': 22,
            'IpRanges': [{'CidrIp': bastion_sec_group.id}]
        },
        {
            'CidrIp':'10.10.1.0/24',
            'IpProtocol':'-1',
            'FromPort':'-1',
            'ToPort':'-1',
        }
    ]
)

# create bastion host
bastion_host = ec2.create_instances(
    ImageId='ami-062f7200baf2fa504',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    SubnetId=subnet_1['Subnet']['SubnetId'],
    SecurityGroups=[
        bastion_sec_group.id,
    ],
    KeyName='test-keyfile'
)

private_host = ec2.create_instances(
    ImageId='ami-062f7200baf2fa504',
    MinCount=1,
    MaxCount=1,
    InstanceType='t2.micro',
    SubnetId=subnet_3['Subnet']['SubnetId'],
    SecurityGroups=[
        sec_group.id,
    ],
    KeyName='private_ssh'
)