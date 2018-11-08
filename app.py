from bot import TelegramBot
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def main():
    TelegramBot('421756283:AAFMiDEYT3bEQ5y07D1GitwBejbjynpIN7c')


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error('Exit program.. Main thread error: {}'.format(e))
        exit()
