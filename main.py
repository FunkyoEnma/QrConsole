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

        qr = QrConsole("https://github.com/FunkyoEnma/QrConsole")

        qr()
        """
        
        self.__shorter = pyshorteners.Shortener()
        self.__lengths = {'chilpit': 23, 'clckru': 21, 'dagd': 20, 'isgd': 20, 'osdb': 22, 'tinyurl': 28}
        self.__url = url
        self.__short = {"tinyurl": "https://tinyurl.com/3shnvrmv"}
        self.__shorteners = []
        #s = s.tinyurl.short("https://recursospython.com/guias-y-manuales/generar-codigo-qr/")
    
    def __call__(self, shortener: str = "tinyurl", save_name: str = None):
        f"""Generar codigo qr para el link {self.__url}.
        parameters:
        shortener -- acortador de enlaces a usar, para ver cuales estan disponibles se puede usar la función
        available_shorteners para conocer los acortadores disponibles o la función shortest_shortener para usar la
        mejor opción
        """

        # En caso de que el parametro shortener sea None se opta por usar la mejor opción
        if shortener == None:
            shortener = self.shortest_shortener

        # Obtener link acortado de la opcion seleccionada
        url_short = self.__short.get(shortener)

        # En caso de que no se tenga el link se genera
        if url_short is None:
            _ = getattr(self.__shorter, shortener)
            url_short = _.short(self.__url)

        # Se genera el codigo qr del link deseado #### Reemplazar despues de pruebas ####
        img = qrcode.make("https://tinyurl.com/3shnvrmv".replace("https://", "").replace("http://", ""),
                        border=0, box_size=1)

        # convertir la imagen a una lista de valores de 0 o 255 dependiendo del color
        img = img.get_image()
        img.save(save_name)
        w_img, h_img = img.size
        img = img.convert("L")
        img = list(img.getdata())


        # Obtener tamaño de terinal para centrar el Qr
        w, h = get_terminal_size()
        margin = 2
        h_min = h_img + (margin * 2)
        w_min = (w_img * 2) + (margin * 2)

        if h < h_min or w < w_min:
            print(f"Por favor cambie el tamaño de la ventana por lo menos a {w_min} columnas con {h_min} filas")

        else:  # Codigo a mostrar si es mayor a lo requerido

            os.system("cls")

            for i in range(h_img + 4):
                print(Back.WHITE, " " * ((w_img * 2) + (margin * 3)), Back.BLACK)

            y = 0

            self.__move(margin, margin * 2)

            for i in range(len(img)):

                self.__move(y + margin + 1, (margin * 2) + 1)

                if (i + 1) % w_img == 0:
                    dat = img[(i + 1) - w_img : i + 1]

                    for (i, item) in enumerate(dat):
                        if item == 255:
                            dat[i] = Back.WHITE + "  "
                        else:
                            dat[i] = Back.BLACK + "  "
                        
                    print(*dat, sep="")

                    y += 1
            
            self.__move(y + margin + margin, (margin * 2) + 1)
            print(Back.WHITE + Fore.BLACK + "QrConsole V-1.0.1 @FunkyoEnma 2022", end="")

            input()

    @property
    def available_shorteners(self):
        """Obtener todos los acortadores disponibles para el link proporcionado"""
        if len(self.__shorteners) == 0:
            self.__check_shorters()
        
        return self.__shorteners

    def __check_shorters(self):
        """Verificar todos los acortadores disponibles de pyshorteners"""
        for i in self.__shorter.available_shorteners:
            mcall = getattr(self.__shorter, i)
            try:
                _ = mcall.short(self.__url)
                self.__lengths[i] = len(_)
                self.__short[i] = _
                self.__shorteners.append(i)
            except:
                pass
        
    @property
    def shortest_shortener(self):
        """Obtener el acortador mas óptimo"""
        if len(self.__lengths) == 0:
            self.__check_shorters()

        return min(self.__lengths, key=self.__lengths.get)

    @staticmethod
    def __move (y, x):
        """Mover el cursor de posición"""
        print(f"\033[{y};{x}H", end="")


qr = QrConsole("https://rosettacode.org/wiki/Terminal_control/Cursor_positioning")
qr()
