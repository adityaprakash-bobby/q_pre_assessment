import boto3

ec2 = boto3.resource('ec2', region_name='us-east-1')

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

ec2_client = boto3.client('ec2', region_name='us-east-1')

ec2Client.modify_vpc_attribute(
    VpcId=vpc.id, 
    EnableDnsSupport={'Value': True}
)

ec2Client.modify_vpc_attribute(
    VpcId=vpc.id,
    EnableDnsHostnames={'Value': True}
)

# create igw for internet access
igw = ec2.create_internet_gateway()
# print(igw.id)
vpc.attach_internet_gateway(InternetGatewayId=igw.id)

# create route table and add public route
route_table = vpc.create_route_table()
public_route = route_table.create_route(DestinationCidrBlock='0.0.0.0/0', GatewayId=igw.id)

# create subnets 
subnet_1 = ec2_client.create_subnet(
    CidrBlock='10.0.1.0/24',
    VpcId=vpc.id,
)
subnet_2 = ec2_client.create_subnet(
    CidrBlock='10.0.2.0/24',
    VpcId=vpc.id,
)
subnet_3 = ec2_client.create_subnet(
    CidrBlock='10.0.3.0/24',
    VpcId=vpc.id,
)
subnet_4 = ec2_client.create_subnet(
    CidrBlock='10.0.4.0/24',
    VpcId=vpc.id,
)

# make subnet_1 and subnet_2 public and leave others private
route_table.associate_with_subnet(SubnetId=subnet_1.get('Subnet').get('SubnetId'))
route_table.associate_with_subnet(SubnetId=subnet_2.get('Subnet').get('SubnetId'))