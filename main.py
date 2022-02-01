import os
import re

import qrcode
import colorama
from colorama import Back, Fore, Style

from terminal import get_terminal_size
import pyshorteners

colorama.init()


class QrConsole:

    def __init__(self, url: str = "https://linktr.ee/FunkyoEnma", text: str = None) -> None:
        """Generador de codigos qr en consola, para usarlo se debe de pasar un argumento un link valido en formato str

        Para generar el qr en pantalla por favor vuelva a llamar la funcion. ej:

        qr = QrConsole("https://github.com/FunkyoEnma/QrConsole")

        qr()

        ****

        Uso del apartado texto:
        ****
        Este apartado es meramente opcional y en caso de no marcarse se necesitara menos tamaño en la consola
        ////

        [Recomendaciones]
        ////

        - Procurar que los textos no sean mas grandes al espacio disponible a la derecha del codigo (No se cuenta etiquetas ni formatos con \\\\033[1 etc...)

        - Los codigos de formato deben de ir siempre dentro de las etiquetas

        [Etiquetas]
        ****
        Las etiquetas siempre deben de ir en el siguiente orden, y se debe de procurar siempre seguir el mismo para evitar errores y estas mismas se deben colocar al inicio de la linea deseada
        ////

        **Alineacion** Esta etiqueta como su nombre lo indica permite configurar la alineacion del texto, teniendo las siguientes opciones:

        - **<[center]** Permite centrar el texto en el espacio disponible
        - **<[right]** Permite alinear el texto a la derecha en el espacio disponible

        **Resaltado** Esta etiqueta permite resaltar la linea, colocando el fondo en blanco y las letras en negro, y su
         etiqueta es <**

        **Rellenado** Esta etiqueta permite rellenar el espacio libre de la linea con el caracter deseado, y su etiqueta
        es <[fill=\ **?**\ ] donde **?** es el caracter deseado

        :param url: Link del cual se desea generar el codigo qr
        :param text: Texto a colocar en la parte derecha del qr, si se deja en blanco se necesitara menos tamaño de consola
        """
        
        self.__shorter = pyshorteners.Shortener()
        self.__lengths = {}
        self.__url = url
        self.__short = {}
        self.__shorteners = []
        self.__text = text
        #s = s.tinyurl.short("https://recursospython.com/guias-y-manuales/generar-codigo-qr/")
    
    def __call__(self, shortener: str = None, save_name: str = None):
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
        img = qrcode.make(url_short.replace("https://", "").replace("http://", ""),
                        border=0, box_size=1)

        # convertir la imagen a una lista de valores de 0 o 255 dependiendo del color
        img = img.get_image()
        img.save(save_name) if save_name is not None else ...
        w_img, h_img = img.size
        img = img.convert("L")
        img = list(img.getdata())


        # Obtener tamaño de terinal para centrar el Qr
        w, h = get_terminal_size()
        margin = 2
        h_min = h_img + (margin * 2)
        w_min = (w_img * 2) + (margin * 2)

        if h < h_min or w < w_min * (2 if self.__text is not None else 1):
            print(f"Por favor cambie el tamaño de la ventana por lo menos a {w_min * 2} columnas con {h_min} filas")

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

            __copyright = "QrConsole V-1.0.1 @FunkyoEnma 2022"

            w_free = (w_img * 2) + (margin * 5) + 1

            self.__move(y + margin + margin, int(((w_img * 2) + (margin * 3)) / 2) - int(len(__copyright) / 2) + 1)
            print(Back.WHITE + Fore.BLACK + __copyright, end="")

            if self.__text is not None:
                text = self.__text.splitlines()

                y = (h - len(text)) // 2

                for i in range(len(text)):
                    self.__move(y + i, w_free)
                    self.__print_ln(text[i], w - w_free - 3)

            input()

    def __print_ln(self, data: str, text_space: int, end="\n"):
        print(Back.BLACK + Fore.WHITE, end="")
        __org_data = data
        __center = 0
        __centred = False
        __right = False
        __format = False

        if re.match("^<\[center].*", data.rstrip().lstrip()) is not None:
            data = data.replace("<[center]", "", 1)
            data = data.rstrip().lstrip().center(text_space)
            __centred = True
        elif re.match("^<\[right].*", data.lstrip().rstrip()) is not None:
            data = data.replace("<[right]", "", 1)
            data = data.rstrip().lstrip().rjust(text_space)
            __right = True

        if re.match("^<\*\*.*", data.lstrip().rstrip()) is not None:
            data = data.split("<**", 1)[1]

            if __centred:
                __center = (text_space - len(data.rstrip().lstrip())) // 2
                data = (Back.BLACK + Fore.WHITE + " " * __center +
                        Back.WHITE + Fore.BLACK + data.rstrip() + Back.BLACK + Fore.WHITE)

            if __right:
                if re.match("^<\[fill=.].*", data.lstrip().rstrip()) is None:
                    __center = text_space - len(data.lstrip().rstrip())
                    data = Back.BLACK + Fore.WHITE + " " * __center + Back.WHITE + Fore.BLACK + data.lstrip().rstrip() \
                           + Style.RESET_ALL
                else:
                    __format = True

        if re.match("^<\[fill=.].*", data.lstrip().rstrip()) is not None:
            fill = data.split("<[fill=", 1)[1][0]
            data = data.replace(f"<[fill={fill}]", "", 1)

            data = data.lstrip().rstrip()

            if __centred:
                if not __format:
                    data = data.center(text_space - len(data), fill)
            if __right:
                data = data.rjust(text_space, fill)
            else:
                data = data + (fill * (text_space - (len(data))))

        print(data, end=end)

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
