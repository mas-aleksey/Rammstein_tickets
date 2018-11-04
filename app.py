from bot import TelegramBot
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    TelegramBot('511667757:AAHMM0NRF4njpnuFbF_pWRQhqF3w5Aojjw8')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(e)
        exit()
