# Assessment Day 3

Use the [script](https://github.com/adityaprakash-bobby/q_pre_assessment/blob/master/VPC-Lambda-APIGateway/task.py) to configure a bastion host for the VPC with 2x Private and 2x Public subnets, with private subnets confgured with NAT gateways. The [script](https://github.com/adityaprakash-bobby/q_pre_assessment/blob/master/VPC-Lambda-APIGateway/task.py) creates a bastion host along with a host in one of the private subnets.


#### Accessing the private instance from JumpBox:

For this we are using ssh agent forwarding. We connect to Jumpbox using a private keyfile, then use this Jumbox to connect to the private instance with the key-pairs registered in the trusted host/administrator. Perform the following in the administrator to access the private instance:

```bash
ssh-add -k <jumpbox-keyfile>.pem
ssh-add -k <private-instance-keyfile>.pem

# connect to the jumpbox
ssh -A <user-name>@<jumpbox-public-ip>

# connect to private instance inside jumpbox
(jumpbox)$ ssh <user-name>@<private-instance-private-ip>
```