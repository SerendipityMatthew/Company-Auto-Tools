import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

sender = '3209534840@qq.com'
password = 'itjxybikiywtdgch'
user = '3209534840@qq.com'


def write_execute_result(execute_result):
    file_name = execute_result + ".txt"
    with open(file_name, 'w') as f:
        f.write(execute_result)

    return file_name


def send_result_mail(build_log_file):
    compiling_report_message = MIMEMultipart()
    compiling_report_message['From'] = formataddr(["Compiling result Report ", sender])
    compiling_report_message['To'] = formataddr(["FK", user])
    compiling_report_message['Subject'] = "Compiling Report"
    compiling_report_message.attach(MIMEText('Compiling report', 'plain', 'utf-8'))
    compiling_log_attach = MIMEText(open(build_log_file, 'rb').read(), 'base64', 'utf-8')
    compiling_log_attach['Content-Type'] = 'application/txt'
    compiling_log_attach["Content-Disposition"] = 'attachment; filename="%s"' % build_log_file
    compiling_report_message.attach(compiling_log_attach)
    server = smtplib.SMTP_SSL("smtp.qq.com", 465)
    server.login(sender, password)
    server.sendmail(sender, [user, ], compiling_report_message.as_string())
    server.quit()
