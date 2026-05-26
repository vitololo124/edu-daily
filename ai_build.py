import json
import dashscope
from datetime import date
import os

dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
today = date.today().strftime("%Y-%m-%d")

with open("data/raw_news.json", "r", encoding="utf-8") as f:
    raw = json.load(f)

prompt = f"""
你是教育行业分析师，请把下面新闻整理成【教育行业日报】，严格分4个板块：
1. 今日速览：3-5条一句话核心要点
2. 政策动态：教育政策、教育部通知、新规
3. 行业热点：机构动态、学校、AI教育、双减、职教、素质教育
4. 资本与趋势：投融资、行业研判、未来1-2个月趋势总结

输出格式：纯文本，简洁干练。
新闻素材：{json.dumps(raw, ensure_ascii=False)}
"""

resp = dashscope.Generation.call(
    model="qwen-turbo",
    messages=[{"role":"user","content":prompt}],
    result_format="text"
)
content = resp.output.text

html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>教育行业日报 | {today}</title>
  <style>
    *{{margin:0;padding:0;box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial}}
    body{{background:#f7f8fa;color:#333;padding:20px;max-width:1000px;margin:0 auto;line-height:1.7}}
    .header{{text-align:center;margin-bottom:30px;padding-bottom:20px;border-bottom:1px solid #eee}}
    h1{{font-size:24px;margin-bottom:8px;color:#222}}
    .time{{color:#666;font-size:14px}}
    .block{{background:#fff;padding:20px 24px;margin-bottom:16px;border-radius:12px;box-shadow:0 1px 3px rgba(0,0,0,0.05)}}
    .block h2{{font-size:18px;margin-bottom:12px;color:#1f2937;border-left:4px solid #409eff;padding-left:10px}}
    .content{{font-size:15px;color:#444;white-space:pre-line}}
    .footer{{margin-top:40px;text-align:center;font-size:12px;color:#999}}
  </style>
</head>
<body>
  <div class="header">
    <h1>教育行业日报</h1>
    <div class="time">更新日期：{today} · 全网自动抓取+AI深度分析</div>
  </div>

  <div class="block">
    <h2>今日速览</h2>
    <div class="content">{content}</div>
  </div>

  <div class="footer">
    本日报由系统自动抓取全网教育资讯生成，仅供行业参考
  </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

os.makedirs("archive", exist_ok=True)
with open(f"archive/{today}.html", "w", encoding="utf-8") as f:
    f.write(html)
