import boto3
import csv
from pprint import pprint
client = boto3.client(service_name='ec2')

file = open('Instance_Details.csv', 'w', newline='')
data = csv.writer(file)
data.writerow(['No.', 'Name', 'InstanceID', 'PubicIP', 'Status', 'AMI ID', 'Availability Zone', 'OS'])

all_regions = []
for each_region in client.describe_regions()['Regions']:
    all_regions.append(each_region['RegionName'])
#print(all_regions)

count = 1
for each_region in all_regions:
    instance_in_each_region = boto3.resource(service_name='ec2', region_name=each_region)
    for each_ins_in_region in instance_in_each_region.instances.all():
        #pprint(dir(each_ins_in_region))
        status = each_ins_in_region.state['Name']
        if each_ins_in_region.tags:
            for idx, tag in enumerate(each_ins_in_region.tags):
                if tag['Key'] == 'Name':
                    instance_name = tag['Value']
        for iface in each_ins_in_region.network_interfaces:
            availability_zone = iface.subnet.availability_zone

        data.writerow([count, instance_name, each_ins_in_region.instance_id, each_ins_in_region.public_ip_address,
                       status, each_ins_in_region.image_id, availability_zone, each_ins_in_region.platform_details])
        count += 1

file.close()
