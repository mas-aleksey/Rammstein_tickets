from telegram.ext import Updater, CommandHandler
from async_task import RepeatEvery
import logging
import datetime
import requests
import time
from worker import Worker

logger = logging.getLogger('Telegram_Bot')


class TelegramBot:
    def __init__(self, token):
        self.timer = RepeatEvery(1, self.timer_func)
        self.token = token
        self.sender = None
        self.worker = None
        self.updater = Updater(token=token)
        self.dp = self.updater.dispatcher
        self.add_bot_handlers()
        self.start_timer()
        logger.info('Start polling')
        self.updater.start_polling(poll_interval=2, timeout=30, read_latency=5)
        self.updater.idle()

    def add_bot_handlers(self):
        self.dp.add_handler(CommandHandler('start', self.start))
        self.dp.add_handler(CommandHandler('help', self.help))
        self.dp.add_handler(CommandHandler('ema', self.show_ema))
        self.dp.add_error_handler(self.error)
        time.sleep(15)

    def start(self, bot, update):
        if not self.sender:
            self.sender = SendMsg(self.token, update.message.chat_id)
        bot.send_message(chat_id=update.message.chat_id, text=str(update.message.chat_id))

    def show_ema(self, bot, update):
        try:
            ema = self.worker.return_ema_format()
        except Exception as e:
            logger.error('get ema error {}'.format(e))
            bot.send_message(chat_id=update.message.chat_id, text='error')
        else:
            bot.send_message(chat_id=update.message.chat_id, text=ema)

    @staticmethod
    def help(bot, update):
        bot.send_message(chat_id=update.message.chat_id, text='help')

    @staticmethod
    def error(bot, update, err):
        logger.warning('Update "%s" caused error "%s"' % (update, err))

    def start_timer(self):
        if not self.worker:
            logger.info('Start process')
            self.worker = Worker()
            self.timer.start()
        else:
            logger.info('Already started')

    def stop_timer(self):
        self.timer.stop()

    def timer_func(self):
        self.sync_timer(1)
        self.worker.process()

    @staticmethod
    def sync_timer(sec):
        while datetime.datetime.now().second != sec:
            time.sleep(1)


class SendMsg:
    def __init__(self, token, chat_id):
        self.token = token
        self.chat_id = chat_id

    def push(self, msg):
        url = '{}{}{}'.format('https://api.telegram.org/bot', self.token, '/sendMessage')
        params = {'chat_id': self.chat_id, 'text': msg}
        requests.post(url, data=params)
