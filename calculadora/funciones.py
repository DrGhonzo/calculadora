# importo libreria pandas como pd
import pandas as pd

# importo libreria pprint como pp
import pprint as pp

#importo libreria json
import json

#importo libreria numpy
import numpy as np

#importo libreria PyQt5
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

#importo libreria de systema
import sys
import math


def mi_funcion():  # "def" es una palabra reservada del interprete para definir funciones y metodos
    # una funcion es una porcion de codigo que puede ser reutilizada tantas veces como se desee siempre que sea invocada
    # de forma correcta
    print("Hola Max")
    pass


def suma(a, b):
    return a + b
    # print(c, a, b)


def resta(a, b):
    c = a - b
    print(c, a, b)


def multiplicacion(a, b):
    c = a * b
    print(c, a, b)


def division(a, b):

    if b != 0:  # los comparadores estan en el libro python para principiantes
        c = a / b
        print(c, a, b)
    else:
        print("cannot divide by zero asshole!!")


def raiz(indice, radicando):
    # TODO: implement a n root operation given two parameters indice and radicando
    '''
    la raiz si es par no admite radicaandos negativos
    la raiz si es impar admite radicandos tanto positivos como negativos
    :param indice:
    :param radicando:
    :return:
    '''

    n = indice
    a = radicando

    if n != 0:
        # indice es un exponente al que elevamos el radicando con la forma indice = 1/n
        if radicando < 0:
            if indice % 2 == 0:  # indice % 2 devuelve el resto de la division de indice por 2, 0 si es entero
                print("theres not real root for this shit")
            else:
                r = abs(a) ** (1/n)
                r *= -1  # (*=) es similar a hacer r = r * -1
                return r
        else:
            return a ** (1/n)
    else:
        print("cannot divide by zero")


class CalculadoraGO(QWidget):  # QWidget es la clase padre y accedo a sus atributos con "self."
    def __init__(self):
        super().__init__()

        # definimos una distribucion vertical de los componentes de la calculadora
        self.layout_vertical = QVBoxLayout()
        # definimos una distribucion horizontal de los componentes de la calculadora
        self.layout_horizontal = QHBoxLayout()

        self.display = QDoubleSpinBox()  # primero se crea la instancia del objeto

        self.display.setAlignment(Qt.AlignRight)  # se alinean los numeros a la derecha
        self.display.setButtonSymbols(QAbstractSpinBox.NoButtons)  # quitamos la vista de los botones de edicion
        self.display.setReadOnly(True)
        self.display.setMaximum(1000)

        self.layout_vertical.addWidget(self.display)


class Calculadora(CalculadoraGO):  # Calculadora hereda los atributos graficos de CalculadoraGO
    #  GO refiere siempre a Graphic Object

    # TODO:
    #   a + b - c = total  objeto valor y objeto funcion, cola de operaciones, ecolamos valor u/o operacion
    #   generar buffer de operaciones y buffer de funciones
    #   crear boton "clear" y "clear all" que limpie el buffer de operaciones y funciones y el historial
    #   optimizar _render_buttons para que ataje cualquier tipo de lista

    def __init__(self, name):
        CalculadoraGO.__init__(self)
        '''
        {
            boton:
                {
                 "nombre":'',
                 "tipo":'',
                 "valor":'',
                 "texto":'',
                 "funcion":'',
                 "operacion":'',
                 "icono":''   
                },
                {
                 "nombre":'',
                 "tipo":'',
                 "valor":'',
                 "texto":'',
                 "funcion":'',
                 "operacion":'',
                 "icono":''   
                }
        }
        '''

        self._numeros = [[7, 8, 9], [4, 5, 6], [1, 2, 3], ['png/mathematical-basic-signs-of-plus-and-minus-with-a-slash.png', 0, ","]]
        self._funciones = ['png/delete.png', 'png/navigation-history-interface-symbol-of-a-clock-with-an-arrow.png']
        self._operaciones = ["+", "-", "x", "/", "="]

        self.display.setMaximum((10 ** 5))
        self.display.setMinimum((-10 ** 5))
        self.display.setDecimals(0)

        self._buffer = []  #
        self._buffer_op = []  #
        self.name = name
        self._resultado = 0.0
        self.resultado_previo = []
        self.setWindowTitle(self.name)  # se llama a un metodo propio de QWidget, es es posible por la herencia

        self._fn_crea_botones()

        self.grupo_numeros.buttonClicked.connect(self.handler_button)
        self.grupo_operaciones.buttonClicked.connect(self.handler_button)
        self.grupo_funciones.buttonClicked.connect(self.handler_button)

    def _fn_crea_botones(self):
        #  creo una distribucion tipo grilla que permite acomodar los objetos graficos por fila, columna
        self.grilla_numeros = QGridLayout()

        #  creo un objeto que agrupa los botones
        self.grupo_numeros = QButtonGroup()

        self.grilla_operaciones = QGridLayout()

        self.grupo_operaciones = QButtonGroup()

        self.grilla_funciones = QGridLayout()

        self.grupo_funciones = QButtonGroup()

        # llamo a un metodo privado _render_buttons que crea y distribuye los botones en funcion de los argumentos pasados
        self._render_buttons(self._numeros, self.grilla_numeros, self.grupo_numeros)

        #
        #
        # llamo a un metodo privado _render_buttons que crea y distribuye los botones en funcion de los argumentos pasados
        self._render_buttons(self._operaciones, self.grilla_operaciones, self.grupo_operaciones)

        self._render_buttons(self._funciones, self.grilla_funciones, self.grupo_funciones)

        # agrego al layout vertical la grilla de numeros con el metodo .addLayout(layout)
        self.layout_vertical.addLayout(self.grilla_numeros)

        self.layout_vertical.addLayout(self.grilla_funciones)

        self.layout_horizontal.addLayout(self.layout_vertical)
        self.layout_horizontal.addLayout(self.grilla_operaciones)

        # seteamos el Layout principal del Widget con el metodo .setLayout(Layout)
        self.setLayout(self.layout_horizontal)

    def _render_buttons(self, _lista_botones, _grilla=None, _grupo=None):
        '''
        :param _lista_botones: lista de listas
        :param _grid: clase QGridLayOut
        :return: nada
        '''
        for row in _lista_botones:  # row es cada elemento en _lista_botones.
            for col in row:  # col es cada elemento de la lista en row
                # creo un objeto con el objeto pasado como parametro en _boton y lo alojo dentro de la grilla
                w = Boton()
                if type(col) is not int:
                    if type(col) is str and len(col) > 1:  # evaluamos si el str es largo o no (mayor a 1)
                        # problemas con esta línea que no renderiza el icono en el boton
                        w.setIcon(QIcon(col))
                    elif type(col) is str:
                        w.setObjectName(col)
                        w.setText(w.objectName())
                else:
                    w.set_numero(True)
                    w.setObjectName(str(col))
                    w.setText(w.objectName())

                # distribuyo los objetos dentro del layout
                # en funcion de su posicion dentro de la lista de listas _lista_botones
                # para ello utilizo el metodo de listas .index(objeto) que devuelve el indice del elemento
                # dentro de la lista que lo contiene
                _grilla.addWidget(w, _lista_botones.index(row), row.index(col))
                if _grupo is not None:
                    _grupo.addButton(w, row.index(col))

    def fn_genera_operacion(self, t):

        self.resultado_previo.append(self._resultado)
        print(t, self.resultado_previo)

        self._buffer = []

    def handler_button(self, sender):

        if not sender.es_numero():
            if sender.text() == "=":
                self._encolador(sender)
                for op in self._buffer_op:
                    if op == "+":
                        # print(self.suma(self.resultado_previo[-1], self.resultado_previo[-2]))
                        self.display.setValue(float(self.suma(self.resultado_previo[-1], self.resultado_previo[-2])))
                    if op == "-":
                        # print(self.suma(self.resultado_previo[-1], self.resultado_previo[-2]))
                        self.display.setValue(float(self.resta(self.resultado_previo[-1], self.resultado_previo[-2])))
                    if op == "x":
                        # print(self.suma(self.resultado_previo[-1], self.resultado_previo[-2]))
                        self.display.setValue(
                            float(self.multiplicacion(self.resultado_previo[-1], self.resultado_previo[-2])))
                    if op == "/":
                        # print(self.suma(self.resultado_previo[-1], self.resultado_previo[-2]))
                        self.display.setValue(float(self.division(self.resultado_previo[-2], self.resultado_previo[-1])))
            elif sender.text() == "C":
                self._buffer_op.clear()
                self.display.setValue(0)
            elif sender.text() == "A":
                self.display.setValue(self.resultado_previo[-1])
            else:
                self._encolador(sender)

        else:
            self.display.setDecimals(0)
            self.salida(int(sender.text()))
            # print(self._resultado)

    def suma(self, a, b):
        self.resultado_previo.append(a + b)
        return self.resultado_previo[-1]

    def resta(self, a, b):
        r = abs(a - b)
        if a > b:
            r *= -1
        self.resultado_previo.append(r)
        return self.resultado_previo[-1]

    def multiplicacion(self, a, b):
        self.resultado_previo.append(a * b)
        return self.resultado_previo[-1]

    def division(self, a, b):

        if b != 0:  # los comparadores estan en el libro python para principiantes
            r = a / b
            d, e = math.modf(r)
            self.display.setDecimals(len(str(d)))
            self.resultado_previo.append(r)
            return self.resultado_previo[-1]
        else:
            print("cannot divide by zero asshole!!")

    def salida(self, valor):
        self._resultado = 0
        self._buffer.append(valor)
        # print(self._buffer)

        #_rango = len(self._buffer) - 1
        for i, v in enumerate(reversed(self._buffer)):  # i = indice, v=valor en _buffer
            self._resultado += v * (10 ** i)  # elevando 10 a el indice, desplazamos el valor en decenas
        self.display.setValue(self._resultado)

    def _encolador(self, sender):
        self.resultado_previo.append(self._resultado)  # [1er_resultado]
        self._buffer_op.append(sender.text())
        self._resultado = 0.0
        self._buffer.clear()
        print(self.resultado_previo, self._buffer_op)


class BotonGo(QPushButton):

    send_valor = pyqtSignal(float)

    def __init__(self):
        super().__init__()


class Boton(BotonGo):

    emite_valor = pyqtSignal(str)  # definimos una señal custom que emite un string

    def __init__(self, icon_path=None):
        BotonGo.__init__(self)
        self._numero = False

    def set_numero(self, es_numero):
        '''

        :param es_numero: booleano
        :return:
        '''
        self._numero = es_numero

    def es_numero(self):
        return self._numero

    def set_icono(self, icono):
        icono = QIcon(QPixmap(icono))
        self.setIcon(icono)

    def mousePressEvent(self, e):

        if e.button() == Qt.LeftButton:
            _valor = self.objectName()
            self.emite_valor.emit(_valor)
            # importante retornar el super referenciando al boton (que hereda atributos de QPushButton) para que
            # siga su curso el "evento" disparado con el mouse
            return super(Boton, self).mousePressEvent(e)


if __name__ == '__main__':

    app = QApplication([])
    app.setStyle('Fusion')

    objeto = Calculadora('calculadora_1')
    objeto.show()

    sys.exit(app.exec_())


"""
    1 - ingreso un numero por la botonera
    1.1 - encolo lo numeros en un arreglo (array, lista) de elementos que formen un valor con cantidad de digitos mayores o iguales a 1
    1.2 - muestro el numero formado
    1.3 - guardo en un arreglo (array, lista) de valores a operar
     
    2 - ingreso una funcion por la botonera
    2.1 - obtener el simbolo de la operacion desde el boton y generar una operacion lista a ser lanzada
    2.2 - guardo la operacion en un arreglo (array, lista) de operaciones a realizar
    
    3 - ingreso el segundo numero por la botonera (repite pasos en 1)
    
    4 - obtengo el resultado de la funcion
    4.1 - realizo recorro el arreglo (array, lista) de operaciones y realizando las operaciones e impactando en el resultado


"""