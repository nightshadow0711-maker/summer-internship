import smtplib
from email.message import EmailMessage
from config.settings import SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SMTP_FROM

def send_report(recipient, subject, body, pdf_bytes=None):
    if not all([SMTP_HOST, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, SMTP_FROM]):
        raise RuntimeError("SMTP settings are not configured in .env")
    msg=EmailMessage()
    msg["Subject"]=subject
    msg["From"]=SMTP_FROM
    msg["To"]=recipient
    msg.set_content(body)
    if pdf_bytes:
        msg.add_attachment(pdf_bytes, maintype="application", subtype="pdf", filename="truthguard_report.pdf")
    with smtplib.SMTP(SMTP_HOST,SMTP_PORT,timeout=20) as server:
        server.starttls()
        server.login(SMTP_USERNAME,SMTP_PASSWORD)
        server.send_message(msg)
