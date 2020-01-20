# Pre Assessment

1. Create IAM Policy which grants access to S3 bucket Only.
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "s3:GetBucketLocation",
            "Resource": "arn:aws:s3:::*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": "s3:*",
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": "s3:ListAllMyBuckets",
            "Resource": "arn:aws:s3:::*"
        }
    ]
}
```
2. The outcome of the following policy will it will deny the access to all the services and their resources to anybody.
3. Steps to launch an EC2 instance:
  - Go to the AWS management console (make sure you choose the appropriate region before hand.)
  - Search for EC2 service and go the EC2 dashboard
  - Click on `Launch Instance` button
  - Choose an Amazon machine Image
  - Configure the instance
    - Mention the number of instances to be bootstrapped.
    - Select the VPC you want the instance to be in.
    - Choose a default subnet in any Availability Zone
  - Choose **Next:Add Storage**
    - By default a 8GB EBS will be provided for the root volume.
    - You can change the size of the disks according to requirement.
  - Click on **Next:Add tags**
    - Specify suitable tags (key-value pairs) to identify you instance
  - Click **Next:Configure Security groups**
    - Mention the ports that have to be opened on the instance and the IPs from which the traffic should be allowed.
    - For example, select SSH and HTTP/HTTPS for a web-server.
  - Click on **Recview and Launch**
    - Click on **Launch**
    - here, you will be prompted to download the key-pair associated with the instance (create a new, or use an existing one) for remote access. Download and store the `<key-pair>.pem` file for future EC2 access.

4. 
