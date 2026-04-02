import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from datetime import datetime
from src.utils.yaml import logger, from_email, to_email, smtp_server, smtp_port, password


def send_email_with_batch_files(file_list):
    valid_files = []

    # 直接校验传入的路径
    for file_path in file_list:
        if os.path.exists(file_path):
            valid_files.append(file_path)
        else:
            logger.info(f"⚠️ 文件不存在：{file_path}")

    if not valid_files:
        logger.info("❌ 未找到任何有效文件")
        return

    logger.info(f"✅ 准备发送 {len(valid_files)} 个文件：")
    i = 1

    for f in valid_files:
        logger.info(f" → 📄文件{i} {os.path.basename(f)}")
        i = i + 1
    logger.info( "=" * 80)

    # 邮件内容
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = f"【自动化测试报告】{datetime.now().strftime('%Y-%m-%d %H:%M')}"

    body = f"本次共发送 {len(valid_files)} 个测试报告\n\n"
    for f in valid_files:
        body += f"📄 {os.path.basename(f)}\n"
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # 添加附件
    for file_path in valid_files:
        with open(file_path, 'rb') as f:
            part = MIMEApplication(f.read())
            part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))
            msg.attach(part)

    # 发送
    logger.info("🔹 开始发邮件")
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())

    logger.info("✅ 邮件发送成功！")

