# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
from matplotlib.pyplot import get_current_fig_manager
__author__="acannia"
__date__ ="$16-02-2014 01:07:02 AM$"

from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from acciones_dia import asset_dia
from read_csv import read_csv 
import matplotlib.pyplot as plt
from operator import itemgetter
from matplotlib.ticker import ScalarFormatter, FormatStrFormatter, FuncFormatter 
from datetime import date
import numpy as np
import sys
import os

class MessageBox(QtGui.QWidget):
     def __init__(self, parent=None):
         QtGui.QWidget.__init__(self, parent)

         self.setGeometry(300, 300, 250, 150)
         self.setWindowTitle('Error')
         
class MyWindow(QtGui.QMainWindow):
    figura = []        

    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        self.connect(self.b_historicos, SIGNAL('clicked()'), self.archivo_historicos)
        self.connect(self.b_dactual, SIGNAL('clicked()'), self.archivo_dactual)
        
        self.p_simil.setValue(100-self.p_gap.value())
        self.connect(self.b_graficar, SIGNAL('clicked()'), self.main3)
        self.connect(self.b_graficar_test, SIGNAL('clicked()'), self.main4)
        self.line_historicos.setText(os.path.join(os.path.abspath(""),'CLPUSD.txt'))
        self.line_dactual.setText(os.path.join(os.path.abspath(""),'CLPtoday.txt'))
        self.connect(self.p_gap, SIGNAL("valueChanged(int)"),self.setValue_spinbox)

        self.show()
        
    
    def setValue_spinbox(self):
        self.p_simil.setValue(100-self.p_gap.value())
    
    def archivo_historicos(self):
        file = str(QtGui.QFileDialog.getOpenFileName(self, 'Abrir Archivo', os.path.expanduser('~'), "Archivos de datos (*.csv *.txt)"))
        if file == "":
            file = ""
        else:
            self.line_historicos.setText(file)

    def archivo_dactual(self):
        file = str(QtGui.QFileDialog.getOpenFileName(self, 'Abrir Archivo', os.path.expanduser('~'), "Archivos de datos (*.csv *.txt)"))
        if file == "":
            file = ""
        else:
            self.line_dactual.setText(file)
    
            
    def main3(self):
        self.figura = []
        for i in range(0, self.dias_graf.value()):
            self.figura.append(plt.figure(i)) 
        print str(self.Indicador.currentText())
        graficos(self.dias_graf.value(), self.x.value(), self.y.value(), str(self.Indicador.currentText()), self.line_historicos.text(), self.line_dactual.text(), self.p_gap.value(),0, "", "" ,self.figura)

    def main4(self):
        self.figura = []
        for i in range(0, self.dias_graf.value()):
            self.figura.append(plt.figure(i)) 
        print str(self.Indicador.currentText())
        fecha = self.date.date().toString("MM/dd/yyyy")
        hora = int(self.hora.time().toString("HHmm"))
        graficos(self.dias_graf.value(), self.x.value(), self.y.value(), str(self.Indicador.currentText()), self.line_historicos.text(), self.line_dactual.text(), self.p_gap.value(),1, fecha, hora, self.figura)

def pre_procesamiento(data_close, data_time_v, HI=900, HF = 1430, date = "01/01/1900", x = 14, y = 14, texto = "RSI(x)"):

    #Se leen las acciones del dia 1
    accion = data_close
    time = data_time_v
    DT = 1
    
    #Se procesan las acciones del dia 1
    acc = asset_dia(accion, time, DT, HI, HF, date)
    
    if len(acc.acciones) == 0:
        return acc
    
    #Utiliza el RSI solo
    if texto == "RSI(X)":
        acc.calculo_RSI(x)
    
    #Utiliza el promedio del STO para una ventana de 15 datos
    if texto == "STO(DF(),x)":
        acc.calculo_STO_mean(x)
    
    #Utiliza el promedio del STO para una ventana de 15 datos y un n2 para el EMA
    if texto == "STO(EMA(y),x)":
        acc.calculo_STO_EMA(x, y)
    
    #Utiliza el STO de los datos para una ventana de 15 datos
    if texto == "STO(x)":
        acc.calculo_STO(x)
        
    #Utiliza el promedio del RSI
    if texto == "RSI(DF(),x)":
        acc.calculo_RSI_AVG(x)

    #Utiliza el promedio del RSI
    if texto == "RSI(EMA(y),x)":
        acc.calculo_RSI_EMA(x, y)
    
    #Normaliza los datos de acciones
    #if texto == "RSI(X)":
    #    acc.calculo_Normalizacion()
    
    return acc

#Estrategia que se utiliza para r los datos con bajo ECM
def graficos(cant_dias_eval = 15, x = 14, y = 14, texto = "RSI(x)", archivo1 = "CLP900.txt", archivo2 = "CLP_Hoy.txt", porcentaje = 0.0, hist = 0, fecha = "01/01/2014", hora = "1000", figures = []):
#dia es el dia que se desea r con datos anteriores en formato '01/01/1900'
#es la hora final donde se desea r en formato string de '0901' hasta '1329'
    
    print "Comiezo pre-procesamiento"
    data = read_csv(archivo1)
    if hist == 0:
        data_hoy = read_csv(archivo2)
    else:
        data_hoy = read_csv("aa")
        indice_dia = 0
        largo_data = len(data.data_close)
        for i in range(0, largo_data):
            if data.data_date[i][0] == fecha:
                indice_dia = i
                break
        
        indice = data.data_time[indice_dia].index(hora)
        data_hoy.data_open.append(data.data_open[indice_dia][0:indice])
        data_hoy.data_close.append(data.data_close[indice_dia][0:indice])
        data_hoy.data_high.append(data.data_high[indice_dia][0:indice])
        data_hoy.data_low.append(data.data_low[indice_dia][0:indice])
        data_hoy.data_date.append(data.data_date[indice_dia][0:indice])
        data_hoy.data_time.append(data.data_time[indice_dia][0:indice])
        data_hoy.max_hora = hora
        data_hoy.min_hora = data.min_hora 
        
    largo = len(data.data_close)
    acciones_hoy = pre_procesamiento(data_hoy.data_close[0], data_hoy.data_time[0], data.min_hora, data_hoy.max_hora, data_hoy.data_date[0], x, y, texto)
    
    n_hora = len(acciones_hoy.acciones)
    
    acc = []
    fitness = []
    largo_dia = 0

    for i in range(0, largo):
        acc_aux = pre_procesamiento(data.data_close[i], data.data_time[i], data.min_hora, data.max_hora, data.data_date[i], x, y, texto)
        if largo_dia < int(data.data_time[i][-1]):
            largo_dia = int(data.data_time[i][-1])
            
        if (len(acc_aux.acciones) == 0) | (len(acciones_hoy.acciones) == 0) | (n_hora > len(acc_aux.acciones)-1):
            continue
        
        try:
            acc_aux.fitness = acc_aux.acciones[-1] - acc_aux.acciones[n_hora+1]
        except ValueError:
            print "error"
            continue
        
        fitness.append(acc_aux.fitness)
        acc.append(acc_aux)

    #Se buscan los N dias mas similares 
    Similes, fit_sim, Ns = similitud(cant_dias_eval, acc, acciones_hoy, porcentaje)
    yFormatter = FormatStrFormatter('%.2f')
    
    ax0 = figures[0].add_subplot(111)
    mes, dia, ano = acciones_hoy.date.split('/')
    fecha = date(int(ano), int(mes), int(dia))
    ax0.set_title('%s' % (fecha.strftime("%A %d, %B %Y") ))
    
    if cant_dias_eval > 1:
        ax1 = figures[1].add_subplot(111)
    if cant_dias_eval > 2:    
        ax2 = figures[2].add_subplot(111)
    if cant_dias_eval > 3:    
        ax3 = figures[3].add_subplot(111)
    if cant_dias_eval > 4:    
        ax4 = figures[4].add_subplot(111)
    if cant_dias_eval > 5:    
        ax5 = figures[5].add_subplot(111)
    if cant_dias_eval > 6:    
        ax6 = figures[6].add_subplot(111)
    if cant_dias_eval > 7:    
        ax7 = figures[7].add_subplot(111)
    if cant_dias_eval > 8:    
        ax8 = figures[8].add_subplot(111)
    if cant_dias_eval > 9:    
        ax9 = figures[9].add_subplot(111)
    if cant_dias_eval > 10:    
        ax10 = figures[10].add_subplot(111)
    if cant_dias_eval > 11:    
        ax11 = figures[11].add_subplot(111)
    if cant_dias_eval > 12:    
        ax12 = figures[12].add_subplot(111)
    if cant_dias_eval > 13:    
        ax13 = figures[13].add_subplot(111)
    if cant_dias_eval > 14:    
        ax14 = figures[14].add_subplot(111)
    if cant_dias_eval > 15:    
        ax15 = figures[15].add_subplot(111)
    if cant_dias_eval > 16:    
        ax16 = figures[16].add_subplot(111)


    ax0.plot(acciones_hoy.acciones_mean)    
    ax0.grid()
    ax0.yaxis.set_major_formatter(yFormatter)

    if cant_dias_eval > 1:
        ax1.plot(acc[Ns[0]].acciones)
        ax1.plot(acc[Ns[0]].acciones_mean)
        ax1.grid()
        ax1.plot(n_hora, acc[Ns[0]].acciones[n_hora], 'o')
        largo_dia = len(acc[Ns[0]].acciones)
        ax1.plot(largo_dia, acc[Ns[0]].acciones[-1], b'o')
        ax1.text(n_hora, acc[Ns[0]].acciones[n_hora], acc[Ns[0]].acciones[n_hora], fontsize=11)
        ax1.text(largo_dia, acc[Ns[0]].acciones[-1], acc[Ns[0]].acciones[-1], fontsize=11)
        
        mes, dia, ano = acc[Ns[0]].date.split('/')
        fecha = date(int(ano), int(mes), int(dia))
        gap = acc[Ns[0]].acciones[0] - acc[Ns[0]-1].acciones[-1]
        gap_p = 100*(acc[Ns[0]].acciones[0] - acc[Ns[0]-1].acciones[-1])/acc[Ns[0]-1].acciones[-1]
        
        ax1.set_title('%s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[0], acc[Ns[0]].fitness, gap, gap_p) )
        print 'Fecha : %s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[0], acc[Ns[0]].fitness, gap, gap_p)
        ax1.yaxis.set_major_formatter(yFormatter)
    
    if cant_dias_eval > 2:    
        ax2.plot(acc[Ns[1]].acciones)
        ax2.plot(acc[Ns[1]].acciones_mean)
        ax2.grid()
        ax2.plot(n_hora, acc[Ns[1]].acciones[n_hora], 'o')
        largo_dia = len(acc[Ns[1]].acciones)
        ax2.plot(largo_dia, acc[Ns[1]].acciones[-1], b'o')
        ax2.text(n_hora, acc[Ns[1]].acciones[n_hora], acc[Ns[1]].acciones[n_hora], fontsize=11)
        ax2.text(largo_dia, acc[Ns[1]].acciones[-1], acc[Ns[1]].acciones[-1], fontsize=11)
        
        mes, dia, ano = acc[Ns[1]].date.split('/')
        fecha = date(int(ano), int(mes), int(dia))
        gap = acc[Ns[1]].acciones[0] - acc[Ns[1]-1].acciones[-1]
        gap_p = 100*(acc[Ns[1]].acciones[0] - acc[Ns[1]-1].acciones[-1])/acc[Ns[1]-1].acciones[-1]
        
        ax2.set_title('%s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[1], acc[Ns[1]].fitness, gap, gap_p) )
        print 'Fecha : %s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[1], acc[Ns[1]].fitness, gap, gap_p)
        ax2.yaxis.set_major_formatter(yFormatter)
    
    if cant_dias_eval > 3:
        ax3.plot(acc[Ns[2]].acciones)
        ax3.plot(acc[Ns[2]].acciones_mean)
        ax3.grid()
        ax3.plot(n_hora, acc[Ns[2]].acciones[n_hora], 'o')
        largo_dia = len(acc[Ns[2]].acciones)
        ax3.plot(largo_dia,  acc[Ns[2]].acciones[-1], b'o')
        ax3.text(n_hora, acc[Ns[2]].acciones[n_hora], acc[Ns[2]].acciones[n_hora], fontsize=11)
        ax3.text(largo_dia, acc[Ns[2]].acciones[-1], acc[Ns[2]].acciones[-1], fontsize=11)
        
        mes, dia, ano = acc[Ns[2]].date.split('/')
        fecha = date(int(ano), int(mes), int(dia))
        gap = acc[Ns[2]].acciones[0] - acc[Ns[2]-1].acciones[-1]
        gap_p = 100*(acc[Ns[2]].acciones[0] - acc[Ns[2]-1].acciones[-1])/acc[Ns[2]-1].acciones[-1]
        
        ax3.set_title('%s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[2], acc[Ns[2]].fitness , gap, gap_p) )
        print 'Fecha : %s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[2], acc[Ns[2]].fitness , gap, gap_p) 
        ax3.yaxis.set_major_formatter(yFormatter)

    if cant_dias_eval > 4:    
        ax4.plot(acc[Ns[3]].acciones)
        ax4.plot(acc[Ns[3]].acciones_mean)
        ax4.grid()
        ax4.plot(n_hora, acc[Ns[3]].acciones[n_hora], 'o')
        largo_dia = len(acc[Ns[3]].acciones)
        ax4.plot(largo_dia,  acc[Ns[3]].acciones[-1], b'o')
        ax4.text(n_hora, acc[Ns[3]].acciones[n_hora], acc[Ns[3]].acciones[n_hora], fontsize=11)
        ax4.text(largo_dia, acc[Ns[3]].acciones[-1], acc[Ns[3]].acciones[-1], fontsize=11)
        
        mes, dia, ano = acc[Ns[3]].date.split('/')
        fecha = date(int(ano), int(mes), int(dia))
        gap = acc[Ns[3]].acciones[0] - acc[Ns[3]-1].acciones[-1]
        gap_p = 100*(acc[Ns[3]].acciones[0] - acc[Ns[3]-1].acciones[-1])/acc[Ns[3]-1].acciones[-1]
        
        ax4.set_title('%s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[3], acc[Ns[3]].fitness, gap, gap_p) )
        print 'Fecha : %s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[3], acc[Ns[3]].fitness, gap, gap_p)
        ax4.yaxis.set_major_formatter(yFormatter)
        
    if cant_dias_eval > 5:    
        ax5.plot(acc[Ns[4]].acciones)
        ax5.plot(acc[Ns[4]].acciones_mean)
        ax5.grid()
        ax5.plot(n_hora, acc[Ns[4]].acciones[n_hora], 'o')
        largo_dia = len(acc[Ns[4]].acciones)
        ax5.plot(largo_dia, acc[Ns[4]].acciones[-1], b'o')
        ax5.text(n_hora, acc[Ns[4]].acciones[n_hora], acc[Ns[4]].acciones[n_hora], fontsize=11)
        ax5.text(largo_dia, acc[Ns[4]].acciones[-1], acc[Ns[4]].acciones[-1], fontsize=11)
        
        mes, dia, ano = acc[Ns[4]].date.split('/')
        fecha = date(int(ano), int(mes), int(dia))
        gap = acc[Ns[4]].acciones[0] - acc[Ns[4]-1].acciones[-1]
        gap_p = 100*(acc[Ns[4]].acciones[0] - acc[Ns[4]-1].acciones[-1])/acc[Ns[4]-1].acciones[-1]
        
        ax5.set_title('%s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[4], acc[Ns[4]].fitness, gap, gap_p) )
        print 'Fecha : %s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[4], acc[Ns[4]].fitness, gap, gap_p)
        ax5.yaxis.set_major_formatter(yFormatter)
          
    if cant_dias_eval > 6:    
        ax6.plot(acc[Ns[5]].acciones)
        ax6.plot(acc[Ns[5]].acciones_mean)
        ax6.grid()
        ax6.plot(n_hora, acc[Ns[5]].acciones[n_hora], 'o')
        largo_dia = len(acc[Ns[5]].acciones)
        ax6.plot(largo_dia, acc[Ns[5]].acciones[-1], b'o')
        ax6.text(n_hora, acc[Ns[5]].acciones[n_hora], acc[Ns[5]].acciones[n_hora], fontsize=11)
        ax6.text(largo_dia, acc[Ns[5]].acciones[-1], acc[Ns[5]].acciones[-1], fontsize=11)
        
        mes, dia, ano = acc[Ns[5]].date.split('/')
        fecha = date(int(ano), int(mes), int(dia))
        gap = acc[Ns[5]].acciones[0] - acc[Ns[5]-1].acciones[-1]
        gap_p = 100*(acc[Ns[5]].acciones[0] - acc[Ns[5]-1].acciones[-1])/acc[Ns[5]-1].acciones[-1]
        
        ax6.set_title('%s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[5], acc[Ns[5]].fitness, gap, gap_p) )
        print 'Fecha : %s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[5], acc[Ns[5]].fitness, gap, gap_p) 
        ax6.yaxis.set_major_formatter(yFormatter)
          
    if cant_dias_eval > 7:    
        ax7.plot(acc[Ns[6]].acciones)
        ax7.plot(acc[Ns[6]].acciones_mean)
        ax7.grid()
        ax7.plot(n_hora, acc[Ns[6]].acciones[n_hora], 'o')
        largo_dia = len(acc[Ns[6]].acciones)
        ax7.plot(largo_dia, acc[Ns[6]].acciones[-1], b'o')
        ax7.text(n_hora, acc[Ns[6]].acciones[n_hora], acc[Ns[6]].acciones[n_hora], fontsize=11)
        ax7.text(largo_dia, acc[Ns[6]].acciones[-1], acc[Ns[6]].acciones[-1], fontsize=11)
        
        mes, dia, ano = acc[Ns[6]].date.split('/')
        fecha = date(int(ano), int(mes), int(dia))
        gap = acc[Ns[6]].acciones[0] - acc[Ns[6]-1].acciones[-1]
        gap_p = 100*(acc[Ns[6]].acciones[0] - acc[Ns[6]-1].acciones[-1])/acc[Ns[6]-1].acciones[-1]
        
        ax7.set_title('%s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[6], acc[Ns[6]].fitness, gap, gap_p) )
        print 'Fecha : %s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[6], acc[Ns[6]].fitness, gap, gap_p) 
        ax7.yaxis.set_major_formatter(yFormatter)
          
    if cant_dias_eval > 8:    
        ax8.plot(acc[Ns[7]].acciones)
        ax8.plot(acc[Ns[7]].acciones_mean)
        ax8.grid()
        ax8.plot(n_hora, acc[Ns[7]].acciones[n_hora], 'o')
        largo_dia = len(acc[Ns[7]].acciones)
        ax8.plot(largo_dia, acc[Ns[7]].acciones[-1], b'o')
        ax8.text(n_hora, acc[Ns[7]].acciones[n_hora], acc[Ns[7]].acciones[n_hora], fontsize=11)
        ax8.text(largo_dia, acc[Ns[7]].acciones[-1], acc[Ns[7]].acciones[-1], fontsize=11)
        
        mes, dia, ano = acc[Ns[7]].date.split('/')
        fecha = date(int(ano), int(mes), int(dia))
        gap = acc[Ns[7]].acciones[0] - acc[Ns[7]-1].acciones[-1]
        gap_p = 100*(acc[Ns[7]].acciones[0] - acc[Ns[7]-1].acciones[-1])/acc[Ns[7]-1].acciones[-1]
        
        ax8.set_title('%s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[7], acc[Ns[7]].fitness, gap, gap_p) )
        print 'Fecha : %s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[7], acc[Ns[7]].fitness, gap, gap_p) 
        ax8.yaxis.set_major_formatter(yFormatter)
          
    if cant_dias_eval > 9:    
        ax9.plot(acc[Ns[8]].acciones)
        ax9.plot(acc[Ns[8]].acciones_mean)
        ax9.grid()
        ax9.plot(n_hora, acc[Ns[8]].acciones[n_hora], 'o')
        largo_dia = len(acc[Ns[8]].acciones)
        ax9.plot(largo_dia, acc[Ns[8]].acciones[-1], b'o')
        ax9.text(n_hora, acc[Ns[8]].acciones[n_hora], acc[Ns[8]].acciones[n_hora], fontsize=11)
        ax9.text(largo_dia, acc[Ns[8]].acciones[-1], acc[Ns[8]].acciones[-1], fontsize=11)
        
        mes, dia, ano = acc[Ns[8]].date.split('/')
        fecha = date(int(ano), int(mes), int(dia))
        gap = acc[Ns[8]].acciones[0] - acc[Ns[8]-1].acciones[-1]
        gap_p = 100*(acc[Ns[8]].acciones[0] - acc[Ns[8]-1].acciones[-1])/acc[Ns[8]-1].acciones[-1]
        
        ax9.set_title('%s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[8], acc[Ns[8]].fitness, gap, gap_p) )
        print 'Fecha : %s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[8], acc[Ns[8]].fitness, gap, gap_p)
        ax9.yaxis.set_major_formatter(yFormatter)
          
    if cant_dias_eval > 10:    
        ax10.plot(acc[Ns[9]].acciones)
        ax10.plot(acc[Ns[9]].acciones_mean)
        ax10.grid()
        ax10.plot(n_hora, acc[Ns[9]].acciones[n_hora], 'o')
        largo_dia = len(acc[Ns[9]].acciones)
        ax10.plot(largo_dia, acc[Ns[9]].acciones[-1], b'o')
        ax10.text(n_hora, acc[Ns[9]].acciones[n_hora], acc[Ns[9]].acciones[n_hora], fontsize=11)
        ax10.text(largo_dia, acc[Ns[9]].acciones[-1], acc[Ns[9]].acciones[-1], fontsize=11)
        
        mes, dia, ano = acc[Ns[9]].date.split('/')
        fecha = date(int(ano), int(mes), int(dia))
        gap = acc[Ns[9]].acciones[0] - acc[Ns[9]-1].acciones[-1]
        gap_p = 100*(acc[Ns[9]].acciones[0] - acc[Ns[9]-1].acciones[-1])/acc[Ns[9]-1].acciones[-1]
        
        ax10.set_title('%s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[9], acc[Ns[9]].fitness, gap, gap_p) )
        print 'Fecha : %s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[9], acc[Ns[9]].fitness, gap, gap_p) 
        ax10.yaxis.set_major_formatter(yFormatter)
          
    if cant_dias_eval > 11:    
        ax11.plot(acc[Ns[10]].acciones)
        ax11.plot(acc[Ns[10]].acciones_mean)
        ax11.grid()
        ax11.plot(n_hora, acc[Ns[10]].acciones[n_hora], 'o')
        largo_dia = len(acc[Ns[10]].acciones)
        ax11.plot(largo_dia, acc[Ns[10]].acciones[-1], b'o')
        ax11.text(n_hora, acc[Ns[10]].acciones[n_hora], acc[Ns[10]].acciones[n_hora], fontsize=11)
        ax11.text(largo_dia, acc[Ns[10]].acciones[-1], acc[Ns[10]].acciones[-1], fontsize=11)
        
        mes, dia, ano = acc[Ns[10]].date.split('/')
        fecha = date(int(ano), int(mes), int(dia))
        gap = acc[Ns[10]].acciones[0] - acc[Ns[10]-1].acciones[-1]
        gap_p = 100*(acc[Ns[10]].acciones[0] - acc[Ns[10]-1].acciones[-1])/acc[Ns[10]-1].acciones[-1]
        
        ax11.set_title('%s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[10], acc[Ns[10]].fitness, gap, gap_p) )
        print 'Fecha : %s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[10], acc[Ns[10]].fitness, gap, gap_p) 
        ax11.yaxis.set_major_formatter(yFormatter)
          
    if cant_dias_eval > 12:    
        ax12.plot(acc[Ns[11]].acciones)
        ax12.plot(acc[Ns[11]].acciones_mean)
        ax12.grid()
        ax12.plot(n_hora, acc[Ns[11]].acciones[n_hora], 'o')
        largo_dia = len(acc[Ns[11]].acciones)
        ax12.plot(largo_dia, acc[Ns[11]].acciones[-1], b'o')
        ax12.text(n_hora, acc[Ns[11]].acciones[n_hora], acc[Ns[11]].acciones[n_hora], fontsize=11)
        ax12.text(largo_dia, acc[Ns[11]].acciones[-1], acc[Ns[11]].acciones[-1], fontsize=11)
        
        mes, dia, ano = acc[Ns[11]].date.split('/')
        fecha = date(int(ano), int(mes), int(dia))
        gap = acc[Ns[11]].acciones[0] - acc[Ns[11]-1].acciones[-1]
        gap_p = 100*(acc[Ns[11]].acciones[0] - acc[Ns[11]-1].acciones[-1])/acc[Ns[11]-1].acciones[-1]
        
        ax12.set_title('%s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[11], acc[Ns[11]].fitness, gap, gap_p) )
        print 'Fecha : %s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[11], acc[Ns[11]].fitness, gap, gap_p) 
        ax12.yaxis.set_major_formatter(yFormatter)
          
    if cant_dias_eval > 13:    
        ax13.plot(acc[Ns[12]].acciones)
        ax13.plot(acc[Ns[12]].acciones_mean)
        ax13.grid()
        ax13.plot(n_hora, acc[Ns[12]].acciones[n_hora], 'o')
        largo_dia = len(acc[Ns[12]].acciones)
        ax13.plot(largo_dia, acc[Ns[12]].acciones[-1], b'o')
        ax13.text(n_hora, acc[Ns[12]].acciones[n_hora], acc[Ns[12]].acciones[n_hora], fontsize=11)
        ax13.text(largo_dia, acc[Ns[12]].acciones[-1], acc[Ns[12]].acciones[-1], fontsize=11)
        
        mes, dia, ano = acc[Ns[12]].date.split('/')
        fecha = date(int(ano), int(mes), int(dia))
        gap = acc[Ns[12]].acciones[0] - acc[Ns[12]-1].acciones[-1]
        gap_p = 100*(acc[Ns[12]].acciones[0] - acc[Ns[12]-1].acciones[-1])/acc[Ns[12]-1].acciones[-1]
        
        ax13.set_title('%s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[12], acc[Ns[12]].fitness, gap, gap_p) )
        print 'Fecha : %s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[12], acc[Ns[12]].fitness, gap, gap_p)
        ax13.yaxis.set_major_formatter(yFormatter)
          
    if cant_dias_eval > 14:    
        ax14.plot(acc[Ns[13]].acciones)
        ax14.plot(acc[Ns[13]].acciones_mean)
        ax14.grid()
        ax14.plot(n_hora, acc[Ns[13]].acciones[n_hora], 'o')
        largo_dia = len(acc[Ns[13]].acciones)
        ax14.plot(largo_dia, acc[Ns[13]].acciones[-1], b'o')
        ax14.text(n_hora, acc[Ns[13]].acciones[n_hora], acc[Ns[13]].acciones[n_hora], fontsize=11)
        ax14.text(largo_dia, acc[Ns[13]].acciones[-1], acc[Ns[13]].acciones[-1], fontsize=11)
        
        mes, dia, ano = acc[Ns[13]].date.split('/')
        fecha = date(int(ano), int(mes), int(dia))
        gap = acc[Ns[13]].acciones[0] - acc[Ns[13]-1].acciones[-1]
        gap_p = 100*(acc[Ns[13]].acciones[0] - acc[Ns[13]-1].acciones[-1])/acc[Ns[13]-1].acciones[-1]
        
        ax14.set_title('%s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[13], acc[Ns[13]].fitness, gap, gap_p) )
        print 'Fecha : %s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[13], acc[Ns[13]].fitness, gap, gap_p)
        ax14.yaxis.set_major_formatter(yFormatter)
          
    if cant_dias_eval > 15:    
        ax15.plot(acc[Ns[14]].acciones)
        ax15.plot(acc[Ns[14]].acciones_mean)
        ax15.grid()
        ax15.plot(n_hora, acc[Ns[14]].acciones[n_hora], 'o')
        largo_dia = len(acc[Ns[14]].acciones)
        ax15.plot(largo_dia, acc[Ns[14]].acciones[-1], b'o')
        ax15.text(n_hora, acc[Ns[14]].acciones[n_hora], acc[Ns[14]].acciones[n_hora], fontsize=11)
        ax15.text(largo_dia, acc[Ns[14]].acciones[-1], acc[Ns[14]].acciones[-1], fontsize=11)
    
        mes, dia, ano = acc[Ns[14]].date.split('/')
        fecha = date(int(ano), int(mes), int(dia))
        gap = acc[Ns[14]].acciones[0] - acc[Ns[14]-1].acciones[-1]
        gap_p = 100*(acc[Ns[14]].acciones[0] - acc[Ns[14]-1].acciones[-1])/acc[Ns[14]-1].acciones[-1]
        
        ax15.set_title('%s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[14], acc[Ns[14]].fitness, gap, gap_p) )
        print 'Fecha : %s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[14], acc[Ns[14]].fitness, gap, gap_p)
        ax15.yaxis.set_major_formatter(yFormatter)
          
    if cant_dias_eval > 16:    
        ax16.plot(acc[Ns[15]].acciones)
        ax16.plot(acc[Ns[15]].acciones_mean)
        ax16.grid()
        ax16.plot(n_hora, acc[Ns[15]].acciones[n_hora], 'o')
        largo_dia = len(acc[Ns[15]].acciones)
        ax16.plot(largo_dia, acc[Ns[15]].acciones[-1], b'o')
        ax16.text(n_hora, acc[Ns[15]].acciones[n_hora], acc[Ns[15]].acciones[n_hora], fontsize=11)
        ax16.text(largo_dia, acc[Ns[15]].acciones[-1], acc[Ns[15]].acciones[-1], fontsize=11)
        
        mes, dia, ano = acc[Ns[15]].date.split('/')
        fecha = date(int(ano), int(mes), int(dia))
        gap = acc[Ns[15]].acciones[0] - acc[Ns[15]-1].acciones[-1]
        gap_p = 100*(acc[Ns[15]].acciones[0] - acc[Ns[15]-1].acciones[-1])/acc[Ns[15]-1].acciones[-1]
        
        ax16.set_title('%s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[15], acc[Ns[15]].fitness, gap, gap_p) )
        print 'Fecha : %s, Simil : %.2f, Fit : %.2f, GAP : %.2f (%.1f%%)' % (fecha.strftime("%A %d, %B %Y"), fit_sim[15], acc[Ns[15]].fitness, gap, gap_p)
        ax16.yaxis.set_major_formatter(yFormatter)

    plt.show() 
    #plt.ioff()
    return


def similitud(N, NDatos, Datos, porcentaje = 0.0):
    Ns = []
    largo = len(NDatos)
    ECM = []
    gap_max = 0.001
    ecm_max = 0.001
    ecm_aux = []
    Gap = []
    porcentaje = porcentaje/100.
    fecha_index = -1
    for i in range(0, len(NDatos)):
        if NDatos[i].date == Datos.date:
            fecha_index = i-1
            break
    gap_hoy = NDatos[fecha_index].acciones[-1] - Datos.acciones[0]
    for i in range(1, largo):
        ecm_sum = 0
        if gap_max < abs(NDatos[i-1].acciones[-1] - NDatos[i].acciones[0]):
            gap_max = abs(NDatos[i-1].acciones[-1] - NDatos[i].acciones[0])
        for j in range(1, len(Datos.datos_filtrados)):
            ecm_sum += abs(Datos.datos_filtrados[j]-NDatos[i].datos_filtrados[j])
        ecm_aux.append(ecm_sum)    
    ecm_max = max(ecm_aux)         
       
    for i in range(0, largo):
        #Se n las funciones y se guardan en ECM
        if i == 0:
            gap_gen = 0
        else:
            gap_gen = NDatos[i-1].acciones[-1] - NDatos[i].acciones[0]
        ECM.append([compara(Datos, NDatos[i], N, gap_gen, gap_hoy, porcentaje, gap_max, ecm_max),i])  
    
    #max_ecm = max(ECM)

    #for i in range(0, largo):
        #Se n las funciones y se guardan en ECM
    #    ECM[i][0] = ECM[i][0]/float(max_ecm[0]) 
        
    #Se ordenan de acuerdo al primer valor
    ECM = sorted(ECM,key=itemgetter(0))

    resultado = []
    similitud = []
    k=0
    for i in ECM:
        resultado.append(NDatos[i[1]])
        similitud.append(i[0])
        Ns.append(i[1])
        k += 1
        if k >= N:
            break
    posiciones = Ns
    #print similitud
    #Se devuelven los N primeros datos
    return resultado, similitud, posiciones

#Funcion que  datos1 con datos2, se mueve a traves de las horas de datos1
def compara(datos1, datos2, N = -1, gap_gen  = 0, gap_hoy = 0, porcentaje = 0.0, gap_max = 0.001, ecm_max = 0.001):
    ECM = 0
    ECM_comp = 0       
    for i in range(0, len(datos1.datos_filtrados)):
        ECM_comp += abs(datos1.datos_filtrados[i]-datos2.datos_filtrados[i])
    
    ECM = (1-porcentaje)*ECM_comp/ecm_max + (porcentaje)*abs(gap_hoy-gap_gen)/gap_max 
    return ECM



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyWindow()
    sys.exit(app.exec_())

