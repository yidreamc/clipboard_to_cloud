import pythoncom
import pyHook
import requests
import json
import pyperclip
from notice import show_toast
from PIL import Image
from PIL import ImageGrab

def to_json(jsonstring):
    return json.loads(jsonstring)
class KeyboardMgr:
    LcontrolPressed = False
    LmenuPressed = False
    sPressed = False
    def on_key_pressed(self, event):
        if str(event.Key) == 'Lcontrol':
            self.LcontrolPressed = True
        if str(event.Key) == 'Lmenu':
            self.LmenuPressed = True
        if str(event.Key) == 'X' and self.LcontrolPressed == True and self.LmenuPressed == True:
            print('copy')
            im = ImageGrab.grabclipboard()
            if isinstance(im, Image.Image):
                tmp_file = 'tmp.png'
                im.save(tmp_file)
                files = {'smfile': open(tmp_file, 'rb')}
                print("upload")
                response = requests.post('https://sm.ms/api/upload',files=files)
                print("upload succes")
                response_json = to_json(response.text)['data']
                url = response_json['url']
                storename = response_json['storename']
                pyperclip.copy('![' + storename + ']('+ url +')')
                show_toast("Copy Success")
        return True
    def on_key_up(self, event):
        if str(event.Key) == 'Lcontrol':
            self.LcontrolPressed = False
        elif str(event.Key) == 'Lmenu':
            self.LmenuPressed = False
        return True
keyMgr = KeyboardMgr()
hookMgr = pyHook.HookManager()
hookMgr.KeyDown = keyMgr.on_key_pressed
hookMgr.KeyUp = keyMgr.on_key_up
hookMgr.HookKeyboard()
pythoncom.PumpMessages()
