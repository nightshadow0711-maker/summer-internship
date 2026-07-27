from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
import io

def build_pdf(result):
    buf=io.BytesIO()
    doc=SimpleDocTemplate(buf,pagesize=A4,rightMargin=36,leftMargin=36,topMargin=36,bottomMargin=36)
    styles=getSampleStyleSheet()
    story=[Paragraph("TRUTHGUARD AI",styles["Title"]),Paragraph("News Verification Report",styles["Heading2"]),Spacer(1,12)]
    story.append(Paragraph(result.get("article_title","Untitled"),styles["Heading1"]))
    story.append(Paragraph(result.get("article_text","")[:2500].replace("&","&amp;").replace("<","&lt;"),styles["BodyText"]))
    story.append(Spacer(1,12))
    data=[
        ["Metric","Result"],
        ["ML Prediction",f'{result.get("ml_prediction")} ({result.get("ml_confidence",0):.1f}%)'],
        ["Online Verification",result.get("online_status")],
        ["Fact Check",result.get("fact_check_status")],
        ["Source Credibility",f'{result.get("source_credibility",0):.1f}/100'],
        ["Final Assessment",f'{result.get("final_assessment")} ({result.get("final_score",0):.1f}%)'],
    ]
    t=Table(data,colWidths=[170,330])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1f3a68")),("TEXTCOLOR",(0,0),(-1,0),colors.white),("GRID",(0,0),(-1,-1),.5,colors.grey),("VALIGN",(0,0),(-1,-1),"TOP"),("PADDING",(0,0),(-1,-1),8)]))
    story += [t,Spacer(1,16),Paragraph("Evidence Sources",styles["Heading2"])]
    for s in result.get("sources",[]):
        story.append(Paragraph(f'{s.get("source_name")} — {s.get("title")} — {s.get("url")}',styles["BodyText"]))
        story.append(Spacer(1,5))
    story.append(Spacer(1,10))
    story.append(Paragraph("Disclaimer: This system is an educational decision-support tool. External evidence availability can affect results.",styles["Italic"]))
    doc.build(story)
    return buf.getvalue()
