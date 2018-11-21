# 跑步是不可能跑步的
高校体育app自动跑步

仅供交流学习使用，not for evil use :)

使用了百度地图api自动寻路（~~虽然可能很绕~~ 已经挺像真人跑的喽 :) ）

![image](https://user-images.githubusercontent.com/19814411/47697310-6929c780-dc45-11e8-92eb-88f9f7b6368d.png)
![image](https://user-images.githubusercontent.com/19814411/47573220-55ddda00-d96f-11e8-85e6-5db1e790ed33.png)


## 使用方法

有 **本地直接运行** 和 **运行微信机器人** 两种方法， **微信机器人** 只建议有服务器的同学使用

### 本地直接运行

## windows
1. 下载 /dist/run.exe， 运行，输入账号密码即可完成一次锻炼（为了避免封号， 完全模拟了跑步流程，耗时较长，未完成前不要关闭）

## linux/macos
```
git clone https://github.com/FengLi666/sports.git
cd sports
pip3 install -r requirement.txt
export PYTHONPATH='.'
python3 ./mysports/run.py

```
输入账号密码
默认情况下跑步数据在一段时间后才会提交给app服务器(即你要保持这个进程一直运行）
如果想立即提交跑步数据
可以使用如下命令
```
python3 ./mysports/run.py --debug True
```

## 运行微信机器人
```
git clone https://github.com/FengLi666/sports.git
cd sports
pip3 install -r requirement.txt
export PYTHONPATH='.'
python3 ./wechat_bot/wechat_bot.py
```
~~具体见代码~~

---

感谢 @RyuBAI 
