import gevent
from gevent import monkey

monkey.patch_all()
from logging import Logger
from wxpy import *
from traceback import print_exc
import builtins

bot = Bot(cache_path=True, console_qr=2)
logger = Logger('sports')


def wxprint(my_bot):
    def func(x):
        logger.warning(x)
        gevent.spawn(my_bot.file_helper.send, x)

    return func


builtins.print = wxprint(bot)

from mysports.run import run


@bot.register(bot.file_helper, except_self=False)
def bot_start_run(msg):
    try:
        if (msg.text == '高校体育'):
            bot.file_helper.send("使用方法：帮肥宅跑步 账号 密码")
        elif (msg.text.startswith("帮肥宅跑步")):
            print("开始跑步...")
            userid = msg.text.split(' ')[1]
            passwd = msg.text.split(' ')[2]
            run(userid, passwd, rg=(1, 2))
        else:
            print('滚一边玩去')
    except Exception as e:
        print_exc(e)


if __name__ == '__main__':
    bot.join()
