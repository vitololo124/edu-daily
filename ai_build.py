from datetime import date
import os
from openai import OpenAI  # 导入OpenAI SDK

# 1. 初始化OpenAI客户端（从环境变量读取密钥，安全无泄露）
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")  # 关键：用环境变量获取密钥，不在代码中明文写
)

# 2. 今日日期
today = date.today().strftime("%Y-%m-%d")

# 3. 调用OpenAI生成教育日报内容（可自定义prompt）
def generate_edu_daily():
    """调用OpenAI生成教育行业日报内容"""
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 可选：gpt-4o（效果更好，成本稍高）
            messages=[
                {"role": "system", "content": """你是教育行业资深分析师，擅长总结行业动态。
                请生成一篇结构化的教育行业日报，包含3个板块：今日速览、政策动态、行业趋势。
                语言简洁专业，每条内容不超过2行，整体控制在300字以内。"""},
                {"role": "user", "content": f"生成{today}的教育行业日报"}
            ],
            temperature=0.7,  # 控制内容多样性
            max_tokens=300    # 控制输出长度
        )
        return response.choices[0].message.content
    except Exception as e:
        # 异常处理：避免因API问题导致整个脚本失败
        print(f"⚠️ AI调用警告：{str(e)}")
        return """### 今日速览
1. 教育数字化转型加速，AI教学工具广泛应用
2. 职业教育校企合作深化，实训基地建设扩容
3. 家庭教育指导服务纳入学校课后服务内容

### 政策动态
教育部发布新版《义务教育课程标准》，强化核心素养培养

### 行业趋势
素质教育与学科教育融合，STEAM教育市场持续增长"""

# 4. 生成完整HTML页面
def build_html(content):
    """将AI生成的内容嵌入HTML模板"""
    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>教育行业日报 | {today}</title>
  <style>
    *{{margin:0;padding:0;box-sizing:border-box;font-family:微软雅黑}}
    body{{background:#f7f8fa;color:#333;padding:30px;max-width:1000px;margin:0 auto;line-height:1.8}}
    .header{{text-align:center;margin-bottom:30px;padding-bottom:20px;border-bottom:1px solid #eee}}
    h1{{font-size:26px;color:#222}}
    .time{{color:#666;margin-top:8px}}
    .block{{background:#fff;padding:24px;margin-bottom:20px;border-radius:12px;box-shadow:0 2px 8px rgba(0,0,0,0.06)}}
    .block h2{{font-size:18px;color:#1f2937;border-left:4px solid #409eff;padding-left:12px;margin-bottom:15px}}
    .content{{font-size:15px;color:#444;white-space:pre-wrap}}  <!-- 保留换行格式 -->
  </style>
</head>
<body>
  <div class="header">
    <h1>教育行业日报</h1>
    <div class="time">更新日期：{today} · AI智能分析</div>
  </div>

  <div class="block">
    <h2>今日速览</h2>
    <div class="content">{content.split('### 今日速览')[1].split('### 政策动态')[0].strip()}</div>
  </div>

  <div class="block">
    <h2>政策动态</h2>
    <div class="content">{content.split('### 政策动态')[1].split('### 行业趋势')[0].strip()}</div>
  </div>

  <div class="block">
    <h2>行业趋势</h2>
    <div class="content">{content.split('### 行业趋势')[1].strip()}</div>
  </div>
</body>
</html>
"""
    return html

# 5. 主执行流程
if __name__ == "__main__":
    print("🚀 开始生成教育行业日报...")
    # 生成内容（AI或备用内容）
    daily_content = generate_edu_daily()
    # 构建HTML
    html_content = build_html(daily_content)
    # 强制写入文件（确保编码正确）
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("✅ 网页文件已成功生成！")
    print("📄 内容预览：")
    print(daily_content)
