import win32com.client
import win32gui
import win32con
import time
import os

from library import read_double_tag


def window_enum_handler(hwnd, resultList):
    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
        resultList.append((hwnd, win32gui.GetWindowText(hwnd)))


def get_app_list(handles=[]):
    mlst=[]
    win32gui.EnumWindows(window_enum_handler, handles)
    for handle in handles:
        mlst.append(handle)
    return mlst


def bringFront(title):
    """
    bring current outlook window to front
    :param title: current outlook mail's title
    """
    appwindows = get_app_list()
    for i in appwindows:
        if i[1].split("-")[0].strip() == title:
            HWND = i[0]
            win32gui.ShowWindow(HWND, win32con.SW_RESTORE)
            win32gui.SetWindowPos(HWND, win32con.HWND_NOTOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
            win32gui.SetWindowPos(HWND, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)
            win32gui.SetWindowPos(HWND, win32con.HWND_NOTOPMOST, 0, 0, 0, 0,
                                  win32con.SWP_SHOWWINDOW + win32con.SWP_NOMOVE + win32con.SWP_NOSIZE)


def send_mail(attachment):
    outlook=win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)

    mail.To = read_double_tag("mail","to")

    mail.CC = read_double_tag("mail","cc")

    title = read_double_tag("mail","title")
    mail.Subject = title

    body = read_double_tag("mail","body")
    body_val = body.replace("\n","<br>")
    mail.HTMLBody = body_val

    mail.Attachments.Add(attachment)

    mail.Display(False)
    bringFront(title)
    time.sleep(5)
    mail.Send()