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
def get_pricing(session, region: str, service_code: str, Filters: list) -> dict:
    """
    :param Filters:
    :param service_code:
    :param region: aws region
    :param session: aws session
    :return: pricing
    """
    logger.info(" ---Inside utils :: get_pricing()--- ")

    aws_pricing_region = region

    client = session.client('pricing', 'us-east-1')

    response = client.get_products(
        ServiceCode=service_code,
        Filters=Filters
    )
    prices = {}
    for price in response['PriceList']:
        price = json.loads(price)
        for key in price['terms']['OnDemand'].keys():
            for k in price['terms']['OnDemand'][key]['priceDimensions'].keys():
                temp = price['terms']['OnDemand'][key]['priceDimensions'][k]['pricePerUnit']['USD']

                prices[price['product']['attributes']['instanceType' if service_code == 'AmazonRDS' else 'volumeApiName']] = temp

    return prices


# returns the list of rds instances
def list_rds_instances(session, regions: list) -> dict:
    """
    :param regions:
    :param session:
    :return:
    """
    logger.info(" ---Inside utils :: list_rds_instances()--- ")
    rds_instance_lst = {}

    for region in regions:
        client = session.client('rds', region_name=region)

        marker = ''
        while True:
            response = client.describe_db_instances(
                MaxRecords=100,
                Marker=marker
            )
            rds_instance_lst.setdefault(region, []).extend(response['DBInstances'])

            try:
                marker = response['Marker']
                if marker == '':
                    break
            except KeyError:
                break
    return rds_instance_lst
