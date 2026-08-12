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

# Research snapshot
x, width, y = 15 * mm, W - 30 * mm, H - 53 * mm
pdf.setFillColor(MUTED)
pdf.setFont("YaHeiBold", 6.8)
pdf.drawString(x, y, "RESEARCH SNAPSHOT  /  研究速览")
y -= 4 * mm
gap = 3 * mm
card_w = (width - 3 * gap) / 4
snapshots = [
    ("30 x 500", "独立群体 × 每域放电"),
    ("0.281 - 0.301", "共享机制 AUC 恢复"),
    ("0.149 - 0.178", "机制变化导致恢复损失"),
    ("95% CI", "配对统计与稳健性检验"),
]
for i, (value, label) in enumerate(snapshots):
    sx = x + i * (card_w + gap)
    pdf.setFillColor(PALE)
    pdf.roundRect(sx, y - 15 * mm, card_w, 15 * mm, 3 * mm, fill=1, stroke=0)
    pdf.setFillColor(BLUE if i < 2 else VIOLET)
    pdf.setFont("YaHeiBold", 10.5 if i != 2 else 9.2)
    pdf.drawString(sx + 4 * mm, y - 6 * mm, value)
    pdf.setFillColor(MUTED)
    pdf.setFont("YaHei", 6.5)
    pdf.drawString(sx + 4 * mm, y - 11.5 * mm, label)
y -= 23 * mm

# Profile and education
y = section(pdf, "01", "研究画像", x, y, width)
y = paragraph(
    pdf,
    "以聚变等离子体与工程系统之间的耦合问题为兴趣核心。具备从跨领域文献中提取关键参数、建立数量级模型、比较技术路线并形成技术报告的完整训练；希望在硕士阶段继续深入托卡马克边缘等离子体、偏滤器及等离子体材料问题。",
    x, y, width, style(8.1, 12.8),
) - 4 * mm

y = section(pdf, "02", "教育与研究方向", x, y, width)
y = paragraph(
    pdf,
    "<b>清华大学 · 工程物理系</b>　核工程与核技术本科　2022.09 - 2026.06<br/>"
    "<b>核工业西南物理研究院</b>　核能科学与技术硕士（即将入学）<br/>"
    "<font color='#1769E0'>关键词　磁约束核聚变 / 托卡马克 / 偏滤器 / 高 Z 杂质输运 / 等离子体材料</font>",
    x, y, width, style(8, 13),
) - 4 * mm

# Main research project
y = section(pdf, "03", "代表性研究", x, y, width)
card_h = 69 * mm
pdf.setFillColor(PALE)
pdf.roundRect(x, y - card_h, width, card_h, 4 * mm, fill=1, stroke=0)
pdf.setFillColor(CYAN)
pdf.roundRect(x, y - card_h, 2.8 * mm, card_h, 1.4 * mm, fill=1, stroke=0)
px, py, pw = x + 7 * mm, y - 7 * mm, width - 14 * mm
pdf.setFillColor(BLUE)
pdf.setFont("YaHeiBold", 6.8)
pdf.drawString(px, py, "2026  |  独立研究尝试 · 受控合成数据 · IEEE TPS 论文工作稿")
py -= 6.5 * mm
py = paragraph(pdf, "跨托卡马克破裂预测中的分布偏移诊断", px, py, pw, style(12.5, 17, NAVY, True)) - 1 * mm
py = paragraph(pdf, "研究目标：解释特征对齐何时有效，以及潜在风险机制变化为何限制跨域恢复", px, py, pw, style(6.8, 10.5, MUTED)) - 3 * mm
research_rows = [
    ("受控设计", "固定观测、噪声与放电划分，仅改变潜在风险机制；构造共享机制与机制变化的成对实验。"),
    ("分析方法", "使用 Wasserstein-1、特征删除、均值-方差对齐与 CORAL；采用放电级无泄漏划分。"),
    ("主要结果", "30 个独立群体、每域 500 炮下，共享机制时恢复 0.281-0.301 AUC；机制变化时明显受限。"),
    ("稳健审计", "以独立校准集、参数扫描、分类器与阈值敏感性检验边界；完成代码-结果-论文映射。"),
]
for label, body in research_rows:
    pdf.setFillColor(VIOLET)
    pdf.roundRect(px, py - 3.8 * mm, 18 * mm, 5.2 * mm, 2.6 * mm, fill=1, stroke=0)
    pdf.setFillColor(colors.white)
    pdf.setFont("YaHeiBold", 6.3)
    pdf.drawCentredString(px + 9 * mm, py - 2.1 * mm, label)
    py = paragraph(pdf, body, px + 22 * mm, py + 0.7 * mm, pw - 22 * mm, style(7.25, 11)) - 2.1 * mm
y -= card_h + 5 * mm

# Undergraduate thesis - concise supporting project
paper_h = 28 * mm
pdf.setFillColor(colors.white)
pdf.setStrokeColor(LINE)
pdf.roundRect(x, y - paper_h, width, paper_h, 4 * mm, fill=1, stroke=1)
pdf.setFillColor(VIOLET)
pdf.roundRect(x, y - paper_h, 2.8 * mm, paper_h, 1.4 * mm, fill=1, stroke=0)
px, py, pw = x + 7 * mm, y - 6.5 * mm, width - 14 * mm
pdf.setFillColor(BLUE)
pdf.setFont("YaHeiBold", 6.6)
pdf.drawString(px, py, "2025 - 2026  |  本科综合论文训练")
py -= 6 * mm
py = paragraph(pdf, "托卡马克等离子体 EUV 辐射研究", px, py, pw, style(10.2, 14, NAVY, True)) - 1.5 * mm
py = paragraph(
    pdf,
    "围绕托卡马克作为 13.5 nm EUV 光源的可行性，完成文献梳理、数量级估算与分层效率模型；识别系统效率和 etendue 约束，并讨论其作为高 Z 杂质辐射研究平台的价值。",
    px, py, pw, style(7.05, 10.6),
)
y -= paper_h + 6 * mm

# Practice and skills
y = section(pdf, "04", "科研实践", x, y, width)
pdf.setFillColor(BLUE)
pdf.setFont("YaHeiBold", 6.8)
pdf.drawString(x, y, "2025.06 - 2025.07")
pdf.setFillColor(NAVY)
pdf.setFont("YaHeiBold", 8.5)
pdf.drawString(x + 32 * mm, y, "核工业西南物理研究院 · 材料研究所")
y = paragraph(
    pdf,
    "参与等离子体材料及钨铜合金模块热负荷性能研究，了解面向聚变装置材料问题的基本科研流程，进一步明确对实验与工程方向的研究兴趣。",
    x + 32 * mm, y - 5.5 * mm, width - 32 * mm, style(7.4, 11.5),
) - 5 * mm

y = section(pdf, "05", "方法与工具", x, y, width)
skills = [
    ("研究", "文献检索与阅读 · 数量级估算 · 功率平衡与效率分析 · 技术路线比较"),
    ("计算", "Python 数据处理与可视化 · MATLAB 数值计算与数据分析"),
    ("表达", "中文技术报告与学术论文写作 · 答辩展示 · 英文文献阅读"),
]
for label, value in skills:
    pdf.setFillColor(BLUE)
    pdf.setFont("YaHeiBold", 7)
    pdf.drawString(x, y, label)
    y = paragraph(pdf, value, x + 18 * mm, y + 1.4 * mm, width - 18 * mm, style(7.25, 11)) - 2.1 * mm

pdf.setStrokeColor(LINE)
pdf.line(x, 10.5 * mm, x + width, 10.5 * mm)
pdf.setFillColor(MUTED)
pdf.setFont("YaHei", 5.8)
pdf.drawString(x, 6.7 * mm, "Academic CV · Fusion & Plasma Research")
pdf.drawRightString(x + width, 6.7 * mm, "2026 · 刘靖臣")
pdf.save()
print(OUTPUT)
