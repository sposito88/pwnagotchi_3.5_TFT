import logging
 
import pwnagotchi.ui.fonts as fonts
from pwnagotchi.ui.hw.base import DisplayImpl
 
import os,time
 
class Spotpear24inch(DisplayImpl):
    def __init__(self, config):
        super(Spotpear24inch, self).__init__(config, 'spotpear24inch')
        self._display = None
 
    def layout(self):
        fonts.setup(12, 10, 12, 70, 25, 9)
        self._layout['width'] = 480
        self._layout['height'] = 318
        self._layout['face'] = (112, 90)
        self._layout['name'] = (5, 20)
        self._layout['channel'] = (0, 0)
        self._layout['aps'] = (40, 0)
        self._layout['uptime'] = (398, 0)
        self._layout['line1'] = [0, 14, 480, 14]
        self._layout['line2'] = [0, 290, 480, 290]
        self._layout['friend_face'] = (285, 0)
        self._layout['friend_name'] = (285, 16)
        self._layout['shakes'] = (0, 300)
        self._layout['mode'] = (447, 300)
        self._layout['status'] = {
            'pos': (147, 217),
            'font': fonts.status_font(fonts.Medium),
            'max': 30
        }
 
        return self._layout
 
    def refresh(self):
        time.sleep(0.1)
 
    def initialize(self):
        from pwnagotchi.ui.hw.libs.fb import fb
        self._display = fb
        logging.info("initializing spotpear 24inch lcd display")
        self._display.ready_fb(i=1)
        self._display.black_scr()
 
    def render(self, canvas):
        self._display.show_img(canvas.rotate(180))
        self.refresh()
 
    def clear(self):
        self._display.black_scr()
        self.refresh()