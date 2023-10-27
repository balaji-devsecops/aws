#!/usr/bin/env python3

import boto3

# Connect to EC2 in a specific region
ec2 = boto3.client('ec2', region_name='us-west-2')

# Get a list of all AMIs with tags
filters = [{'Name': 'tag-key', 'Values': ['*']}]
for ami in ec2.describe_images(Owners=['self'], Filters=filters)['Images']:
    print("ImageId: {}\nTags: {}\n".format(ami['ImageId'], ami['Tags']))
