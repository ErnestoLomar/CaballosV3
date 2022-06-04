##########################################
# Autor: Ernesto Lomar
# Fecha de creación: 19/01/2022
# Ultima modificación: 22/05/2022
# 
# Software Carrera de barriles
#
##########################################

import cv2
import numpy as np
import imutils
import os
import sys
import time
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QGraphicsOpacityEffect

programa_activo = True

xy_uno = "380,120"
xy_dos = "380,480"
ultimo_dato_vuelta = ""
carpeta_fotos = 'Photos'

numero_de_caballo = 0

global valor_area
valor_area = 500.0

global numero
numero = ['+52']
global numero_area
numero_area = []

inicio_banner = time.time()

class principal(QMainWindow):

  def __init__(self):
    super().__init__()
    uic.loadUi("main_window.ui", self)

    global ventana_linea_meta
    ventana_linea_meta = finish_line_window()

    global dialog_estadistica
    dialog_estadistica = statistics_window(self)

    ventana_calibrar = area_window(self)
    
    self.btn_detectar.clicked.connect(self.deteccion)
    self.btn_terminar.clicked.connect(self.terminar_deteccion)
    self.btn_abrir_calibrar.clicked.connect(ventana_calibrar.show)
    self.btn_linea_de_meta.clicked.connect(ventana_linea_meta.mostrar_ventana_linea)
    self.btn_estadisticas.clicked.connect(dialog_estadistica.show)

    self.btn_terminar.hide()
    self.titulo_numero_vuelta_1.hide()
    self.titulo_numero_vuelta_2.hide()
    self.titulo_numero_vuelta_3.hide()
    self.titulo_numero_vuelta_4.hide()
    self.titulo_numero_vuelta_5.hide()
    

  #Creamos la función para terminar la detección de movimiento.
  def terminar_deteccion(self):
    global programa_activo
    if count > 0:
      programa_activo = False
      self.btn_terminar.hide()
      self.btn_detectar.show()
      self.label_titulo.show()
      cv2.destroyAllWindows()
      self.label_cronometro_actual.setText(f"00:00.000")
      dialog_estadistica.lista_tiempos.addItem("************************************************************")
    else:
      dialog_esperando.close()
      programa_activo = False
      self.btn_terminar.hide()
      self.btn_detectar.show()
      self.label_titulo.show()
      cv2.destroyAllWindows()
      self.label_cronometro_actual.setText(f"00:00.000")

  #Creamos la función para iniciar la detección de movimiento
  def deteccion(self):
    self.btn_detectar.hide()
    self.btn_terminar.show()
    self.label_frame_1.setPixmap(QtGui.QPixmap(""))
    self.label_frame_2.setPixmap(QtGui.QPixmap(""))
    self.label_frame_3.setPixmap(QtGui.QPixmap(""))
    self.label_frame_4.setPixmap(QtGui.QPixmap(""))
    self.label_frame_5.setPixmap(QtGui.QPixmap(""))
    self.titulo_numero_vuelta_1.hide()
    self.titulo_numero_vuelta_2.hide()
    self.titulo_numero_vuelta_3.hide()
    self.titulo_numero_vuelta_4.hide()
    self.titulo_numero_vuelta_5.hide()
    global numero_de_caballo
    numero_de_caballo +=1

    #Creamos la carpeta llamda "Fotos", donde se guardan las capturas del movimiento, 
    # si no existe la carpeta "Fotos" la cramos.
    if not os.path.exists(carpeta_fotos):
      print('Carpeta creada: ', carpeta_fotos)
      os.makedirs(carpeta_fotos)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW);
    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))

    #Declaramos variables locales de la función.
    
    #Instancias de clases.
    global dialog_esperando
    dialog_esperando = waiting_window(self)
    global programa_activo
    dialog_foto = popup_window(self)
    
    #Variables booleanas.
    programa_activo = True
    ventana_activa = False
    tiempo_de_espera = False
    cronometro_activo = False
    
    #Variables numéricas.
    global count
    count = 0
    global decimas, centecimas, milesimas
    decimas = 0
    centecimas = 0
    milesimas = 0
    i = 0
    minutos = 0
    horas = 0
    round_decimas = 2
    numero_de_frame = 1
    
    #Variables de cadena.
    tiempo_actual = ""

    while(programa_activo):

      if cronometro_activo:
        final_temporal = time.time()
        k = f"{final_temporal - inicio}"
        if final_temporal - inicio < 10:
          valor_tiempo = k [0:5]
        else:
          valor_tiempo = k [0:6]
        if round(final_temporal - inicio, 2) >= 60.00:
          minutos+=1
          inicio = time.time()
        if minutos >= 60:
          horas+=1
        if horas >= 99:
          sys.exit()
        if minutos <=9:
          self.label_cronometro_actual.setText(f"0{minutos}:{valor_tiempo}")
          tiempo_actual = f"0{minutos}:{valor_tiempo}"
        if minutos >= 10:
          self.label_cronometro_actual.setText(f"{minutos}:{valor_tiempo}")
          tiempo_actual = f"{minutos}:{valor_tiempo}"
        if float(valor_tiempo) < 10.0:
          self.label_cronometro_actual.setText(f"0{minutos}:0{valor_tiempo}")
          tiempo_actual = f"0{minutos}:0{valor_tiempo}"
          decimas = valor_tiempo[2:3]
          centecimas = valor_tiempo[3:4]
          milesimas = valor_tiempo[4:5]
        if float(valor_tiempo) >= 10.0:
          decimas = valor_tiempo[3:4]
          centecimas = valor_tiempo[4:5]
          milesimas = valor_tiempo[5:6]

      if ventana_activa:
        final2 = time.time()
        #print(f"Tiempo popup: {round(final2 - inicio, 1)}")
        if float(valor_tiempo) >= 3.00:
          dialog_foto.close()
          ventana_activa = False

      if tiempo_de_espera:
            final_espera = time.time()
            #print(f"Tiempo de espera: {round(final_espera - inicio_espera, 1)}")
            if float(valor_tiempo) >= 3.00:
              tiempo_de_espera = False

      ret,frame = cap.read()
      frame2 = imutils.resize(frame, width=480)
      if ret==False:break

      #CHECAR COORDENADAS DE LA PARTE DE LA IZQUIERDA PORQUE SE VA MUY LARGO

      area_pts = np.array([[int(xy_uno.split(sep=',')[0])+40, int(xy_uno.split(sep=',')[1])], [frame2.shape[1]-(int(xy_uno.split(sep=',')[0])), int(xy_uno.split(sep=',')[1])], 
      [frame2.shape[1]-(int(xy_dos.split(sep=',')[0])), int(xy_dos.split(sep=',')[1])], [int(xy_dos.split(sep=',')[0])+40, int(xy_dos.split(sep=',')[1])]])
      
      cv2.drawContours(frame2, [area_pts], -1, (0, 0, 255), 2)
      cv2.line(frame2, (int(xy_uno.split(sep=',')[0]), int(xy_uno.split(sep=',')[1])), (int(xy_dos.split(sep=',')[0]), int(xy_dos.split(sep=',')[1])), (0, 255, 255), 1)

      imAux = np.zeros(shape=(frame2.shape[:2]), dtype=np.uint8)
      imAux = cv2.drawContours(imAux, [area_pts], -1, (255), -1)
      image_area = cv2.bitwise_and(frame2, frame2, mask=imAux)


      fgmask = fgbg.apply(image_area)
      fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
      fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)
      fgmask = cv2.dilate(fgmask, None, iterations=1)

      if count == 0:
        dialog_esperando.show()
        inicio = time.time()
      if count == 1:
        dialog_esperando.close()

      if i == 10:
        inicio = time.time()
        cronometro_activo = True


      if i > 10:

        contornos = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        for c in contornos:
          #print("no se detecta movimiento")
          area = cv2.contourArea(c)
          # print(f"El area es: {area}")
          if area >= valor_area and tiempo_de_espera == False:
            #print(f"El area es: {area}")
            #print("se detecta movimiento")
            x,y,w,h = cv2.boundingRect(c)
            #cv2.rectangle(frame, (x,y), (x+w,y+h),(0,255,0))
            if (int(xy_uno.split(sep=',')[0])-20) < (x + w) < (int(xy_dos.split(sep=',')[0])+20):
              #print(f"----------------El area GANADORA es: {area}")
              #print("Detectado")
              cv2.line(frame2, (int(xy_uno.split(sep=',')[0]), int(xy_uno.split(sep=',')[1])), 
              (int(xy_dos.split(sep=',')[0]), int(xy_dos.split(sep=',')[1])), (0, 255, 0), 3)
            
              objeto = frame

              final = time.time()

              #print(f"La vuelta tardó {valor_tiempo} segundos.")
              tiempoDeVuelta = valor_tiempo

              cv2.imwrite(carpeta_fotos+'/vuelta_{}.jpg'.format(count),objeto)
              #print('Imagen almacenada: ', 'vuelta_{}.jpg'.format(count))

              hora_actual = time.ctime()
              hora_actual = hora_actual.split()

              #print(hora_actual[3])


              if count == 0:
                dialog_foto.label_foto.setPixmap(QtGui.QPixmap(carpeta_fotos+'/vuelta_{}.jpg'.format(count)))
                self.label_frame_1.setPixmap(QtGui.QPixmap(carpeta_fotos+'/vuelta_{}.jpg'.format(0)))
                self.titulo_numero_vuelta_1.show()
                self.titulo_numero_vuelta_1.setText(f'INICIO')
                #global numero_de_caballo
                #dialog_estadistica.titulo_estadisticas.setText(f'Estadísticas caballo {numero_de_caballo}')
                dialog_estadistica.lista_tiempos.addItem("************************************************************")
                dialog_estadistica.lista_tiempos.addItem(f"Caballo {numero_de_caballo} - COMIENZO DEL CRONÓMETRO - hora: {hora_actual[3]}")
                dialog_foto.label_tiempo.setStyleSheet("QLabel{\n"
"    \n"
"    font: 20pt \"Tw Cen MT Condensed Extra Bold\";\n"
"    color: rgb(255,255, 255);\n"
"}")
                dialog_foto.label_tiempo.setText("COMIENZO DEL CRONÓMETRO")
              else:
                if numero_de_frame == 2:
                  self.label_frame_2.setPixmap(QtGui.QPixmap(carpeta_fotos+'/vuelta_{}.jpg'.format(1)))
                  self.titulo_numero_vuelta_2.show()
                  self.titulo_numero_vuelta_2.setText('Vuelta 1')
                if numero_de_frame == 3:
                  self.label_frame_3.setPixmap(QtGui.QPixmap(carpeta_fotos+'/vuelta_{}.jpg'.format(2)))
                  self.titulo_numero_vuelta_3.show()
                  self.titulo_numero_vuelta_3.setText('Vuelta 2')
                if numero_de_frame == 4:
                  self.label_frame_4.setPixmap(QtGui.QPixmap(carpeta_fotos+'/vuelta_{}.jpg'.format(3)))
                  self.titulo_numero_vuelta_4.show()
                  self.titulo_numero_vuelta_4.setText('Vuelta 3')
                if numero_de_frame == 5:
                  self.label_frame_5.setPixmap(QtGui.QPixmap(carpeta_fotos+'/vuelta_{}.jpg'.format(4)))
                  self.titulo_numero_vuelta_5.show()
                  self.titulo_numero_vuelta_5.setText('Vuelta 4')
                if numero_de_frame > 5:
                  self.label_frame_5.setPixmap(QtGui.QPixmap(carpeta_fotos+'/vuelta_{}.jpg'.format(count)))
                  self.titulo_numero_vuelta_5.setText(f'Vuelta {count}')
                  self.label_frame_4.setPixmap(QtGui.QPixmap(carpeta_fotos+'/vuelta_{}.jpg'.format(count-1)))
                  self.titulo_numero_vuelta_4.setText(f'Vuelta {count-1}')
                  self.label_frame_3.setPixmap(QtGui.QPixmap(carpeta_fotos+'/vuelta_{}.jpg'.format(count-2)))
                  self.titulo_numero_vuelta_3.setText(f'Vuelta {count-2}')
                  self.label_frame_2.setPixmap(QtGui.QPixmap(carpeta_fotos+'/vuelta_{}.jpg'.format(count-3)))
                  self.titulo_numero_vuelta_2.setText(f'Vuelta {count-3}')
                  self.label_frame_1.setPixmap(QtGui.QPixmap(carpeta_fotos+'/vuelta_{}.jpg'.format(count-4)))
                  self.titulo_numero_vuelta_1.setText(f'Vuelta {count-4}')

                dialog_foto.label_foto.setPixmap(QtGui.QPixmap(carpeta_fotos+'/vuelta_{}.jpg'.format(count)))
                dialog_foto.label_tiempo.setStyleSheet("QLabel{\n"
"    \n"
"    font: 97 36pt \"Arial black\";\n"
"    color: rgb(255,255, 255);\n"
"}")
                dialog_foto.label_tiempo.setText(tiempo_actual)
                dialog_foto.label_numero_vuelta.setText(f"Vuelta {count}")
                dialog_estadistica.lista_tiempos.addItem(f"Vuelta {count} - {tiempo_actual} - hora: {hora_actual[3]}")
                global ultimo_dato_vuelta
                ultimo_dato_vuelta = f"Vuelta {count} - {tiempo_actual} - hora: {hora_actual[3]}"

              dialog_foto.show()
              numero_de_frame +=1


              inicio = time.time()
              minutos = 0
              horas = 0
            
              ventana_activa = True

            
              tiempo_de_espera = True
              inicio_espera = time.time()            

              count+=1

      #cv2.imshow('Detectando...', frame2)
      #cv2.imshow('Detectando...', frame2)
      #cv2.imshow("fgmask",fgmask)

      i = i +1
      k = cv2.waitKey(1)
      if k == 27:
        break
    cap.release()

class popup_window(QDialog):
  def __init__(self, *args, **kwargs):
    super(popup_window, self).__init__(*args, **kwargs)
    uic.loadUi("pop-up_capture.ui", self)
    self.label_foto.setScaledContents(True)

class waiting_window(QDialog):
  def __init__(self, *args, **kwargs):
    super(waiting_window, self).__init__(*args, **kwargs)
    uic.loadUi("waiting_window.ui", self)

class statistics_window(QDialog):
  def __init__(self, *args, **kwargs):
    super(statistics_window, self).__init__(*args, **kwargs)
    uic.loadUi("statistics_window.ui", self)
    self.btn_regresar.clicked.connect(self.close)

class finish_line_window(QDialog):
  def __init__(self, *args, **kwargs):
    global count_linea
    count_linea = 1
    super(finish_line_window, self).__init__(*args, **kwargs)
    uic.loadUi("finish_line_window.ui", self)
    self.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
    self.btn_meta_lista.clicked.connect(self.meta_lista)
    self.btn_cancelar_linea.clicked.connect(self.meta_lista)
    #self.btn_meta_lista.clicked.connect(self.close)
    self.setMouseTracking(True)
    self.opacity_effect_r = QGraphicsOpacityEffect()
    self.opacity_effect_g = QGraphicsOpacityEffect()
  
        # setting opacity level
    self.opacity_effect_r.setOpacity(0.3)
    self.opacity_effect_g.setOpacity(0.3)
  
        # adding opacity effect to the label
    self.label_rojo.setGraphicsEffect(self.opacity_effect_r)
    self.label_verde.setGraphicsEffect(self.opacity_effect_g)
    if not os.path.exists('fotogramas'):
      print('Carpeta creada: ', 'fotogramas')
      os.makedirs('fotogramas')

  def mousePressEvent(self, event):
      if event.button() == QtCore.Qt.LeftButton:
          variable = str(event.pos())
          variable2 = variable[20:]
          variable3 = variable2.replace(")","")
          global count_linea
          if count_linea == 1:
            global xy_uno
            xy_uno = variable3
            count_linea+=1
          elif count_linea == 2:
            global xy_dos 
            xy_dos = variable3
            count_linea=1
            cv2.line(frame21, (int(xy_uno.split(sep=',')[0]), int(xy_uno.split(sep=',')[1])), (int(xy_dos.split(sep=',')[0]), int(xy_dos.split(sep=',')[1])), (0, 255, 0), 3)
            cv2.imshow('Object Tracker', frame21)

  def mouseMoveEvent(self, event):
      QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.PointingHandCursor)

  def leaveEvent(self, event):
      QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.ArrowCursor)

  def meta_lista(self):
    global flag_editar_linea
    flag_editar_linea = False
    camara_frame.release()
    self.close()

  def cancelar_linea_meta(self):
    self.close()

  def mostrar_ventana_linea(self):
    global camara_frame
    camara_frame = cv2.VideoCapture(0, cv2.CAP_DSHOW);
    global flag_editar_linea
    flag_editar_linea = True
    count = 0
    self.show()
    while flag_editar_linea == True:
      ret,frame = camara_frame.read()


      global frame21
      frame21 = imutils.resize(frame, width=480)
      
      # cv2.namedWindow('Object Tracker')
      # cv2.setMouseCallback("Object Tracker", on_EVENT_LBUTTONDOWN)


      if ret==False:break
      cv2.imwrite('fotogramas/fotograma_{}.jpg'.format(count),frame21)
      self.fondo_linea_meta.setPixmap(QtGui.QPixmap('fotogramas/fotograma_{}.jpg'.format(count)))
      os.remove('fotogramas/fotograma_{}.jpg'.format(count))
      k = cv2.waitKey(1)
      if k == 27:
        break
    camara_frame.release()

class area_window(QDialog):
  def __init__(self, *args, **kwargs):
    super(area_window, self).__init__(*args, **kwargs)
    uic.loadUi("area_window.ui", self)
    self.btn_editar_area.clicked.connect(self.calibrar)
    self.label_area_actual.setText(f"El area actual es de: {valor_area}")
    self.btn_0.clicked.connect(self.agregar_cero)
    self.btn_1.clicked.connect(self.agregar_uno)
    self.btn_2.clicked.connect(self.agregar_dos)
    self.btn_3.clicked.connect(self.agregar_tres)
    self.btn_4.clicked.connect(self.agregar_cuatro)
    self.btn_5.clicked.connect(self.agregar_cinco)
    self.btn_6.clicked.connect(self.agregar_seis)
    self.btn_7.clicked.connect(self.agregar_siete)
    self.btn_8.clicked.connect(self.agregar_ocho)
    self.btn_9.clicked.connect(self.agregar_nueve)
    self.btn_del.clicked.connect(self.eliminar_ultimo)
    

  def eliminar_ultimo(self):
    try:
      numero_area.pop()
      numero_bien2 = "".join(numero_area)
      self.valor_areas.setText(numero_bien2)
    except:
      self.close()

  def agregar_cero(self):
    numero_area.append('0')
    numero_bien2 = "".join(numero_area)
    self.valor_areas.setText(numero_bien2)

  def agregar_uno(self):
    numero_area.append('1')
    numero_bien2 = "".join(numero_area)
    self.valor_areas.setText(numero_bien2)

  def agregar_dos(self):
    numero_area.append('2')
    numero_bien2 = "".join(numero_area)
    self.valor_areas.setText(numero_bien2)

  def agregar_tres(self):
    numero_area.append('3')
    numero_bien2 = "".join(numero_area)
    self.valor_areas.setText(numero_bien2)

  def agregar_cuatro(self):
    numero_area.append('4')
    numero_bien2 = "".join(numero_area)
    self.valor_areas.setText(numero_bien2)
  
  def agregar_cinco(self):
    numero_area.append('5')
    numero_bien2 = "".join(numero_area)
    self.valor_areas.setText(numero_bien2)

  def agregar_seis(self):
    numero_area.append('6')
    numero_bien2 = "".join(numero_area)
    self.valor_areas.setText(numero_bien2)

  def agregar_siete(self):
    numero_area.append('7')
    numero_bien2 = "".join(numero_area)
    self.valor_areas.setText(numero_bien2)

  def agregar_ocho(self):
    numero_area.append('8')
    numero_bien2 = "".join(numero_area)
    self.valor_areas.setText(numero_bien2)

  def agregar_nueve(self):
    numero_area.append('9')
    numero_bien2 = "".join(numero_area)
    self.valor_areas.setText(numero_bien2)

  def calibrar(self):
    global numero_area
    numero_area = []
    global valor_area
    try:
      valor_area = float(self.valor_areas.toPlainText())
      self.valor_areas.setText("")
      self.valor_areas.setStyleSheet("QTextEdit{\n"
"    \n"
"    background-color: rgb(49, 51, 89);\n"
"}")
      self.label_area_actual.setText(f"El area actual es de: {valor_area}")
      self.close()
    except:
      self.valor_areas.setStyleSheet("QTextEdit{\n"
"    \n"
"    background-color: rgb(255, 0, 0);\n"
"}")

if __name__ == '__main__':
  app = QApplication(sys.argv)
  GUI = principal()
  GUI.setWindowFlags(QtCore.Qt.CustomizeWindowHint)
  GUI.show()
  sys.exit(app.exec_())