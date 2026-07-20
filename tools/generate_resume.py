"""Generate a two-page, website-styled public resume PDF."""
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
OUTPUT = ROOT / "assets" / "Liu-Jingchen-Resume.pdf"
pdfmetrics.registerFont(TTFont("YaHei", r"C:\Windows\Fonts\msyh.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("YaHeiBold", r"C:\Windows\Fonts\msyhbd.ttc", subfontIndex=0))

W, H = A4
NAVY = colors.HexColor("#0C1425")
BLUE = colors.HexColor("#1368E8")
VIOLET = colors.HexColor("#7546E8")
CYAN = colors.HexColor("#16B8C8")
TEXT = colors.HexColor("#172033")
MUTED = colors.HexColor("#667085")
PALE = colors.HexColor("#F4F7FC")
LINE = colors.HexColor("#DCE4F0")
WHITE = colors.white


def style(size=9, leading=14, color=TEXT, bold=False):
    return ParagraphStyle("x", fontName="YaHeiBold" if bold else "YaHei", fontSize=size,
                          leading=leading, textColor=color, spaceAfter=0)


def para(c, text, x, y_top, width, pstyle):
    p = Paragraph(text, pstyle)
    _, height = p.wrap(width, H)
    p.drawOn(c, x, y_top - height)
    return y_top - height


def pill(c, text, x, y, fill=BLUE, text_color=WHITE):
    tw = pdfmetrics.stringWidth(text, "YaHei", 7) + 8 * mm
    c.setFillColor(fill); c.roundRect(x, y, tw, 7 * mm, 3.5 * mm, fill=1, stroke=0)
    c.setFillColor(text_color); c.setFont("YaHei", 7); c.drawCentredString(x + tw / 2, y + 2.25 * mm, text)
    return x + tw + 2 * mm


def section_label(c, text, x, y, width):
    c.setFillColor(BLUE); c.setFont("YaHeiBold", 8); c.drawString(x, y, text.upper())
    c.setStrokeColor(LINE); c.setLineWidth(.5); c.line(x, y - 2.5 * mm, x + width, y - 2.5 * mm)
    return y - 7 * mm


def sidebar(c, lang):
    sw = 60 * mm
    c.setFillColor(NAVY); c.rect(0, 0, sw, H, fill=1, stroke=0)
    c.setFillColor(VIOLET); c.circle(-8 * mm, H - 12 * mm, 30 * mm, fill=1, stroke=0)
    c.setFillColor(BLUE); c.circle(53 * mm, H + 2 * mm, 17 * mm, fill=1, stroke=0)
    c.setFillColor(CYAN); c.circle(54 * mm, 18 * mm, 25 * mm, fill=1, stroke=0)
    x, y = 10 * mm, H - 28 * mm
    c.setFillColor(WHITE); c.setFont("YaHeiBold", 25); c.drawString(x, y, "刘靖臣" if lang == "zh" else "Jingchen")
    if lang == "en": c.drawString(x, y - 10 * mm, "Liu")
    y -= 16 * mm if lang == "zh" else 27 * mm
    y = para(c, "核工程与核技术<br/>磁约束核聚变 · 等离子体物理" if lang == "zh" else "Nuclear Engineering<br/>Magnetic Confinement Fusion<br/>Plasma Physics", x, y, 42 * mm, style(8.5, 13, colors.HexColor("#C8D5EA"))) - 8 * mm
    c.setFillColor(colors.HexColor("#6F87A8")); c.rect(x, y, 40 * mm, .4, fill=1, stroke=0); y -= 10 * mm
    c.setFillColor(CYAN); c.setFont("YaHeiBold", 7.5); c.drawString(x, y, "CONTACT" if lang == "en" else "联系")
    y -= 7 * mm
    for line in ["jingchen0911@outlook.com", "github.com/ljingchen77-rgb", "ljingchen77-rgb.github.io/learner/"]:
        y = para(c, line, x, y, 43 * mm, style(6.8, 10, colors.HexColor("#D8E2F2"))) - 2 * mm
    y -= 6 * mm
    c.setFillColor(CYAN); c.setFont("YaHeiBold", 7.5); c.drawString(x, y, "EDUCATION" if lang == "en" else "教育")
    y -= 8 * mm
    if lang == "zh":
        education = [("2022—2026", "清华大学", "工程物理系 · 本科"), ("即将入学", "核工业西南物理研究院", "核能科学与技术 · 硕士")]
    else:
        education = [("2022—2026", "Tsinghua University", "Engineering Physics · B.Eng."), ("Incoming", "Southwestern Institute of Physics", "Nuclear Science & Technology")]
    for date, school, degree in education:
        c.setFillColor(CYAN); c.circle(x + 1 * mm, y - 1 * mm, 1.1 * mm, fill=1, stroke=0)
        c.setStrokeColor(colors.HexColor("#355071")); c.line(x + 1 * mm, y - 2 * mm, x + 1 * mm, y - 17 * mm)
        c.setFillColor(colors.HexColor("#91A5C1")); c.setFont("YaHei", 6.5); c.drawString(x + 5 * mm, y - 1.5 * mm, date)
        y = para(c, f"<b>{school}</b><br/><font color='#AFC0D8'>{degree}</font>", x + 5 * mm, y - 5 * mm, 39 * mm, style(7.3, 11, WHITE)) - 8 * mm
    y -= 2 * mm
    c.setFillColor(CYAN); c.setFont("YaHeiBold", 7.5); c.drawString(x, y, "TOOLS" if lang == "en" else "工具")
    y -= 8 * mm
    tags = ["Python", "MATLAB", "Data Analysis" if lang == "en" else "数据分析", "Physical Modeling" if lang == "en" else "物理建模", "Academic Writing" if lang == "en" else "学术写作"]
    for tag in tags:
        y = para(c, "• " + tag, x, y, 42 * mm, style(7.2, 11, colors.HexColor("#D8E2F2"))) - 1.5 * mm
    c.setFillColor(colors.HexColor("#07101D")); c.roundRect(9 * mm, 10 * mm, 42 * mm, 13 * mm, 4 * mm, fill=1, stroke=0)
    c.setFillColor(CYAN); c.setFont("YaHeiBold", 7); c.drawString(13 * mm, 17 * mm, "BILINGUAL RESUME · 双语简历")
    c.setFillColor(colors.HexColor("#8EA3BF")); c.setFont("YaHei", 5.8); c.drawString(13 * mm, 13.5 * mm, "Generated from the public portfolio")


def metric(c, x, y, value, label):
    c.setFillColor(PALE); c.roundRect(x, y, 37 * mm, 20 * mm, 4 * mm, fill=1, stroke=0)
    c.setFillColor(BLUE); c.setFont("YaHeiBold", 13); c.drawString(x + 4 * mm, y + 10 * mm, value)
    c.setFillColor(MUTED); c.setFont("YaHei", 6.5); c.drawString(x + 4 * mm, y + 5 * mm, label)


def main_content(c, lang):
    x, width, y = 72 * mm, 125 * mm, H - 20 * mm
    c.setFillColor(BLUE); c.setFont("YaHeiBold", 7); c.drawString(x, y, "RESEARCH PORTFOLIO · 2026")
    y -= 10 * mm
    title = "探索聚变，记录思考。" if lang == "zh" else "Exploring fusion, documenting ideas."
    y = para(c, title, x, y, width, style(19, 25, TEXT, True)) - 3 * mm
    profile = ("清华大学工程物理系核工程与核技术专业本科生，即将前往核工业西南物理研究院攻读核能科学与技术方向硕士。研究兴趣集中于磁约束核聚变、托卡马克边缘等离子体与高 Z 杂质辐射。" if lang == "zh" else "Undergraduate in Nuclear Engineering and Nuclear Technology at Tsinghua University. Incoming graduate student at the Southwestern Institute of Physics, focusing on magnetic confinement fusion, tokamak edge plasmas, and high-Z impurity radiation.")
    y = para(c, profile, x, y, width, style(8.5, 14, MUTED)) - 9 * mm
    y = section_label(c, "研究经历" if lang == "zh" else "Research Experience", x, y, width)
    c.setFillColor(PALE); c.roundRect(x, y - 106 * mm, width, 106 * mm, 5 * mm, fill=1, stroke=0)
    c.setFillColor(VIOLET); c.roundRect(x, y - 106 * mm, 3 * mm, 106 * mm, 1.5 * mm, fill=1, stroke=0)
    px, py, pw = x + 7 * mm, y - 8 * mm, width - 14 * mm
    c.setFillColor(BLUE); c.setFont("YaHeiBold", 7); c.drawString(px, py, "2025—2026 · " + ("本科综合论文训练" if lang == "zh" else "UNDERGRADUATE THESIS"))
    py -= 7 * mm
    project = "托卡马克等离子体 EUV 辐射的研究" if lang == "zh" else "Feasibility of Tokamak Plasma as an EUV Radiation Source"
    py = para(c, project, px, py, pw, style(13, 18, TEXT, True)) - 2 * mm
    mentor = "清华大学工程物理系 · 指导教师：谭熠 副教授" if lang == "zh" else "Department of Engineering Physics, Tsinghua University · Supervisor: Assoc. Prof. Yi Tan"
    py = para(c, mentor, px, py, pw, style(7, 11, MUTED)) - 5 * mm
    question = ("<b>核心问题：</b>托卡马克能否作为 13.5 nm 工业级极紫外光刻光源？" if lang == "zh" else "<b>Research question:</b> Can a tokamak serve as an industrial 13.5 nm EUV lithography source?")
    py = para(c, question, px, py, pw, style(7.8, 12, TEXT)) - 6 * mm
    mx = px
    labels = [("≈ 0.5%", "等离子体层 CE 中值" if lang == "zh" else "Median plasma-level CE"), ("10⁻⁴—10⁻³", "系统层有效 CE" if lang == "zh" else "System-level CE"), ("≈ 10⁸×", "Etendue 失配" if lang == "zh" else "Etendue mismatch")]
    for value, label in labels: metric(c, mx, py - 20 * mm, value, label); mx += 40 * mm
    py -= 28 * mm
    bullets = (["建立输入功率—总辐射—Sn/Xe 杂质辐射—13.5 nm 带内输出的分层转换效率模型。", "从参数匹配、能量效率、辐射亮度、MHD 稳定性与工程集成等维度对比托卡马克和 LPP 光源。", "结论表明托卡马克难以成为工业 EUV 光源，但可作为高 Z 杂质辐射与边缘输运研究平台。"] if lang == "zh" else ["Built a layered conversion-efficiency model from input power to total radiation, Sn/Xe impurity radiation, and 13.5 nm in-band output.", "Compared tokamak and LPP sources across parameter matching, efficiency, radiance, MHD stability, and engineering integration.", "Concluded that tokamaks are unlikely industrial EUV sources but remain valuable platforms for high-Z impurity and edge-transport research."])
    for item in bullets:
        py = para(c, f"<font color='#7546E8'>●</font>　{item}", px, py, pw, style(7.3, 12, TEXT)) - 2 * mm
    y -= 115 * mm
    y = section_label(c, "研究方向" if lang == "zh" else "Research Focus", x, y, width)
    tags = (["磁约束核聚变", "托卡马克", "偏滤器物理", "高 Z 杂质输运", "EUV 辐射", "碰撞辐射模型"] if lang == "zh" else ["Magnetic Confinement", "Tokamak", "Divertor Physics", "High-Z Impurities", "EUV Radiation", "C-R Modeling"])
    tx, ty = x, y - 7 * mm
    for tag in tags:
        tag_width = pdfmetrics.stringWidth(tag, "YaHei", 7) + 10 * mm
        if tx + tag_width > x + width:
            tx = x
            ty -= 10 * mm
        tx = pill(c, tag, tx, ty, colors.HexColor("#EAF1FF"), BLUE)
    c.setFillColor(MUTED); c.setFont("YaHei", 6); c.drawRightString(x + width, 10 * mm, "ljingchen77-rgb.github.io/learner/ · 2026")


c = canvas.Canvas(str(OUTPUT), pagesize=A4)
c.setTitle("刘靖臣 / Jingchen Liu — Resume")
c.setAuthor("Jingchen Liu")
for language in ("zh", "en"):
    c.setFillColor(colors.white); c.rect(0, 0, W, H, fill=1, stroke=0)
    sidebar(c, language); main_content(c, language); c.showPage()
c.save()
print(OUTPUT)
