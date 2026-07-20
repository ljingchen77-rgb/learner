"""Generate the public bilingual resume PDF from website content."""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "Liu-Jingchen-Resume.pdf"
pdfmetrics.registerFont(TTFont("YaHei", r"C:\Windows\Fonts\msyh.ttc", subfontIndex=0))
pdfmetrics.registerFont(TTFont("YaHeiBold", r"C:\Windows\Fonts\msyhbd.ttc", subfontIndex=0))

BLUE = colors.HexColor("#1368E8")
TEXT = colors.HexColor("#172033")
MUTED = colors.HexColor("#667085")
LINE = colors.HexColor("#D9E0EB")
styles = getSampleStyleSheet()

title = ParagraphStyle("title", fontName="YaHeiBold", fontSize=24, leading=30, textColor=TEXT, spaceAfter=4)
subtitle = ParagraphStyle("subtitle", fontName="YaHei", fontSize=9, leading=14, textColor=MUTED, spaceAfter=12)
section = ParagraphStyle("section", fontName="YaHeiBold", fontSize=12, leading=17, textColor=BLUE, spaceBefore=10, spaceAfter=6)
body = ParagraphStyle("body", fontName="YaHei", fontSize=9, leading=15, textColor=TEXT, spaceAfter=5)
small = ParagraphStyle("small", fontName="YaHei", fontSize=8, leading=12, textColor=MUTED)


def header(name, descriptor):
    return [Paragraph(name, title), Paragraph(descriptor, subtitle),
            Paragraph("jingchen0911@outlook.com　·　github.com/ljingchen77-rgb　·　ljingchen77-rgb.github.io/learner/", small), Spacer(1, 5 * mm)]


def heading(text):
    return [Paragraph(text, section), Table([[""]], colWidths=[180 * mm], rowHeights=[0.3 * mm], style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), LINE)]))]


def bullets(items):
    return [Paragraph("• " + item, body) for item in items]


story = []
story += header("刘靖臣", "核工程与核技术 · 磁约束核聚变 · 等离子体物理")
story += heading("个人简介")
story += [Paragraph("清华大学工程物理系核工程与核技术专业本科生，即将前往核工业西南物理研究院攻读核能科学与技术方向硕士，研究兴趣集中于磁约束核聚变、托卡马克边缘等离子体与高 Z 杂质辐射。", body)]
story += heading("教育经历")
story += [Paragraph("<b>清华大学 · 工程物理系</b>　核工程与核技术本科　2022.09—2026.06", body), Paragraph("<b>核工业西南物理研究院</b>　核能科学与技术硕士（即将入学）", body)]
story += heading("研究经历")
story += [Paragraph("<b>托卡马克等离子体 EUV 辐射的研究</b>　本科综合论文训练　2025—2026", body), Paragraph("指导教师：谭熠 副教授", small)]
story += bullets([
    "基于系统文献调研、数量级估算与定性物理推理，评估托卡马克作为 13.5 nm EUV 光刻光源的可行性。",
    "建立输入功率—总辐射—Sn/Xe 杂质辐射—13.5 nm 带内输出的分层转换效率模型。",
    "从参数匹配、能量效率、辐射亮度、MHD 稳定性和工程集成等维度与工业 LPP 光源进行比较。",
    "估算等离子体层 CE 中值约 0.5%，系统层有效 CE 约 10⁻⁴—10⁻³，etendue 失配约 10⁸ 倍。",
    "研究表明托卡马克难以成为工业 EUV 光源，但可作为高 Z 杂质辐射和边缘输运研究平台。",
])
story += heading("研究方向与能力")
story += [Paragraph("磁约束核聚变 · 托卡马克 · 偏滤器物理 · 高 Z 杂质输运 · EUV 辐射 · 碰撞辐射模型", body), Paragraph("Python · MATLAB · 数据分析 · 物理建模 · 文献调研 · 学术写作", body)]

story.append(PageBreak())
story += header("Jingchen Liu", "Nuclear Engineering · Magnetic Confinement Fusion · Plasma Physics")
story += heading("PROFILE")
story += [Paragraph("Undergraduate in Nuclear Engineering and Nuclear Technology at the Department of Engineering Physics, Tsinghua University. Incoming graduate student in Nuclear Science and Technology at the Southwestern Institute of Physics, with research interests in magnetic confinement fusion, tokamak edge plasmas, and high-Z impurity radiation.", body)]
story += heading("EDUCATION")
story += [Paragraph("<b>Tsinghua University · Department of Engineering Physics</b>　B.Eng. in Nuclear Engineering and Nuclear Technology　Sep 2022—Jun 2026", body), Paragraph("<b>Southwestern Institute of Physics</b>　Incoming graduate student in Nuclear Science and Technology", body)]
story += heading("RESEARCH EXPERIENCE")
story += [Paragraph("<b>Feasibility of Tokamak Plasma as an EUV Radiation Source</b>　Undergraduate Thesis　2025—2026", body), Paragraph("Supervisor: Assoc. Prof. Yi Tan", small)]
story += bullets([
    "Assessed the feasibility of tokamak plasmas as 13.5 nm EUV lithography sources through literature review, order-of-magnitude estimation, and qualitative physical reasoning.",
    "Developed a layered conversion-efficiency framework from input power to total radiation, Sn/Xe impurity radiation, and in-band output.",
    "Compared tokamak and industrial LPP sources across parameter matching, efficiency, spectral radiance, MHD stability, and engineering integration.",
    "Estimated a median plasma-level CE of about 0.5%, system-level CE of 10⁻⁴—10⁻³, and an etendue mismatch of approximately 10⁸.",
    "Concluded that tokamaks are unlikely to serve as industrial EUV sources, but remain valuable platforms for high-Z impurity radiation and edge-transport research.",
])
story += heading("RESEARCH INTERESTS & SKILLS")
story += [Paragraph("Magnetic Confinement Fusion · Tokamak · Divertor Physics · High-Z Impurity Transport · EUV Radiation · Collisional-Radiative Modeling", body), Paragraph("Python · MATLAB · Data Analysis · Physical Modeling · Literature Review · Academic Writing", body)]

doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=15 * mm, leftMargin=15 * mm, topMargin=14 * mm, bottomMargin=14 * mm, title="刘靖臣 / Jingchen Liu — Resume", author="Jingchen Liu")
doc.build(story)
print(OUTPUT)
