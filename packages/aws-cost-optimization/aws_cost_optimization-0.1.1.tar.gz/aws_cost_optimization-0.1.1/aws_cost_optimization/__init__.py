import time

from boto3 import session
import logging
from aws_cost_optimization.utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

__author__ = "Dheeraj Banodha"
__version__ = '0.1.1'


class aws_client:
    def __init__(self, **kwargs):
        if 'aws_access_key_id' in kwargs.keys() and 'aws_secret_access_key' in kwargs.keys():
            self.session = session.Session(
                aws_access_key_id=kwargs['aws_access_key_id'],
                aws_secret_access_key=kwargs['aws_secret_access_key'],
            )
        elif 'profile_name' in kwargs.keys():
            self.session = session.Session(profile_name=kwargs['profile_name'])

        self.regions = get_regions(self.session)
        self.aws_region_map = {
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
            'eu-central-1': 'EU (Frankfurt)',
            'eu-north-1': 'EU (Stockholm)'
        }

    def gp2_to_gp3(self) -> list:
        """
        :return: list of cost saving recommendations
        """
        logger.info(" ---Inside aws_client :: gp2_to_gp3()--- ")

        recommendations = []

        volumes = list_volumes(self.session, self.regions)

        for region, volume_list in volumes.items():
            resolved_region = self.aws_region_map[region]
            for volume in volume_list:
                if volume['VolumeType'] == 'gp2':
                    Filters = [
                        {'Type': 'TERM_MATCH', 'Field': 'volumeType', 'Value': 'General Purpose'},
                        {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': resolved_region}
                    ]
                    price = get_pricing(self.session, region, 'AmazonEC2', Filters=Filters)
                    current_cost = float(price['gp2']) * float(volume['Size'])
                    effective_cost = float(price['gp3']) * float(volume['Size'])
                    recommendation = {
                        'Region': region,
                        'Volume Id': volume['VolumeId'],
                        'Current Cost': current_cost,
                        'Effective Cost': effective_cost,
                        'Savings': current_cost - effective_cost,
                        'Savings %':  ((current_cost - effective_cost)/current_cost)*100
                    }
                    recommendations.append(recommendation)

        return recommendations

    def rds_upgrades(self) -> list:
        """
        :return: list of cost saving recommendations
        """
        logger.info(" ---Inside aws_client :: rds_upgrades()--- ")

        recommendations = []

        rds_instances = list_rds_instances(self.session, self.regions)

        for region, rds_list in rds_instances.items():
            resolved_region = self.aws_region_map[region]
            for instance in rds_list:
                instance_type = instance['DBInstanceClass']
                instance_family = instance_type.split('.')[1]

                Filters = [
                    {'Type': 'TERM_MATCH', 'Field': 'instanceType', 'Value': instance_type},
                    {'Type': 'TERM_MATCH', 'Field': 'databaseEngine', 'Value': instance['Engine']},
                    {'Type': 'TERM_MATCH', 'Field': 'deploymentOption', 'Value': 'Single-AZ' if instance['MultiAZ'] else 'Multi-AZ'},
                    {'Type': 'TERM_MATCH', 'Field': 'productFamily', 'Value': 'Database Instance'},
                    {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': resolved_region}
                ]

                def evaluate(frm: str, to: str):
                    price_from = get_pricing(
                        self.session, region, 'AmazonRDS',
                        Filters
                    )
                    print(price_from)
                    Filters[0]['Value'] = instance_type.replace(frm, to)
                    price_to = get_pricing(
                        self.session, region, 'AmazonRDS', Filters
                    )
                    print(price_to)
                    current_cost = float(price_from[instance_type]) * 730
                    effective_cost = float(price_to[instance_type.replace(frm, to)]) * 730

                    recommendation = {
                        'Region': region,
                        'Instance Id': instance['DBInstanceIdentifier'],
                        'Instance Type': instance_type,
                        'Upgrade To': instance_type.replace(frm, to),
                        'Current Cost': current_cost,
                        'Effective Cost': effective_cost,
                        'Savings': current_cost - effective_cost,
                        'Savings %': ((current_cost - effective_cost) / current_cost) * 100
                    }
                    return recommendation

                match instance_family:
                    case 'm3':
                        recommendations.append(evaluate('m3', 'm5'))
                    case 'r3':
                        recommendations.append(evaluate('r3', 'r5'))
                    case 'm1':
                        recommendations.append(evaluate('m1', 't2'))

        return recommendations
