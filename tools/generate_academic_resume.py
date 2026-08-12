"""Generate a polished one-page Chinese academic CV for supervisor outreach."""
from pathlib import Path
import json

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
DATA = json.loads((Path(__file__).with_name("academic_resume_data.json")).read_text(encoding="utf-8"))
BASIC = DATA["basics"]
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
pdf.drawString(x, H - 17 * mm, BASIC["name"])
pdf.setFillColor(colors.HexColor("#D7E2F2"))
pdf.setFont("YaHei", 8.4)
pdf.drawString(x, H - 26 * mm, f'{BASIC["school"]} · {BASIC["major"]}')
pdf.setFillColor(CYAN)
pdf.setFont("YaHeiBold", 8.2)
pdf.drawString(x, H - 34 * mm, f'研究定位  |  {BASIC["focus"]}')

cx = 119 * mm
pdf.setFillColor(colors.HexColor("#E2EAF5"))
pdf.setFont("YaHei", 6.8)
pdf.drawString(cx, H - 17 * mm, f'邮箱  {BASIC["email"]}')
pdf.drawString(cx, H - 24 * mm, f'主页  {BASIC["website"]}')
pdf.drawString(cx, H - 31 * mm, f'GitHub  {BASIC["github"]}')
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
undergrad, graduate = DATA["education"]
ey = paragraph(pdf, f'<b>{undergrad["school"]}</b>　{undergrad["degree"]}　{undergrad["period"]}', ex, ey, ew, style(8.8, 13, NAVY, True)) - 2 * mm
ey = paragraph(pdf, f'<b>升学去向</b>　{graduate["school"]} · {graduate["degree"]}（{graduate["period"]}）', ex, ey, ew, style(7.6, 11.5)) - 2 * mm
ey = paragraph(pdf, f'<b>相关课程</b>　{" · ".join(DATA["courses"])}', ex, ey, ew, style(7.6, 11.5)) - 2 * mm
paragraph(pdf, f'<b>荣誉奖项</b>　<font color="#1769E0">{" · ".join(DATA["honors"])}</font>', ex, ey, ew, style(7.6, 11.5))
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
research = DATA["research"]
pdf.drawString(px, py, f'{research["period"]}  |  {research["status"]}')
py -= 6 * mm
py = paragraph(pdf, research["title"], px, py, pw, style(11.5, 15.5, NAVY, True)) - 2 * mm
research_rows = research["items"]
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
thesis = DATA["thesis"]
pdf.drawString(px, py, f'{thesis["period"]}  |  本科综合论文训练')
py -= 5.5 * mm
py = paragraph(pdf, thesis["title"], px, py, pw, style(9.3, 12.5, NAVY, True)) - 1 * mm
paragraph(
    pdf,
    thesis["summary"],
    px, py, pw, style(7.1, 10.3),
)
y -= paper_h + 4 * mm

# Internship receives its own prominent section.
y = section(pdf, "03", "生产实习与科研实践", x, y, width)
pdf.setFillColor(BLUE)
pdf.setFont("YaHeiBold", 6.8)
internship = DATA["internship"]
pdf.drawString(x, y, internship["period"])
pdf.setFillColor(NAVY)
pdf.setFont("YaHeiBold", 8.5)
pdf.drawString(x + 42 * mm, y, f'{internship["organization"]}（{internship["mentor"]}指导）')
y = paragraph(
    pdf,
    internship["summary"],
    x + 42 * mm, y - 5.5 * mm, width - 42 * mm, style(7.15, 10.8),
) - 6 * mm

y = section(pdf, "04", "校园经历、技能与兴趣", x, y, width)
skills = [
    ("经历", " · ".join(DATA["activities"])),
    ("技能", " · ".join(DATA["skills"])),
    ("兴趣", " · ".join(DATA["interests"])),
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
