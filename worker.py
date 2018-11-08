import requests
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger('Worker')


class Worker:
    def __init__(self):
        self.url = 'https://www.parter.ru/event/rammstein-europe-stadium-tour-2019-втб-аренадинамо-центральный-стадион-11321917/?affiliate=ONE'

    def status(self):
        try:
            r = requests.get(self.url)
        except Exception as e:
            logger.error('request error: {}'.format(e))
        else:
            return self.get_tiket(r.text)

    @staticmethod
    def get_tiket(html):
        soup = BeautifulSoup(html, 'html.parser')
        sizes = soup.find_all('div', class_='fast-booking-font-switch')
        text = sizes[1].text
        logger.info('{}'.format(text))
        if 'билетов' in text:
            return None
        else:
            return text
