from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from datetime import datetime

from UserManager import UserData
import smtplib

MY_EMAIL = os.getenv("MY_EMAIL")
EMAIL_PWD = os.getenv("EMAIL_PWD")


class NotificationManager:

    def __init__(self, playlist):
        self.playlist_name = playlist["name"]
        self.playlist_link = playlist["external_urls"]["spotify"]

    def send_email(self, user: UserData):
        # ---*--- Compose message in UTF-8 encoding ---*---
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "New playlist of the month."
        msg["From"] = MY_EMAIL
        msg["To"] = user.email
        part1 = MIMEText(f"Привет, {user.name}!\n"
                         f"Спасибо за подписку!\n"
                         f"Вот Ваша ссылка на свежий плейлист с лучшими треками прошлого месяца по версии "
                         f"Billboard.com.\n "
                         f"{self.playlist_name} - {self.playlist_link}", "plain", "utf-8")
        msg.attach(part1)
        # ---*--- Send composed message to user ---*---
        with smtplib.SMTP(host="smtp.yandex.ru") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, EMAIL_PWD)
            connection.sendmail(MY_EMAIL, user.email, msg.as_string().encode('ascii'))

            with open("sendmail.log", mode="a") as f:
                f.write(f"{datetime.now()}: Mail sent to {user.email}\n")
