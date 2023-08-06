from DateTime import DateTime
from boto3 import session
import logging
from aws_cost_optimization.utils import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

__author__ = "Dheeraj Banodha"
__version__ = '0.0.1'


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

    def gp2_to_gp3(self) -> list:
        """
        :return:
        """
        logger.info(" ---aws_client :: gp2_to_gp3()--- ")

        recommendations = []

        volumes = list_volumes(self.session, self.regions)

        for region, volume_list in volumes.items():
            for volume in volume_list:
                if volume['VolumeType'] == 'gp2':
                    price = get_pricing(self.session, region, 'AmazonEC2', filter_field='volumeType',
                                        filter_value='General Purpose')
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
