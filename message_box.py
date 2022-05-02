from ctypes import *
from ctypes.wintypes import HWND,LPWSTR,UINT


MB_OK = 0x0
MB_OKCXL = 0x01
MB_YESNOCXL = 0x03
MB_YESNO = 0x04
MB_HELP = 0x4000
ICON_EXLAIM=0x30
ICON_INFO = 0x40
ICON_STOP = 0x10
ICON_HELP=0x20


# define Pop-up Message
def MessageBoxW(hwnd,text,caption,utype):
    _user32 = WinDLL('user32', use_last_error=True)

    _MessageBoxW = _user32.MessageBoxW
    _MessageBoxW.restype = UINT  # default return type is c_int, this is not required
    _MessageBoxW.argtypes = (HWND, LPWSTR, LPWSTR, UINT)

    result=_MessageBoxW(hwnd,text,caption,utype)

    if not result:
        raise WinError(get_last_error())
    return result


# Show Message
def showMbox(text,caption,style):
    sty = int(style) + 4096
    result=MessageBoxW(None,text,caption,sty)
    return result