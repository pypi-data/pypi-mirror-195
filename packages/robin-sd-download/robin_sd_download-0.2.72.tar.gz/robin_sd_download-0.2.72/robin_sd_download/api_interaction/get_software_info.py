import requests
import datetime

from robin_sd_download.api_interaction import get_bearer_token
from robin_sd_download.supportive_scripts import yaml_parser
from robin_sd_download.supportive_scripts import logger


def get_software_info():
    config = yaml_parser.parse_config()
    radar_id = config['radar_id']
    request_url = config['api_url']

    try:
        bearer_token = str(get_bearer_token.get_bearer_token())
    except Exception as e:
        logger.log(message=f"Failed to get bearer token: {e}", log_level="error", to_terminal=True)
        return None

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {bearer_token}',
    }

    api_endpoint = f'/api/radars/{radar_id}'

    try:
        response = requests.get(request_url + api_endpoint, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        logger.log(message=f"Failed to get software info: {e}", log_level="error", to_terminal=True)
        return None

    software_info = response.json()['radar']['software']

    # Extract the relevant information from the software object
    software = {
        'id': software_info['_id'],
        'software_path': software_info['softwarePath'],
        'software_type': software_info['softwareType'],
        'radar_type': software_info['radarType'],
        'version': software_info['version'],
        'recalled': software_info['recalled'],
        'available_for_all': software_info['availableForAll'],
        'created_at': datetime.datetime.strptime(software_info['createdAt'], '%Y-%m-%dT%H:%M:%S.%fZ'),
        'updated_at': datetime.datetime.strptime(software_info['updatedAt'], '%Y-%m-%dT%H:%M:%S.%fZ')
    }

    # Log the software information
    logger.log(message=f"Software ID: {software['id']}" , log_level="info" , to_terminal=True)
    logger.log(message=f"Software type: {software['software_type']}" , log_level="info" , to_terminal=True)
    logger.log(message=f"Radar type: {', '.join(software['radar_type'])}" , log_level="info" , to_terminal=True)
    logger.log(message=f"Version: {software['version']}" , log_level="info" , to_terminal=True)
    logger.log(message=f"Recalled: {software['recalled']}" , log_level="info" , to_terminal=True)
    logger.log(message=f"Created at: {software['created_at']}" , log_level="info" , to_terminal=True)
    logger.log(message=f"Updated at: {software['updated_at']}" , log_level="info" , to_terminal=True)


    return software
