import pythoncom
import pyHook
import requests
import json
import pyperclip
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
            im = ImageGrab.grabclipboard()
            if isinstance(im, Image.Image):
                tmp_file = 'tmp.png'
                im.save(tmp_file)
                files = {'smfile': open(tmp_file, 'rb')}
                response = requests.post('https://sm.ms/api/upload',files=files)
                response_json = to_json(response.text)['data']
                print(response_json)
                url = response_json['url']
                filename = response_json['filename']
                pyperclip.copy('![' + filename + ']('+ url +')')
                print('复制成功')
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
