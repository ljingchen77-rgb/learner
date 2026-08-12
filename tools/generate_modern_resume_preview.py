"""Generate a clean, modular two-column resume preview."""
import json
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
DATA = json.loads(Path(__file__).with_name("academic_resume_data.json").read_text(encoding="utf-8"))
OUTPUT = ROOT / "assets" / "Liu-Jingchen-Resume-Modern-Preview.pdf"

pdfmetrics.registerFont(TTFont("YaHei", r"C:\Windows\Fonts\msyh.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("YaHeiBold", r"C:\Windows\Fonts\msyhbd.ttc", subfontIndex=0))

W, H = A4
INK = colors.HexColor("#172033")
MUTED = colors.HexColor("#667085")
BLUE = colors.HexColor("#2563EB")
TEAL = colors.HexColor("#0891B2")
PALE = colors.HexColor("#F5F7FB")
SIDE = colors.HexColor("#F0F4FA")
LINE = colors.HexColor("#D9E1EC")


def ps(size=7.4, leading=11, color=INK, bold=False):
    return ParagraphStyle("p", fontName="YaHeiBold" if bold else "YaHei", fontSize=size, leading=leading, textColor=color)


def para(c, text, x, top, width, style):
    p = Paragraph(text, style)
    _, h = p.wrap(width, H)
    p.drawOn(c, x, top - h)
    return top - h


def section_title(c, text, x, y, width, accent=BLUE):
    c.setFillColor(accent)
    c.rect(x, y - 1.2 * mm, 2.2 * mm, 6.2 * mm, fill=1, stroke=0)
    c.setFillColor(INK)
    c.setFont("YaHeiBold", 10)
    c.drawString(x + 5 * mm, y, text)
    c.setStrokeColor(LINE)
    c.line(x + 32 * mm, y + 1.2 * mm, x + width, y + 1.2 * mm)
    return y - 8 * mm


def label_row(c, label, value, x, y, width):
    c.setFillColor(BLUE)
    c.setFont("YaHeiBold", 6.5)
    c.drawString(x, y, label)
    return para(c, value, x + 16 * mm, y + 1.2 * mm, width - 16 * mm, ps(6.8, 10)) - 1.5 * mm


c = canvas.Canvas(str(OUTPUT), pagesize=A4)
c.setTitle("刘靖臣 - 现代简历预览")
c.setAuthor(DATA["basics"]["name"])
c.setFillColor(colors.white)
c.rect(0, 0, W, H, fill=1, stroke=0)

# Compact header with no decorative elements behind text.
c.setFillColor(colors.HexColor("#0F1F3A"))
c.rect(0, H - 38 * mm, W, 38 * mm, fill=1, stroke=0)
c.setFillColor(colors.white)
c.setFont("YaHeiBold", 23)
c.drawString(15 * mm, H - 16 * mm, DATA["basics"]["name"])
c.setFillColor(colors.HexColor("#C9D5E7"))
c.setFont("YaHei", 8)
c.drawString(15 * mm, H - 25 * mm, f'{DATA["basics"]["school"]} · {DATA["basics"]["major"]}')
c.setFillColor(colors.HexColor("#67E8F9"))
c.setFont("YaHeiBold", 7.5)
c.drawString(15 * mm, H - 32 * mm, DATA["basics"]["focus"])

cx = 116 * mm
c.setFillColor(colors.HexColor("#E6EDF7"))
c.setFont("YaHei", 6.7)
c.drawString(cx, H - 15 * mm, DATA["basics"]["email"])
c.drawString(cx, H - 22 * mm, DATA["basics"]["website"])
c.drawString(cx, H - 29 * mm, DATA["basics"]["github"])

# Two-column body.
margin = 15 * mm
gap = 9 * mm
left_w = 57 * mm
right_x = margin + left_w + gap
right_w = W - right_x - margin
body_top = H - 46 * mm
c.setFillColor(SIDE)
c.roundRect(margin, 14 * mm, left_w, body_top - 14 * mm, 4 * mm, fill=1, stroke=0)

# Sidebar
lx, ly, lw = margin + 6 * mm, body_top - 7 * mm, left_w - 12 * mm
ly = section_title(c, "教育背景", lx, ly, lw, TEAL)
for item in DATA["education"]:
    ly = para(c, f'<b>{item["school"]}</b><br/>{item["degree"]}<br/><font color="#667085">{item["period"]}</font>', lx, ly, lw, ps(7.1, 10.8)) - 4 * mm

ly = section_title(c, "相关课程", lx, ly, lw, TEAL)
for item in DATA["courses"]:
    ly = para(c, f'<font color="#0891B2">●</font>　{item}', lx, ly, lw, ps(6.8, 10)) - 1 * mm

ly -= 3 * mm
ly = section_title(c, "荣誉奖项", lx, ly, lw, TEAL)
for item in DATA["honors"]:
    ly = para(c, f'<font color="#0891B2">●</font>　{item}', lx, ly, lw, ps(6.8, 10)) - 1 * mm

ly -= 3 * mm
ly = section_title(c, "技能", lx, ly, lw, TEAL)
for item in DATA["skills"]:
    ly = para(c, item, lx, ly, lw, ps(6.7, 9.8)) - 1.2 * mm

ly -= 3 * mm
ly = section_title(c, "校园与兴趣", lx, ly, lw, TEAL)
ly = para(c, " · ".join(DATA["activities"]), lx, ly, lw, ps(6.5, 9.7)) - 3 * mm
para(c, " · ".join(DATA["interests"]), lx, ly, lw, ps(6.7, 10, TEAL, True))

# Main column
rx, ry, rw = right_x, body_top - 7 * mm, right_w
ry = section_title(c, "研究经历", rx, ry, rw)
r = DATA["research"]
c.setFillColor(BLUE)
c.setFont("YaHeiBold", 6.5)
c.drawString(rx, ry, f'{r["period"]} · {r["status"]}')
ry -= 6 * mm
ry = para(c, r["title"], rx, ry, rw, ps(11, 15, INK, True)) - 3 * mm
for label, value in r["items"]:
    ry = label_row(c, label, value, rx, ry, rw)

ry -= 4 * mm
t = DATA["thesis"]
c.setFillColor(BLUE)
c.setFont("YaHeiBold", 6.5)
c.drawString(rx, ry, f'{t["period"]} · 本科综合论文训练')
ry -= 6 * mm
ry = para(c, t["title"], rx, ry, rw, ps(9, 12.5, INK, True)) - 2 * mm
ry = para(c, t["summary"], rx, ry, rw, ps(6.9, 10.3)) - 7 * mm

ry = section_title(c, "生产实习", rx, ry, rw)
i = DATA["internship"]
c.setFillColor(BLUE)
c.setFont("YaHeiBold", 6.5)
c.drawString(rx, ry, i["period"])
ry -= 6 * mm
ry = para(c, i["organization"], rx, ry, rw, ps(9.3, 12.5, INK, True)) - 1 * mm
ry = para(c, f'指导教师：{i["mentor"]}', rx, ry, rw, ps(6.6, 9.5, MUTED)) - 3 * mm
ry = para(c, i["summary"], rx, ry, rw, ps(7, 10.7)) - 5 * mm

# Readable internship highlights, separated from the paragraph.
c.setFillColor(PALE)
c.roundRect(rx, ry - 34 * mm, rw, 34 * mm, 3 * mm, fill=1, stroke=0)
hy = ry - 6 * mm
highlights = [
    ("测试平台", "20 MW 电子束材料测试平台；红外测温与吸收功率计算"),
    ("研究对象", "W/CuCrZr 水冷模块；9/15 MW·m<super>-2</super> 循环热负荷"),
    ("分析关注", "连接界面、钨再结晶、表面开裂与热负荷损伤"),
]
for label, value in highlights:
    hy = label_row(c, label, value, rx + 5 * mm, hy, rw - 10 * mm)

c.setStrokeColor(LINE)
c.line(margin, 9.5 * mm, W - margin, 9.5 * mm)
c.setFillColor(MUTED)
c.setFont("YaHei", 5.7)
c.drawString(margin, 6 * mm, "Academic Resume · Fusion Engineering")
c.drawRightString(W - margin, 6 * mm, "2026 · 刘靖臣")
c.save()
print(OUTPUT)
