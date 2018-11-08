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
        self.token = token
        self.timer = RepeatEvery(1, self.timer_func)
        self.sender = SendMsg(token, 134751583)
        self.worker = Worker()
        self.updater = Updater(token=token)
        self.add_bot_handlers()
        self.start_timer()
        logger.info('Start polling')
        self.updater.start_polling(poll_interval=2, timeout=30, read_latency=5)
        self.updater.idle()

    def add_bot_handlers(self):
        dp = self.updater.dispatcher
        dp.add_handler(CommandHandler('show', self.show))
        dp.add_handler(CommandHandler('start', self.start))
        dp.add_error_handler(self.error)

    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text=str(update.message.chat_id))

    def show(self, bot, update):
        logger.info('show')
        status = self.worker.status()
        logger.info('{}'.format(status))
        if status:
            bot.send_message(chat_id=update.message.chat_id, text=status)
        else:
            bot.send_message(chat_id=update.message.chat_id, text='none')

    @staticmethod
    def error(bot, update, err):
        logger.warning('Update "%s" caused error "%s"' % (update, err))

    def start_timer(self):
        self.sender.push('Запуск процесса')
        self.timer.start()

    def timer_func(self):
        self.sync_timer(1)
        result = self.worker.status()
        if result:
            self.sender.push(result)

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
