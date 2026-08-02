# -*- coding: utf-8 -*-
"""
fetch_weather.py —— 广州天气数据获取脚本
============================================
这个脚本的作用：
1. 向 Open-Meteo 免费天气接口发起请求（不需要注册、不需要 API Key）
2. 获取广州未来 7 天的最高温、最低温和降水量
3. 把数据整理成简洁的 JSON 格式，保存到同目录下的 guangzhou_weather.json

运行方式（在终端执行）：
    python fetch_weather.py

运行成功后，会在当前目录生成一个 guangzhou_weather.json 文件，
index.html 网页就会读取这个文件来画图表。
"""

# ------------------- 第一步：导入需要的库 -------------------
# json：Python 自带的库，用来把数据保存成 JSON 格式文件
import json

# datetime：Python 自带的库，用来获取"当前时间"，显示数据更新时间
from datetime import datetime, timezone, timedelta

# requests：第三方库，用来向网站发送网络请求。
# 如果运行时报错 "No module named 'requests'"，
# 请在终端先执行：pip install requests
import requests


# ------------------- 第二步：定义一些固定信息 -------------------
# 广州的经纬度（纬度、经度），Open-Meteo 靠这两个数字定位城市
LATITUDE = 23.1291
LONGITUDE = 113.2644

# Open-Meteo 免费天气接口的地址（固定不变）
API_URL = "https://api.open-meteo.com/v1/forecast"

# 输出文件的名字（放在脚本同目录下）
OUTPUT_FILE = "guangzhou_weather.json"

# 中国标准时间（东八区，即北京时间）的时区对象
# 因为服务器时间可能是 UTC，我们需要手动换算成北京时间来显示
BEIJING_TZ = timezone(timedelta(hours=8))


def fetch_weather():
    """
    主函数：获取天气数据并保存成 JSON 文件
    （函数就像一个小工厂，把它要做的事情都装在里面，
      程序从最下面的 if __name__ == '__main__' 开始执行这个函数）
    """

    # ---------- 第 1 步：准备请求参数 ----------
    # params 是一个"字典"（Python 里用 { } 表示，里面是一组"键: 值"），
    # 这些参数会作为网址后面的 ?xxx=yyy 部分发送给服务器，告诉它我们想要什么数据
    params = {
        # 城市经纬度
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        # 需要的每日数据：最高温、最低温、降水量
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        # 未来预报几天（7 天）
        "forecast_days": 7,
        # 时区：让服务器直接返回北京时间
        "timezone": "Asia/Shanghai",
    }

    print("正在向 Open-Meteo 请求广州未来 7 天天气数据...")

    # ---------- 第 2 步：发送请求并获取响应 ----------
    try:
        # requests.get 就是"向服务器发起一次 GET 请求"
        # params=params 表示把这些参数附加到网址后面
        # timeout=30 表示最多等 30 秒，防止网络卡住导致程序一直停在这里
        response = requests.get(API_URL, params=params, timeout=30)

        # raise_for_status() 的意思是：如果服务器返回了错误状态码
        # （比如 404 网页不存在、500 服务器出错），就抛出异常让我们知道
        response.raise_for_status()

        # .json() 会把服务器返回的 JSON 文本，解析成 Python 能直接使用的字典
        data = response.json()
        print("请求成功！正在整理数据...")

    except requests.exceptions.RequestException as e:
        # 网络出错（比如没网、接口临时故障）时会走到这里
        # 打印错误信息并终止程序，方便新手看到具体原因
        print("请求失败，请检查网络连接。错误信息：")
        print(e)
        return

    # ---------- 第 3 步：从服务器数据中提取我们需要的部分 ----------
    # 服务器返回的数据结构里，天气预报数据都在 data["daily"] 里，
    # 它是一个字典，里面有三个列表（数组）：
    #   time               -> 每天的日期，例如 ["2026-08-02", "2026-08-03", ...]
    #   temperature_2m_max -> 每天的最高温列表
    #   temperature_2m_min -> 每天的最低温列表
    #   precipitation_sum  -> 每天的降水量列表
    daily = data["daily"]
    dates = daily["time"]                 # 日期列表
    temp_max_list = daily["temperature_2m_max"]  # 最高温列表
    temp_min_list = daily["temperature_2m_min"]  # 最低温列表
    precip_list = daily["precipitation_sum"]     # 降水量列表

    # ---------- 第 4 步：把数据整理成简洁的 JSON 结构 ----------
    # 我们要生成的目标结构：
    # {
    #   "city": "Guangzhou",
    #   "updated_at": "当前时间",
    #   "data": [
    #       {"date": "2026-08-02", "temp_max": 29.0, "temp_min": 25.0, "precipitation": 0.0},
    #       ...
    #   ]
    # }
    #
    # 下面这行是"列表推导式"，等价于用 for 循环逐个把每一天的数据装进字典。
    # 它遍历 dates 的索引（range(len(dates))），把每一天的
    # 日期、最高温、最低温、降水量装进一个小字典，收集成一个大列表。
    # 注：range(len(dates)) 会生成 0,1,2,... 直到天数减一，
    # 这样就能用同一个下标 i 同时取出同一天的日期和温度。
    weather_list = [
        {
            "date": dates[i],
            "temp_max": temp_max_list[i],
            "temp_min": temp_min_list[i],
            "precipitation": precip_list[i],
        }
        for i in range(len(dates))
    ]

    # 组装成最终要保存的整体结构
    # datetime.now(BEIJING_TZ) 获取当前北京时间
    # strftime("%Y-%m-%d %H:%M:%S") 把时间格式化成"年-月-日 时:分:秒"的字符串
    result = {
        "city": "Guangzhou",
        "updated_at": datetime.now(BEIJING_TZ).strftime("%Y-%m-%d %H:%M:%S"),
        "data": weather_list,
    }

    # ---------- 第 5 步：保存成 JSON 文件 ----------
    try:
        # open() 打开（没有就创建）文件，以"写"模式（"w"）写入
        # encoding="utf-8" 指定用 UTF-8 编码，这样中文等字符不会乱码
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            # json.dump 把 Python 字典保存成 JSON 文本写入文件
            # ensure_ascii=False 允许直接保存中文/符号，而不是转成 \uXXXX
            # indent=2 让 JSON 文件里的内容有缩进，方便人查看
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"成功！天气数据已保存到：{OUTPUT_FILE}")
        print(f"更新时间：{result['updated_at']}")
        print(f"共获取 {len(weather_list)} 天数据，第一天：{dates[0]}，最后一天：{dates[-1]}")

    except OSError as e:
        # 文件写入失败（比如磁盘空间不足、目录没有写权限）会走到这里
        print("保存文件失败：", e)


# ------------------- 程序的真正入口 -------------------
# 这行是 Python 的固定写法：当直接运行这个脚本时，下面的代码才会执行；
# 当这个脚本被其他脚本"导入"时，下面的代码不会执行。
if __name__ == "__main__":
    fetch_weather()
