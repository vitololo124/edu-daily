import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, date
import os

os.makedirs("data", exist_ok=True)
today = date.today().strftime("%Y-%m-%d")

# 教育行业核心新闻源（自动抓取这些网站的最新资讯）
sources = [
    {"name": "教育部官网", "url": "http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/s5987/"},
    {"name": "中国教育报", "url": "https://www.jyb.cn/edu/xw"},
    {"name": "多知网", "url": "https://www.duozhi.com/news/"},
    {"name": "芥末堆", "url": "https://www.jiemodui.com/news"},
]

news_list = []

# 抓取单网站新闻的函数
def get_news(name, url):
    try:
        # 模拟浏览器访问，避免被屏蔽
        headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
        res = requests.get(url, headers=headers, timeout=10)
        res.encoding = "utf-8"  # 确保中文显示正常
        soup = BeautifulSoup(res.text, "html.parser")
        # 提取前8条新闻链接（避免抓取过多）
        items = soup.find_all("a")[:8]
        for i in items:
            title = i.get_text(strip=True)  # 提取标题并去除空格
            link = i.get("href", "")        # 提取链接
            # 只保留有效标题（长度>8字）
            if len(title) > 8:
                news_list.append({
                    "source": name,
                    "title": title,
                    "url": link,
                    "date": today
                })
    except Exception as e:
        print(f"{name} 抓取异常：{e}")  # 抓取失败时输出错误信息

# 遍历所有新闻源，执行抓取
for s in sources:
    get_news(s["name"], s["url"])

# 保存抓取结果到data文件夹
with open("data/raw_news.json", "w", encoding="utf-8") as f:
    json.dump(news_list, f, ensure_ascii=False, indent=2)
