import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import os
from datetime import datetime
from src.utils.yaml import logger, from_email, to_email, smtp_server, smtp_port, password, PROJECT_NAME


def send_email_with_batch_files(
        file_list,
        test_results=None,
        pass_count=0,
        fail_count=0,
        skip_count=0
):
    # ====================== 强制保留所有附件，无论成功失败 ======================
    valid_files = []
    for file_path in file_list:
        if os.path.exists(file_path):
            valid_files.append(file_path)
        else:
            logger.info(f"⚠️ 文件不存在：{file_path}")

    if test_results is None:
        test_results = []

    total_count = pass_count + fail_count + skip_count
    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    failed_list = [item for item in test_results if item["result"] == "Fail"]

    logger.info("=" * 80)
    logger.info(f"✅ 测试执行完成，准备发送邮件")
    logger.info(f"📊 Scenario总数：{total_count} | 成功：{pass_count} | 失败：{fail_count} | 跳过：{skip_count}")
    logger.info("=" * 80)

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg[
        'Subject'] = f"【{PROJECT_NAME}_UI自动化测试报告】 {now_time}  | 成功：{pass_count} 失败：{fail_count}  跳过：{skip_count}"

    html = f"""
<html>
<head>
    <meta charset="utf-8">
    <style>
        body{{font-family:微软雅黑; line-height:1.6;}}
        .summary{{border-collapse:collapse; width:70%; margin:10px 0;}}
        .summary th,.summary td{{border:1px solid #333; padding:10px; text-align:center;}}
        .summary th{{background:#f2f2f2;}}
        .pass{{color:green; font-weight:bold;}}
        .fail{{color:red; font-weight:bold;}}
        .detail{{border-collapse:collapse; width:100%; margin:20px 0;}}
        .detail th,.detail td{{border:1px solid #333; padding:8px; text-align:left;}}
        .detail th{{background:#f0f0f0;}}
    </style>
</head>
<body>
    <h2>Web UI 自动化测试结果</h2>
    <p>执行时间：{now_time}</p>

    <!-- 1. 总统计表 -->
    <h3>📊 用例统计</h3>
    <table class="summary">
        <tr>
            <th>用例总数</th>
            <th>成功</th>
            <th>失败</th>
            <th>跳过</th>
        </tr>
        <tr>
            <td>{total_count}</td>
            <td class="pass">{pass_count}</td>
            <td class="fail">{fail_count}</td>
            <td>{skip_count}</td>
        </tr>
    </table>

    <!-- 2. 失败用例详细表（相同 Feature 自动合并） -->
    <h3>📄 失败用例详细信息</h3>
"""

    # 相同 Feature 合并显示
    if fail_count > 0:
        html += """
        <table class="detail">
            <tr>
                <th>Feature</th>
                <th>Scenario</th>
                <th>Test Result</th>
                <th>Failed Step</th>
                <th>Error</th>
            </tr>
        """

        from collections import defaultdict
        feature_map = defaultdict(list)
        for item in failed_list:
            feature_map[item["feature"]].append(item)

        first_in_group = True
        for feature, items in feature_map.items():
            for item in items:
                html += f"""
                <tr>
                    <td>{feature if first_in_group else ""}</td>
                    <td>{item["scenario"]}</td>
                    <td class="fail">{item["result"]}</td>
                    <td>{item["failed_step"]}</td>
                    <td>{item["error"]}</td>
                </tr>
                """
                first_in_group = False
            first_in_group = True

        html += """
        </table>
        """
    else:
        html += "<h3 style='color:green'>✅ 全部用例执行成功</h3>"

    html += """
    <br>
    <p>详细报告见附件</p>
    <p>本邮件由自动化框架自动发送，无需回复</p>
</body>
</html>
    """

    msg.attach(MIMEText(html, 'html', 'utf-8'))

    # ====================== ✅ 核心：无论成功/失败，强制添加所有附件 ======================
    for f in file_list:  # 这里改用原始 file_list，确保一定发送
        try:
            if os.path.exists(f):
                with open(f, 'rb') as fp:
                    part = MIMEApplication(fp.read())
                    part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(f))
                    msg.attach(part)
                logger.info(f"📎 已添加附件：{os.path.basename(f)}")
        except Exception as e:
            logger.error(f"❌ 附件添加失败：{f} => {str(e)}")

    # 发送邮件
    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
        logger.info("✅ 邮件发送成功！")
    except Exception as e:
        logger.error(f"❌ 邮件发送失败：{str(e)}")