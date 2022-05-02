import win32com.client
import time
import os

from library import read_double_tag, read_html


def send_mail(attachment):
    outlook=win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)

    mail.To = read_double_tag("mail","to")
    mail.CC = read_double_tag("mail","cc")
    mail.Subject = read_double_tag("mail","title")
    mail.HTMLBody = read_double_tag("mail","body")
    mail.Attachments.Add(attachment)

    mail.Display(False)
    time.sleep(10)
    mail.Send()