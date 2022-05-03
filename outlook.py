import win32com.client
import time
import os

from library import read_double_tag


def send_mail(attachment):
    outlook=win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)

    mail.To = read_double_tag("mail","to")

    mail.CC = read_double_tag("mail","cc")

    mail.Subject = read_double_tag("mail","title")

    body = read_double_tag("mail","body")
    body_val = body.replace("\n","<br>")
    mail.HTMLBody = body_val

    mail.Attachments.Add(attachment)

    mail.Display(False)
    time.sleep(10)
    mail.Send()