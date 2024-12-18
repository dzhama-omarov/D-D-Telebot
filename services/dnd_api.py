import requests
from loguru import logger

# The base URL for the API
BASE_URL = 'https://www.dnd5eapi.co/api/'


def get_from_dnd_api(endpoint: str = '') -> tuple[int, list]:
    """
Makes a GET request to the D&D 5e API and returns the number and
list of results.

    :param endpoint: API endpoint (for example, 'spells', 'classes').
    :return: A tuple containing the number of results (int) and a list
(list).
    :raises: Exception if the response status code is not 200.
"""
url = '{}/{}'.format(BASE_URL.rstrip('/'), endpoint)
try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'count' in data and 'results' in data:
                logger.info ('Successful request to {}. {} records received.'
                            .format(endpoint, data['count']))
                return data['count'], data['results']
            else:
logger.error('Invalid data format when requesting to {}.'
.format(endpoint))
raise ValueError('Invalid data format in the API response.')
        else:
            logger.error('API error: status code {} when requesting to {}.'
.format(response.status_code, endpoint))
raise Exception('API error: status code {}'
                            .format(response.status_code))
    except Exception as e:
        logger.exception('Exception when requesting to {}: {}'
                         .format(endpoint, e))
        raise
