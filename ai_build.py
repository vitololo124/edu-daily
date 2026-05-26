from datetime import date
import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
today = date.today().strftime("%Y-%m-%d")

def get_content():
    try:
        res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role":"system","content":"你是教育行业分析师，输出简洁教育行业日报，分3块：今日速览、政策动态、行业趋势，简短专业"},
                {"role":"user","content":f"生成{today}教育行业日报"}
            ]
        )
        return res.choices[0].message.content
    except:
        return f"""### 今日速览
教育行业数字化持续推进，AI教学工具普及
### 政策动态
各地落实双减政策，规范校外培训
### 行业趋势
职业教育、素质教育赛道持续扩容"""

html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width">
<title>教育行业日报 | {today}</title>
<style>
body{{background:#f7f8fa;font-family:微软雅黑;padding:30px;max-width:1000px;margin:0 auto}}
.box{{background:#fff;padding:24px;border-radius:12px;margin-bottom:20px;box-shadow:0 2px 8px #eee}}
h1{{text-align:center;color:#222}}
.time{{text-align:center;color:#666;margin-bottom:30px}}
h2{{border-left:4px solid #409eff;padding-left:12px;color:#222}}
</style>
</head>
<body>
<h1>教育行业日报</h1>
<div class="time">{today}</div>
<div class="box">{get_content()}</div>
</body>
</html>
"""

with open("index.html","w",encoding="utf-8") as f:
    f.write(html)
