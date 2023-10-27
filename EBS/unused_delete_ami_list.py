#!/usr/bin/env python3

import boto3

# Connect to EC2 in a specific region
ec2 = boto3.client('ec2', region_name='us-west-2')

# Get a list of all AMIs currently in use
in_use_amis = []
for reservation in ec2.describe_instances()['Reservations']:
    for instance in reservation['Instances']:
        in_use_amis.append(instance['ImageId'])

# Get a list of all AMIs with tags
tagged_amis = []
filters = [{'Name': 'tag-key', 'Values': ['*']}]
for ami in ec2.describe_images(Owners=['self'], Filters=filters)['Images']:
    tagged_amis.append(ami['ImageId'])

# Get a list of unused AMIs
unused_amis = set(tagged_amis) - set(in_use_amis)

# Delete unused AMIs
for ami_id in unused_amis:
    ec2.deregister_image(ImageId=ami_id)
    print("Deleted AMI {}".format(ami_id))
