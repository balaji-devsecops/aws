#!/usr/bin/env python3

import boto3

# Connect to EC2
ec2 = boto3.client('ec2', region_name='eu-central-1')

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

# Print unused AMIs with associated tags
for ami in ec2.describe_images(ImageIds=list(unused_amis))['Images']:
    print("ImageId: {}\nTags: {}\n".format(ami['ImageId'], ami['Tags']))
