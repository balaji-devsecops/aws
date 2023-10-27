#!/usr/bin/env python3

import boto3

# Connect to EC2 in a specific region
ec2 = boto3.client('ec2', region_name='us-west-2')

# Get a list of all AMIs currently in use
used_amis = {}
for reservation in ec2.describe_instances()['Reservations']:
    for instance in reservation['Instances']:
        ami_id = instance['ImageId']
        if ami_id not in used_amis:
            used_amis[ami_id] = {'Tags': [], 'Instances': []}
        used_amis[ami_id]['Instances'].append(instance['InstanceId'])

# Get a list of used AMIs with tags
filters = [{'Name': 'tag-key', 'Values': ['*']}]
for ami in ec2.describe_images(Owners=['self'], Filters=filters)['Images']:
    ami_id = ami['ImageId']
    if ami_id in used_amis:
        used_amis[ami_id]['Tags'] = ami['Tags']

# Print used AMIs with associated tags and instances
for ami_id, ami_data in used_amis.items():
    print("ImageId: {}\nTags: {}\nInstances: {}\n".format(ami_id, ami_data['Tags'], ami_data['Instances']))
