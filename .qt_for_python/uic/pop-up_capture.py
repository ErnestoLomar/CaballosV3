# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\Ernesto Lomar\Desktop\CaballosV3\pop-up_capture.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Fotograma(object):
    def setupUi(self, Fotograma):
        Fotograma.setObjectName("Fotograma")
        Fotograma.resize(487, 420)
        Fotograma.setMinimumSize(QtCore.QSize(420, 420))
        Fotograma.setMaximumSize(QtCore.QSize(520, 420))
        self.label_fondo_foto = QtWidgets.QLabel(Fotograma)
        self.label_fondo_foto.setGeometry(QtCore.QRect(0, 0, 520, 460))
        self.label_fondo_foto.setMinimumSize(QtCore.QSize(520, 460))
        self.label_fondo_foto.setMaximumSize(QtCore.QSize(520, 460))
        self.label_fondo_foto.setStyleSheet("background-color: rgb(91, 57, 36);")
        self.label_fondo_foto.setText("")
        self.label_fondo_foto.setScaledContents(True)
        self.label_fondo_foto.setObjectName("label_fondo_foto")
        self.label_foto = QtWidgets.QLabel(Fotograma)
        self.label_foto.setGeometry(QtCore.QRect(20, 90, 441, 320))
        self.label_foto.setMinimumSize(QtCore.QSize(400, 300))
        self.label_foto.setMaximumSize(QtCore.QSize(480, 360))
        self.label_foto.setStyleSheet("")
        self.label_foto.setText("")
        self.label_foto.setScaledContents(True)
        self.label_foto.setObjectName("label_foto")
        self.label_numero_vuelta = QtWidgets.QLabel(Fotograma)
        self.label_numero_vuelta.setGeometry(QtCore.QRect(20, 90, 141, 41))
        self.label_numero_vuelta.setStyleSheet("font: bold 9pt \"AcadEref\";\n"
"color: rgb(0,0,0);\n"
"background-color: rgb(255, 159, 28);")
        self.label_numero_vuelta.setAlignment(QtCore.Qt.AlignCenter)
        self.label_numero_vuelta.setObjectName("label_numero_vuelta")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Fotograma)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 481, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_tiempo = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(10)
        self.label_tiempo.setFont(font)
        self.label_tiempo.setStyleSheet("color: rgb(255, 255, 255);\n"
"font: 87 26pt \"Arial Black\";")
        self.label_tiempo.setAlignment(QtCore.Qt.AlignCenter)
        self.label_tiempo.setObjectName("label_tiempo")
        self.horizontalLayout.addWidget(self.label_tiempo)

        self.retranslateUi(Fotograma)
        QtCore.QMetaObject.connectSlotsByName(Fotograma)

    def retranslateUi(self, Fotograma):
        _translate = QtCore.QCoreApplication.translate
        Fotograma.setWindowTitle(_translate("Fotograma", "Fotografía caballo"))
        self.label_numero_vuelta.setText(_translate("Fotograma", "Comienzo"))
        self.label_tiempo.setText(_translate("Fotograma", "00:00.0"))
