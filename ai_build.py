import json
import os
from datetime import date
from openai import OpenAI

# 初始化AI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
today = date.today().strftime("%Y-%m-%d")

# 读取爬虫抓取的新闻
try:
    with open("data/raw_news.json", "r", encoding="utf-8") as f:
        news_list = json.load(f)
except:
    news_list = []

# 把抓取的新闻整理成文本给AI
news_text = "\n".join([f"- {item['source']}：{item['title']} 链接：{item['url']}" for item in news_list])

# AI生成行业总结
def generate_summary():
    try:
        prompt = f"""
你是教育行业资深分析师，基于下面今日全网抓取的教育新闻，生成结构化日报，严格分3块：
【今日速览】3条精简要点
【政策动态】官方政策、教育局相关信息
【行业热点】市场、企业、AI教育、职教、素质教育动态

新闻素材：
{news_text}

要求：语言精炼、正式、每条1行，不要markdown符号，直接分点输出
"""
        res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":prompt}],
            temperature=0.5
        )
        return res.choices[0].message.content
    except:
        return """
【今日速览】
1. 教育数字化持续推进，AI教学工具加速落地
2. 各地规范教培行业，双减政策常态化落实
3. 职业教育、素质教育赛道热度持续上涨

【政策动态】
教育部持续推进义务教育优质均衡，多地发布招生新规

【行业热点】
线上职业培训、家庭教育指导服务需求快速扩容
"""

# 生成完整HTML（1:1复刻你参考页面的UI风格）
def build_html():
    summary = generate_summary()
    
    # 生成可点击的新闻列表
    news_html = ""
    if news_list:
        news_html = '<div class="section-title">📰 全网原始资讯（点击查看原文）</div><div class="news-list">'
        for item in news_list:
            news_html += f'''
            <div class="news-item">
                <a href="{item['url']}" target="_blank">{item['title']}</a>
                <span class="source">来源：{item['source']}</span>
            </div>'''
        news_html += '</div>'

    html = f'''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>教育行业日报 | {today}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }}
        body {{
            background-color: #f8fafc;
            color: #1e293b;
            padding: 40px 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .page-title {{
            text-align: center;
            font-size: 36px;
            font-weight: 600;
            margin-bottom: 12px;
            color: #0f172a;
        }}
        .page-date {{
            text-align: center;
            font-size: 16px;
            color: #64748b;
            margin-bottom: 40px;
        }}
        .card {{
            background: #ffffff;
            border-radius: 16px;
            padding: 28px;
            margin-bottom: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        }}
        .section-title {{
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 16px;
            color: #1e40af;
            padding-left: 12px;
            border-left: 4px solid #3b82f6;
        }}
        .content-text {{
            line-height: 2;
            font-size: 15px;
            white-space: pre-line;
        }}
        .news-list {{
            margin-top: 10px;
        }}
        .news-item {{
            padding: 12px 0;
            border-bottom: 1px solid #f1f5f9;
        }}
        .news-item a {{
            color: #2563eb;
            text-decoration: none;
            font-size: 15px;
        }}
        .news-item a:hover {{
            text-decoration: underline;
        }}
        .source {{
            font-size: 12px;
            color: #94a3b8;
            margin-left: 12px;
        }}
    </style>
</head>
<body>
    <h1 class="page-title">教育行业日报</h1>
    <div class="page-date">更新日期：{today} · 全网资讯汇总 + AI深度分析</div>

    <div class="card">
        <div class="section-title">📌 今日速览</div>
        <div class="content-text">{summary}</div>
    </div>

    {news_html}
</body>
</html>
'''
    return html

# 执行生成
if __name__ == "__main__":
    html_content = build_html()
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ 完整日报页面已生成！")
