from secrets import TOKEN, ADMIN_CHAT_ID
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import subprocess
import os
import getpass
import socket


def admin_only(f):
    def wrapper(bot, update):
        logger.info('chat id: {}'.format(update.message.chat.id))

        if update.message.chat.id != ADMIN_CHAT_ID:
            update.message.reply_text('Nothing here')
            logger.info('text: \'{}\' chat id: {}'.format(update.message.text,
                                                          update.message.chat.id))
            return
        f(bot, update)

    return wrapper


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


@admin_only
def start(bot, update):
    update.message.reply_text('Hi, admin!')


@admin_only
def help(bot, update):
    update.message.reply_text('Here is some help')


CMD_LS = 'ls'
CMD_CD = 'cd'
CMD_CAT = 'cat'
CMD_STAT = 'stat'
SUPPORTED_COMMANDS = [CMD_LS, CMD_CD, CMD_CAT, CMD_STAT]

def process_command(cmd):
    if not cmd[0] in SUPPORTED_COMMANDS:
        return False

    output = ['<b>{}@{}</b>'.format(getpass.getuser(), socket.gethostname())]
    output.append('cur_dir')

    if(cmd[0] == CMD_CD):
        try:
            os.chdir(' '.join(cmd[1:]))
        except FileNotFoundError as e:
            output.append(str(e))
    else:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        cmd_output, cmd_error = process.communicate()
        cmd_output = cmd_output.decode("utf-8")
        cmd_error = cmd_error.decode("utf-8")
        if cmd_output:
            output.append(cmd_output)
            logger.info(cmd_output)
        if cmd_error:
            output.append(cmd_error)
            logger.error(cmd_error)

    output[1] = '<b>{}</b>'.format(os.getcwd())
    output = '\n'.join(output)

    return output

@admin_only
def echo(bot, update):
    """

    :param bot: Bot
    :param update: Update
    :return:
    """

    cmd = update.message.text.split()
    output = process_command(cmd)
    if output:
        update.message.reply_text(output, parse_mode='HTML')
    else:
        update.message.reply_text('Unsupported command: {}'.format(cmd[0]))


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
