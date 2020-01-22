import boto3

def main():
    ec2 = boto3.resource('ec2', region_name='us-east-1')

    id = input('Enter instance id;')

    instance = ec2.Instance(id)

    print('Starting instance with id ', id)
    instance.start()

    # get attached volumes before stopping instance
    volumes = instance.volumes

    print('Stopping instance with id ', id)
    instance.stop()

    print('Creating snapshots of EBS attached to instance with id ', id)
    for volume in volumes.all():
        snap = ec2.create_snapshot(
            Description='Snap-auto' + volume.id,
            VolumeId=volume.id,
            TagSpecifications=[
                {
                    'ResourceType': 'snapshot',
                    'Tags': [
                        {
                            'Key':'string',
                            'Value':'string'
                        },
                    ]
                },
            ],
        )
        print('[Create snapshot]: ' + snap.snapshot_id + ' for volume ' + snap.volume_id)

    print('Terminating instance with id ', id)
    instance.terminate()

if __name__ == '__main__':
    main()