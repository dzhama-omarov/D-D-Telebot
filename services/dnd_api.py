import requests
from loguru import logger

# Базовый URL для API
BASE_URL = 'https://www.dnd5eapi.co/api/'


def get_from_dnd_api(endpoint: str = '') -> tuple[int, list]:
    """
    Делает GET-запрос к D&D 5e API и возвращает количество и
    список результатов.

    :param endpoint: Конечная точка API (например, 'spells', 'classes').
    :return: Кортеж, содержащий количество результатов (int) и список
    (list).
    :raises: Exception, если статус-код ответа не равен 200.
    """
    url = '{}/{}'.format(BASE_URL.rstrip('/'), endpoint)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'count' in data and 'results' in data:
                logger.info('Успешный запрос к {}. Получено {} записей.'
                            .format(endpoint, data['count']))
                return data['count'], data['results']
            else:
                logger.error('Некорректный формат данных при запросе к {}.'
                             .format(endpoint))
                raise ValueError('Некорректный формат данных в ответе API.')
        else:
            logger.error('Ошибка API: статус-код {} при запросе к {}.'
                         .format(response.status_code, endpoint))
            raise Exception('Ошибка API: статус-код {}'
                            .format(response.status_code))
    except Exception as e:
        logger.exception('Исключение при запросе к {}: {}'
                         .format(endpoint, e))
        raise
