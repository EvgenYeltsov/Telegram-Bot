import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailService:

	def send_email(self, fromaddr, toaddr, body):
		server=smtplib.SMTP('smtp.gmail.com', 587)
		msg = MIMEMultipart()
		msg['From'] = fromaddr
		msg['To'] = toaddr
		msg['Subject'] = "Отправитель: STV_telegram_bot"
		msg.attach(MIMEText(body, 'plain'))
		server.ehlo()
		server.starttls()
		server.ehlo()
		server.login(fromaddr, "Your Password!")
		text = msg.as_string()
		server.sendmail(fromaddr, toaddr, text)
		server.quit()
