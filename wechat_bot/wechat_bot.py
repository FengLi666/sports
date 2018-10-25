from gevent import monkey

monkey.patch_all()
from wxpy import *

bot = Bot()
print = bot.file_helper.send
from mysports.run import run


@bot.register(bot.file_helper, except_self=False)
def bot_start_run(msg):
    if (msg.text == '高校体育'):
        bot.file_helper.send("使用方法：帮肥宅跑步 账号 密码")
    elif (msg.text.startswith("帮肥宅跑步")):
        print("开始跑步...")
        userid = msg.split(' ')[1]
        passwd = msg.split(' ')[2]
        run(userid, passwd)


if __name__ == '__main__':
    bot.join()
