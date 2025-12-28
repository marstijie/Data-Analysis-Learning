# 载入环境
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

with open("美食排行.xlsx", "rb") as food_file:
    food_content = food_file.read()

# 设置邮件类型、格式
att1 = MIMEText(food_content, "base64", "gb2312")
att1["Content-Type"] = "application/octet-stream"
att1.add_header("Content-Disposition", "attachment", filename="美食排行.xlsx")

with open("城市景点.xlsx", "rb") as view_file:
    view_content = view_file.read()
att2 = MIMEText(view_content, "base64", "gb2312")
att2["Content-Type"] = "application/octet-stream"
att2.add_header("Content-Disposition", "attachment", filename="城市景点.xlsx")

# 邮箱服务器设置
mailHost = "smtp.qq.com"
# 邮箱账号设置
mailUser = "1545991749@qq.com"
# 邮箱授权码设置
mailPass = "--------------"

# 使用smtplib.SMTP_SSL(服务器, 端口号),端口号为465
smtpObj = smtplib.SMTP_SSL(mailHost, 465)
# 使用login()函数传入邮箱账户和授权码，登录邮箱
smtpObj.login(mailUser, mailPass)

# 此处可设置多个mail发送对象
mail_dict = {"marstijie": "molamolas@163.com","李唯佳":"1115780231@qq.com"}
mail_list = mail_dict.items()
for key, value in mail_list:
    # 使用MIMEMultipart()构造附件
    message = MIMEMultipart()
    # 使用attach()将附件att1、2设置到邮件内容里
    message.attach(att1)
    message.attach(att2)

    # 使用MIMEText()设置邮件正文
    mail_content = MIMEText(f"{key}同学，附件是今日北京和上海美食和景点信息，请查收！", "plain", "utf-8")
    # 使用格式化设置邮件发件人名称
    message['From'] = Header(f"时间管理大师<{mailUser}>")
    # 使用格式化设置邮件收件人名称
    message['To'] = Header(f"{key}同学<{value}>")
    # 设置邮件主题 北京和上海旅游信息汇总
    message['Subject'] = Header("北京和上海旅游信息汇总")
    # 使用message.attach()函数上传邮件正文
    message.attach(mail_content)
    # 使用sendmail(发送人，收件人，message.as_string())发邮件
    smtpObj.sendmail(mailUser, value, message.as_string())
    # 获取姓名格式化输出"xx的邮件发送成功"
    print(f"{key}的邮件发送成功")