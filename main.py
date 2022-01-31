from inspect import Attribute
import os

import qrcode
from PIL import Image
import colorama
from colorama import Back, Fore

from terminal import get_terminal_size
import pyshorteners

colorama.init()

class QrConsole:

    def __init__(self, url: str = "https://linktr.ee/FunkyoEnma") -> None:
        """Generador de codigos qr en consola, para usarlo se debe de pasar un argumento un link valido en formato str

        Para generar el qr en pantalla por favor vuelva a llamar la funcion. ej:

        qr = QrConsole("https://link.com")
        qr()
        """
        
        self.__shorter = pyshorteners.Shortener()
        self.__lengths = {'chilpit': 23, 'clckru': 21, 'dagd': 20, 'isgd': 20, 'osdb': 22, 'tinyurl': 28}
        self.__url = url
        self.__shorteners = []
        #s = s.tinyurl.short("https://recursospython.com/guias-y-manuales/generar-codigo-qr/")
    
    def __call__(self,shortener=None, force = True):

        if shortener == None:
            shortener = self.shortest_shortener

        img = qrcode.make("https://tinyurl.com/3shnvrmv".replace("https://", "").replace("http://", ""),
                        border=0, box_size=1)

        img = img.get_image()
        w_img, h_img = img.size
        img = img.convert("L")
        img = list(img.getdata())

        w, h = get_terminal_size()

        if h < h_img:
            print("Consola mas pequeña de lo requerido")
        elif h == h_img:
            print("iguales")
        else:

            margin = int((h - h_img) / 2) + 1

            for i in range(h - 1):
                print(Back.WHITE," " * ((w_img * 2) + (margin * 3)), Back.BLACK)

            y = 0

            self.__move(margin, margin * 2)

            for i in range(len(img)):

                self.__move(y + margin, margin * 2)

                if (i + 1) % w_img == 0:
                    dat = img[(i + 1) - w_img : i + 1]

                    for (i, item) in enumerate(dat):
                        if item == 255:
                            dat[i] = Back.WHITE + "  "
                        else:
                            dat[i] = Back.BLACK + "  "
                        
                    print(*dat, sep="")

                    y += 1
            
        input()

    @property
    def available_shorteners(self):
        if len(self.__shorteners) == 0:
            self.check_shorters()
        
        return self.__shorteners

    def check_shorters(self):
        for i in self.__shorter.available_shorteners:
            mcall = getattr(self.__shorter, i)
            try:
                _ = mcall.short(self.__url)
                self.__lengths[i] = len(_)
                self.__shorteners.append(i)
            except:
                pass
        
    @property
    def shortest_shortener(self):
        if len(self.__lengths) == 0:
            self.check_shorters()

        return min(self.__lengths, key=self.__lengths.get)

    @staticmethod
    def __move (y, x):
        print(f"\033[{y};{x}H", end="")


qr = QrConsole("https://rosettacode.org/wiki/Terminal_control/Cursor_positioning")
print(qr.shortest_shortener)
