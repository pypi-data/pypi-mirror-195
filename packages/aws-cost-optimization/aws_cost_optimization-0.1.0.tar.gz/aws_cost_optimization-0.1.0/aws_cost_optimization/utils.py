import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


def get_regions(session):
    """
    :session: aws session object
    :return: list of regions
    """
    logger.info(" ---Inside utils :: get_regions()--- ")
    client = session.client('ec2', region_name='us-east-1')
    region_response = client.describe_regions()

    regions = [region['RegionName'] for region in region_response['Regions']]
    return regions


def list_volumes(session, regions: list) -> dict:
    """
    :param regions:
    :param session:
    :return:
    """
    logger.info(" ---Inside utils :: list_gp2_volumes()--- ")

    volume_list = {}

    for region in regions:
        client = session.client('ec2', region_name=region)
        marker = ''
        while True:
            if marker == '':
                response = client.describe_volumes()
            else:
                response = client.describe_volumes(
                    NextToken=marker
                )
            volume_list.setdefault(region, []).extend(response['Volumes'])

            try:
                marker = response['NextToken']
                if marker == '':
                    break
            except KeyError:
                break

    return volume_list


# returns the pricing of resource
def get_pricing(session, region: str, service_code: str, filter_field: str, filter_value: str) -> dict:
    """
    :param filter_value:
    :param filter_field:
    :param service_code:
    :param region: aws region
    :param session: aws session
    :return: pricing
    """
    logger.info(" ---Inside utils :: get_pricing()--- ")

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
    resolved_region = aws_region_map[region]
    aws_pricing_region = region

    client = session.client('pricing', region_name=aws_pricing_region)

    response = client.get_products(
        ServiceCode=service_code,
        Filters=[
            {'Type': 'TERM_MATCH', 'Field': filter_field, 'Value': filter_value},
            {'Type': 'TERM_MATCH', 'Field': 'location', 'Value': resolved_region}
        ]
    )
    prices = {}
    for price in response['PriceList']:
        # print(price)
        price = json.loads(price)
        for key in price['terms']['OnDemand'].keys():
            for k in price['terms']['OnDemand'][key]['priceDimensions'].keys():
                temp = price['terms']['OnDemand'][key]['priceDimensions'][k]['pricePerUnit']['USD']
                prices[price['product']['attributes']['volumeApiName']] = temp

    return prices
