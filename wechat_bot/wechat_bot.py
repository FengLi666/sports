from gevent import monkey
monkey.patch_all()
from wxpy import *
from traceback import print_exc
import builtins


bot = Bot()
builtins.print = bot.file_helper.send

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
            run(userid, passwd)
        else:
            print('滚一边玩去')
    except Exception as e:
        print_exc(e)


if __name__ == '__main__':
    bot.join()
