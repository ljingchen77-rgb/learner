"""Generate a one-page Chinese academic resume for supervisor outreach."""
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
NAVY, BLUE, VIOLET, CYAN = map(colors.HexColor, ["#101828", "#1368E8", "#7546E8", "#16B8C8"])
TEXT, MUTED, PALE, LINE = map(colors.HexColor, ["#172033", "#667085", "#F4F7FC", "#DCE4F0"])

def st(size=8.4, leading=13, color=TEXT, bold=False):
    return ParagraphStyle("a", fontName="YaHeiBold" if bold else "YaHei", fontSize=size, leading=leading, textColor=color)

def para(c, text, x, top, width, style):
    p = Paragraph(text, style); _, h = p.wrap(width, H); p.drawOn(c, x, top-h); return top-h

def heading(c, text, x, y, width):
    c.setFillColor(BLUE); c.setFont("YaHeiBold", 10); c.drawString(x, y, text)
    c.setStrokeColor(LINE); c.line(x, y-2.4*mm, x+width, y-2.4*mm); return y-7*mm

c = canvas.Canvas(str(OUTPUT), pagesize=A4); c.setTitle("刘靖臣 - 学术简历"); c.setAuthor("刘靖臣")
c.setFillColor(colors.white); c.rect(0,0,W,H,fill=1,stroke=0)
c.setFillColor(NAVY); c.rect(0,H-48*mm,W,48*mm,fill=1,stroke=0)
c.setFillColor(VIOLET); c.circle(-6*mm,H+1*mm,27*mm,fill=1,stroke=0)
c.setFillColor(BLUE); c.circle(W-3*mm,H-5*mm,24*mm,fill=1,stroke=0)
c.setFillColor(CYAN); c.circle(W-34*mm,H+3*mm,11*mm,fill=1,stroke=0)
x=16*mm
c.setFillColor(colors.white); c.setFont("YaHeiBold",25); c.drawString(x,H-19*mm,"刘靖臣")
c.setFillColor(colors.HexColor("#C6D4E8")); c.setFont("YaHei",8.5)
c.drawString(x,H-28*mm,"清华大学工程物理系 · 核工程与核技术")
c.drawString(x,H-35*mm,"拟研究方向：磁约束核聚变 · 托卡马克边缘与偏滤器物理")
cx=116*mm; c.setFillColor(colors.HexColor("#D9E4F2")); c.setFont("YaHei",7)
c.drawString(cx,H-19*mm,"邮箱  jingchen0911@outlook.com"); c.drawString(cx,H-26*mm,"主页  ljingchen77-rgb.github.io/learner/"); c.drawString(cx,H-33*mm,"GitHub  github.com/ljingchen77-rgb")
c.setFillColor(CYAN); c.roundRect(cx,H-43*mm,58*mm,6.5*mm,3.25*mm,fill=1,stroke=0)
c.setFillColor(NAVY); c.setFont("YaHeiBold",6.8); c.drawCentredString(cx+29*mm,H-40.8*mm,"2026 年本科毕业 · 即将攻读硕士")
x,width,y=16*mm,W-32*mm,H-58*mm
y=heading(c,"个人概况",x,y,width)
y=para(c,"清华大学工程物理系核工程与核技术专业本科生，即将前往核工业西南物理研究院攻读核能科学与技术方向硕士。希望继续学习磁约束核聚变、托卡马克边缘等离子体、偏滤器与等离子体材料相关问题。具备文献调研、数量级估算、物理建模和技术报告写作经验。",x,y,width,st())-4*mm
y=heading(c,"教育背景与研究兴趣",x,y,width)
y=para(c,"<b>清华大学 · 工程物理系</b>　核工程与核技术本科　2022.09 - 2026.06<br/><b>核工业西南物理研究院</b>　核能科学与技术硕士（即将入学）<br/><font color='#1368E8'>磁约束核聚变 · 托卡马克 · 偏滤器物理 · 高 Z 杂质输运 · 等离子体材料</font>",x,y,width,st(8.2,14))-4*mm
y=heading(c,"研究经历",x,y,width)
card_h=88*mm; c.setFillColor(PALE); c.roundRect(x,y-card_h,width,card_h,4*mm,fill=1,stroke=0)
c.setFillColor(VIOLET); c.roundRect(x,y-card_h,2.7*mm,card_h,1.35*mm,fill=1,stroke=0)
px,py,pw=x+7*mm,y-8*mm,width-14*mm
c.setFillColor(BLUE); c.setFont("YaHeiBold",7); c.drawString(px,py,"2025 - 2026 · 本科综合论文训练"); py-=7*mm
py=para(c,"托卡马克等离子体 EUV 辐射的研究",px,py,pw,st(13,18,TEXT,True))-1*mm
py=para(c,"指导教师：谭熠 副教授 · 清华大学工程物理系",px,py,pw,st(7,11,MUTED))-4*mm
items=["围绕托卡马克能否作为 13.5 nm EUV 光刻光源开展系统可行性评估，独立完成相关文献梳理、指标归纳与论文写作。","建立输入功率、总辐射、Sn/Xe 杂质辐射与 13.5 nm 带内输出之间的分层转换效率模型。","对比托卡马克边缘及偏滤器参数与 Sn/Xe 最优辐射窗口，分析能量效率、辐射亮度、MHD 稳定性和工程集成约束。","估算等离子体层 CE 中值约 0.5%，系统层有效 CE 约 10<super>-4</super> 至 10<super>-3</super>，并识别约 10<super>8</super> 倍的 etendue 失配。","形成能力：跨领域文献调研、数量级估算、物理建模、技术比较、论文与答辩材料撰写。"]
for item in items: py=para(c,"<font color='#7546E8'>●</font>　"+item,px,py,pw,st(7.4,11.5))-1.5*mm
y-=card_h+8*mm; y=heading(c,"相关实践",x,y,width)
c.setFillColor(BLUE); c.setFont("YaHeiBold",7); c.drawString(x,y,"2025.06 - 2025.07")
c.setFillColor(TEXT); c.setFont("YaHeiBold",8.7); c.drawString(x+34*mm,y,"核工业西南物理研究院 · 材料研究所")
y=para(c,"在导师指导下参与等离子体材料及钨铜合金模块在热负荷条件下的性能研究，了解面向等离子体材料研究的基本问题与科研工作流程，并进一步明确偏工程、实验方向的研究兴趣。",x+34*mm,y-6*mm,width-34*mm,st(7.7,12))-7*mm
y=heading(c,"专业能力",x,y,width)
skills=[("研究方法","文献检索与阅读、数量级估算、功率平衡与转换效率分析、跨方案技术比较"),("工具","Python 数据处理与可视化、MATLAB 数值计算与数据分析"),("专业基础","托卡马克、偏滤器、高 Z 杂质辐射、EUV、等离子体材料"),("表达","中文技术报告、学术论文写作、答辩展示与英文文献阅读")]
for label,value in skills:
    c.setFillColor(BLUE); c.setFont("YaHeiBold",7.2); c.drawString(x,y,label)
    y=para(c,value,x+22*mm,y+1.5*mm,width-22*mm,st(7.4,11.5))-2.5*mm
c.setStrokeColor(LINE); c.line(x,11*mm,x+width,11*mm); c.setFillColor(MUTED); c.setFont("YaHei",6)
c.drawString(x,7*mm,"学术联系简历 · Curriculum Vitae"); c.drawRightString(x+width,7*mm,"2026 · 刘靖臣")
c.save(); print(OUTPUT)
