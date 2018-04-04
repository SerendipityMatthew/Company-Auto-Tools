import commands
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

sender = '3209534840@qq.com'
password = 'itjxybikiywtdgch'
user = '3209534840@qq.com'


def write_execute_result(execute_result, file_name="build"):
    file_name = file_name + ".txt"
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


def execute_command(compile_command, always_send_email=False):
    execute_status, execute_result = commands.getstatusoutput(compile_command)
    print "the command = %s command exec status = %s, result %s " % (compile_command, execute_status, execute_result)
    file_dir = write_execute_result(execute_result)
    if always_send_email:
        send_result_mail(file_dir)
    if execute_status != 0:
        # we will send email when we got a wrong
        if not always_send_email:
            send_result_mail(file_dir)
        raise RuntimeError()
