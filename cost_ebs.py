#!/usr/bin/env python3
import boto3
import pandas as pd
import json
import sys

def get_attached_gp2_volumes(ec2):
    response = ec2.describe_volumes(Filters=[
        {'Name': 'volume-type', 'Values': ['gp2']},
        {'Name': 'attachment.status', 'Values': ['attached']}
    ])
    attached_volumes = response['Volumes']
    return attached_volumes

def sum_attached_gp2_sizes(volumes):
    total_size = sum(volume['Size'] for volume in volumes)
    return total_size

def get_available_ebs_volumes(ec2):
    response = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])
    available_volumes = response['Volumes']
    return available_volumes

def sum_available_ebs_size(volumes):
    total_size = sum(volume['Size'] for volume in volumes)
    return total_size

if __name__ == "__main__":
    region = sys.argv[1]
    ec2 = boto3.client('ec2', region_name=region)

    attached_volumes = get_attached_gp2_volumes(ec2)
    total_attached_size = sum_attached_gp2_sizes(attached_volumes)

    available_volumes = get_available_ebs_volumes(ec2)
    total_available_size = sum_available_ebs_size(available_volumes)

    print(f"Total size of attached gp2 EBS volumes: {total_attached_size} GiB")
    print(f"Total size of available EBS volumes: {total_available_size} GiB")

    aws_region_map = {
    'ca-central-1': 'Canada (Central)',
    'ap-northeast-3': 'Asia Pacific (Osaka-Local)',
    'us-east-1': 'US East (N. Virginia)',
    'ap-northeast-2': 'Asia Pacific (Seoul)',
    'us-gov-west-1': 'AWS GovCloud (US)',
    'us-east-2': 'US East (Ohio)',
    'ap-northeast-1': 'Asia Pacific (Tokyo)',
    'ap-south-1': 'Asia Pacific (Mumbai)',
    'ap-southeast-2': 'Asia Pacific (Sydney)',
    'ap-southeast-1': 'Asia Pacific (Singapore)',
    'sa-east-1': 'South America (Sao Paulo)',
    'us-west-2': 'US West (Oregon)',
    'eu-west-1': 'EU (Ireland)',
    'eu-west-3': 'EU (Paris)',
    'eu-west-2': 'EU (London)',
    'us-west-1': 'US West (N. California)',
    'eu-central-1': 'EU (Frankfurt)'
    }
    ebs_name_map = {
        'standard': 'Magnetic',
        'gp2': 'General Purpose',
        'gp3': 'General Purpose',
        'io1': 'Provisioned IOPS',
        'st1': 'Throughput Optimized HDD',
        'sc1': 'Cold HDD'
    }

    resolved_region = aws_region_map[region]
    aws_pricing_region = "us-east-1"
    pricing_auth = boto3.client('pricing', region_name=aws_pricing_region)

    for ebs_code in ebs_name_map:
        response = pricing_auth.get_products(ServiceCode='AmazonEC2', Filters=[
            {'Type': 'TERM_MATCH', 'Field': 'volumeType', 'Value': ebs_name_map[ebs_code]},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': resolved_region}])

        for result in response['PriceList']:
            json_result = json.loads(result)
            for json_result_level_1 in json_result['terms']['OnDemand'].values():
                for json_result_level_2 in json_result_level_1['priceDimensions'].values():
                    for price_value in json_result_level_2['pricePerUnit'].values():
                        if ebs_code == json_result['product']['attributes']['volumeApiName']:
                            ebs_name_map[ebs_code] = float(price_value)


    gp2_total_cost = total_attached_size * ebs_name_map['gp2']
    gp3_total_cost = total_attached_size * ebs_name_map['gp3']
    cost_difference = gp2_total_cost - gp3_total_cost

    total_available_cost = sum(volume['Size'] * ebs_name_map[volume['VolumeType']] for volume in available_volumes)


    data_gp2 = []
    data_available = []
    total_cost_difference = 0
    total_available_cost = 0

    for volume in attached_volumes:
        if volume['VolumeType'] == 'gp2':
            gp2_cost = ebs_name_map['gp2'] * volume['Size']
            gp3_cost = ebs_name_map['gp3'] * volume['Size']
            cost_difference = gp2_cost - gp3_cost
            total_cost_difference += cost_difference
            data_gp2.append({'VolumeId': volume['VolumeId'], 'Size (GiB)': volume['Size'], 'Cost GP2 ($)': gp2_cost, 'Cost GP3 ($)': gp3_cost, 'Cost Difference ($)': cost_difference})

    # Adicionar linha com a soma total das diferenças de custo
    data_gp2.append({'VolumeId': 'Total', 'Size (GiB)': '', 'Cost GP2 ($)': '', 'Cost GP3 ($)': '', 'Cost Difference ($)': total_cost_difference})

    for volume in available_volumes:
        ebs_type = volume['VolumeType']
        cost_per_size = ebs_name_map.get(ebs_type, 0)
        cost = cost_per_size * volume['Size']
        total_available_cost += cost  # Adicionar o custo ao total
        data_available.append({'VolumeId': volume['VolumeId'], 'Size (GiB)': volume['Size'], 'Type': ebs_type, 'Cost ($)': cost})
    
    data_available.append({'VolumeId': 'Total', 'Size (GiB)': '', 'Type': '', 'Cost ($)': total_available_cost})
    df_gp2 = pd.DataFrame(data_gp2)
    df_available = pd.DataFrame(data_available)

    # Escrever para arquivo Excel
    with pd.ExcelWriter('ebs_volumes.xlsx') as writer:
        df_gp2.to_excel(writer, sheet_name='GP2 Volumes', index=False)
        df_available.to_excel(writer, sheet_name='Available Volumes', index=False)
print(f"Total cost of available EBS volumes: ${total_available_cost:.2f}")
print(f"Total cost difference (savings) by switching to gp3: ${total_cost_difference:.2f}")
print("Excel file generated successfully.")
