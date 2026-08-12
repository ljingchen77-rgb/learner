"""Generate a polished one-page Chinese academic CV for supervisor outreach."""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "Liu-Jingchen-Academic-Resume-CN.pdf"
pdfmetrics.registerFont(TTFont("YaHei", r"C:\Windows\Fonts\msyh.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("YaHeiBold", r"C:\Windows\Fonts\msyhbd.ttc", subfontIndex=0))

W, H = A4
NAVY = colors.HexColor("#0B1630")
BLUE = colors.HexColor("#1769E0")
VIOLET = colors.HexColor("#7357E8")
CYAN = colors.HexColor("#21BED0")
TEXT = colors.HexColor("#172033")
MUTED = colors.HexColor("#667085")
PALE = colors.HexColor("#F3F6FB")
LINE = colors.HexColor("#DDE5F0")


def style(size=8.2, leading=12.5, color=TEXT, bold=False, align=0):
    return ParagraphStyle(
        "cv", fontName="YaHeiBold" if bold else "YaHei", fontSize=size,
        leading=leading, textColor=color, alignment=align,
    )


def paragraph(pdf, text, x, top, width, pstyle):
    block = Paragraph(text, pstyle)
    _, height = block.wrap(width, H)
    block.drawOn(pdf, x, top - height)
    return top - height


def section(pdf, index, title, x, y, width):
    pdf.setFillColor(BLUE)
    pdf.roundRect(x, y - 0.8 * mm, 7 * mm, 5.2 * mm, 2.6 * mm, fill=1, stroke=0)
    pdf.setFillColor(colors.white)
    pdf.setFont("YaHeiBold", 6.8)
    pdf.drawCentredString(x + 3.5 * mm, y + 0.5 * mm, index)
    pdf.setFillColor(NAVY)
    pdf.setFont("YaHeiBold", 10.5)
    pdf.drawString(x + 10 * mm, y, title)
    pdf.setStrokeColor(LINE)
    pdf.line(x + 35 * mm, y + 1.2 * mm, x + width, y + 1.2 * mm)
    return y - 7 * mm


pdf = canvas.Canvas(str(OUTPUT), pagesize=A4)
pdf.setTitle("刘靖臣 - 学术简历")
pdf.setAuthor("刘靖臣")
pdf.setFillColor(colors.white)
pdf.rect(0, 0, W, H, fill=1, stroke=0)

# Header
pdf.setFillColor(NAVY)
pdf.rect(0, H - 45 * mm, W, 45 * mm, fill=1, stroke=0)
pdf.setFillColor(VIOLET)
pdf.circle(-6 * mm, H + 1 * mm, 27 * mm, fill=1, stroke=0)
pdf.setFillColor(BLUE)
pdf.circle(W - 2 * mm, H - 4 * mm, 24 * mm, fill=1, stroke=0)
pdf.setFillColor(CYAN)
pdf.circle(W - 34 * mm, H + 4 * mm, 11 * mm, fill=1, stroke=0)

x = 15 * mm
pdf.setFillColor(colors.white)
pdf.setFont("YaHeiBold", 25)
pdf.drawString(x, H - 17 * mm, "刘靖臣")
pdf.setFillColor(colors.HexColor("#D7E2F2"))
pdf.setFont("YaHei", 8.4)
pdf.drawString(x, H - 26 * mm, "清华大学工程物理系 · 核工程与核技术")
pdf.setFillColor(CYAN)
pdf.setFont("YaHeiBold", 8.2)
pdf.drawString(x, H - 34 * mm, "研究定位  |  磁约束核聚变 · 托卡马克边缘与偏滤器物理")

cx = 119 * mm
pdf.setFillColor(colors.HexColor("#E2EAF5"))
pdf.setFont("YaHei", 6.8)
pdf.drawString(cx, H - 17 * mm, "邮箱  jingchen0911@outlook.com")
pdf.drawString(cx, H - 24 * mm, "主页  ljingchen77-rgb.github.io/learner/")
pdf.drawString(cx, H - 31 * mm, "GitHub  github.com/ljingchen77-rgb")
pdf.setFillColor(CYAN)
pdf.roundRect(cx, H - 41 * mm, 59 * mm, 6.5 * mm, 3.25 * mm, fill=1, stroke=0)
pdf.setFillColor(NAVY)
pdf.setFont("YaHeiBold", 6.8)
pdf.drawCentredString(cx + 29.5 * mm, H - 38.8 * mm, "2026 本科毕业 · 即将攻读核能科学与技术硕士")

x, width, y = 15 * mm, W - 30 * mm, H - 54 * mm

# Education, courses and honors are placed first for a complete student profile.
y = section(pdf, "01", "教育背景与专业基础", x, y, width)
edu_h = 38 * mm
pdf.setFillColor(PALE)
pdf.roundRect(x, y - edu_h, width, edu_h, 4 * mm, fill=1, stroke=0)
ex, ey, ew = x + 6 * mm, y - 7 * mm, width - 12 * mm
ey = paragraph(pdf, "<b>清华大学 · 工程物理系</b>　核工程与核技术本科　2022.09 - 2026.06", ex, ey, ew, style(8.8, 13, NAVY, True)) - 2 * mm
ey = paragraph(pdf, "<b>升学去向</b>　核工业西南物理研究院 · 核能科学与技术硕士（即将入学）", ex, ey, ew, style(7.6, 11.5)) - 2 * mm
ey = paragraph(pdf, "<b>相关课程</b>　计算机模拟物理 · 材料学导论 · 同位素分离原理 · 级联理论", ex, ey, ew, style(7.6, 11.5)) - 2 * mm
paragraph(pdf, "<b>荣誉奖项</b>　<font color='#1769E0'>国防科技奖学金 · 志愿奖学金 · 社工奖学金</font>", ex, ey, ew, style(7.6, 11.5))
y -= edu_h + 6 * mm

# Research is intentionally concise: question, work and output.
y = section(pdf, "02", "研究经历", x, y, width)
card_h = 47 * mm
pdf.setFillColor(PALE)
pdf.roundRect(x, y - card_h, width, card_h, 4 * mm, fill=1, stroke=0)
pdf.setFillColor(CYAN)
pdf.roundRect(x, y - card_h, 2.8 * mm, card_h, 1.4 * mm, fill=1, stroke=0)
px, py, pw = x + 7 * mm, y - 7 * mm, width - 14 * mm
pdf.setFillColor(BLUE)
pdf.setFont("YaHeiBold", 6.8)
pdf.drawString(px, py, "2026  |  独立研究尝试 · 受控合成数据")
py -= 6 * mm
py = paragraph(pdf, "跨托卡马克破裂预测中的分布偏移诊断", px, py, pw, style(11.5, 15.5, NAVY, True)) - 2 * mm
research_rows = [
    ("研究问题", "区分预测模型跨运行域失效是源于测量数据差异，还是潜在破裂规律变化。"),
    ("主要工作", "使用 Python 设计成对受控实验，完成 30 组重复、统计区间及多项敏感性检验。"),
    ("阶段产出", "形成可复现实验代码、结果审计及 IEEE TPS 格式中英文论文工作稿；尚待真实多装置数据验证。"),
]
for label, body in research_rows:
    pdf.setFillColor(VIOLET)
    pdf.roundRect(px, py - 3.8 * mm, 18 * mm, 5.2 * mm, 2.6 * mm, fill=1, stroke=0)
    pdf.setFillColor(colors.white)
    pdf.setFont("YaHeiBold", 6.3)
    pdf.drawCentredString(px + 9 * mm, py - 2.1 * mm, label)
    py = paragraph(pdf, body, px + 22 * mm, py + 0.7 * mm, pw - 22 * mm, style(7.2, 10.6)) - 1.8 * mm
y -= card_h + 4 * mm

# Undergraduate thesis - concise supporting project
paper_h = 21 * mm
pdf.setFillColor(colors.white)
pdf.setStrokeColor(LINE)
pdf.roundRect(x, y - paper_h, width, paper_h, 4 * mm, fill=1, stroke=1)
pdf.setFillColor(VIOLET)
pdf.roundRect(x, y - paper_h, 2.8 * mm, paper_h, 1.4 * mm, fill=1, stroke=0)
px, py, pw = x + 7 * mm, y - 6.5 * mm, width - 14 * mm
pdf.setFillColor(BLUE)
pdf.setFont("YaHeiBold", 6.6)
pdf.drawString(px, py, "2025 - 2026  |  本科综合论文训练")
py -= 5.5 * mm
py = paragraph(pdf, "托卡马克等离子体 EUV 辐射研究", px, py, pw, style(9.3, 12.5, NAVY, True)) - 1 * mm
paragraph(
    pdf,
    "完成文献梳理、数量级估算与分层效率模型，讨论 13.5 nm EUV 辐射的系统约束和研究价值。",
    px, py, pw, style(7.1, 10.3),
)
y -= paper_h + 4 * mm

# Internship receives its own prominent section.
y = section(pdf, "03", "生产实习与科研实践", x, y, width)
pdf.setFillColor(BLUE)
pdf.setFont("YaHeiBold", 6.8)
pdf.drawString(x, y, "2025.06.23 - 2025.07.25")
pdf.setFillColor(NAVY)
pdf.setFont("YaHeiBold", 8.5)
pdf.drawString(x + 42 * mm, y, "核工业西南物理研究院 · 材料研究所（练有运老师指导）")
y = paragraph(
    pdf,
    "参与面向等离子体材料及 W/CuCrZr 水冷模块热负荷研究；学习 20 MW 电子束平台加载、红外测温、吸收功率计算及材料表征方法，结合 9/15 MW·m<super>-2</super> 循环工况分析连接界面、钨再结晶与表面损伤，并完成生产实习报告。",
    x + 42 * mm, y - 5.5 * mm, width - 42 * mm, style(7.15, 10.8),
) - 6 * mm

y = section(pdf, "04", "校园经历、技能与兴趣", x, y, width)
skills = [
    ("经历", "班级科研委员 · 系学生会/系团委 · 校团委 1911 星球 · 乡村振兴与“音禾计划”志愿服务"),
    ("技能", "Python 数据分析与可视化 · MATLAB 数值计算 · 文献调研 · 技术报告与论文写作"),
    ("兴趣", "篮球 · 架子鼓八级 · 葫芦丝七级"),
]
for label, value in skills:
    pdf.setFillColor(BLUE)
    pdf.setFont("YaHeiBold", 7)
    pdf.drawString(x, y, label)
    y = paragraph(pdf, value, x + 18 * mm, y + 1.4 * mm, width - 18 * mm, style(7.05, 10.5)) - 1.6 * mm

pdf.setStrokeColor(LINE)
pdf.line(x, 10.5 * mm, x + width, 10.5 * mm)
pdf.setFillColor(MUTED)
pdf.setFont("YaHei", 5.8)
pdf.drawString(x, 6.7 * mm, "Academic CV · Fusion & Plasma Research")
pdf.drawRightString(x + width, 6.7 * mm, "2026 · 刘靖臣")
pdf.save()
print(OUTPUT)
