#!/usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import math

class asset_dia:
    
    #Inicia objeto
    #
    #acciones: datos paratrabajar
    #time: hora de los datos
    #DT: Delta de tiempo en minutos
    #HI: Hora inicio
    #HF: Hora final
    
    def __init__(self, acciones, time, DT=1, HI=900, HF = 1330, date = "01/01/1900"):
        self.acciones = []
        self.acciones_promedio = []
        self.datos_filtrados = []
        self.acciones_mean = []
        self.acciones_mean2 = []
        self.date = date[0]
        self.day = 0 #1 lunes, 2 martes, 3 miercoles, etc...
        #Desde aca se corrige el arreglo de acciones 
        #y se le agregan todas las horas desde el inicio
        #hasta el final con un delta de N minutos
        #
        #Los datos que no existen se corrigen y se transforman
        #al dato siguiente de manera que quitar los 0s
        if len(acciones) < 1:
            print 'dia malo'
            return
        
        tiempos = []
        delta_aux = HI%100
        HI = int(HI/100)
        HI = HI*100
        for i in range(0, 1740):
            hora = HI+delta_aux
            if hora%100 > 59:
                HI += 100
                delta_aux = 0
                hora = HI+delta_aux
                
            delta_aux += 1    
            if hora < 1000:
                string_tiempo = '0%i'%hora
            else:
                string_tiempo = '%i'%hora
            tiempos.append([i, string_tiempo])
            
            if hora == HF:
                break
            

        acciones_tem = []
        time_tem = []
        j = 0
        for i in tiempos:
            try:
                time.index(int(i[1]))
                acciones_tem.append(acciones[j])
                time_tem.append(i[1])
                j += 1
            except ValueError:
                acciones_tem.append(-1)
                time_tem.append(i[1])
                
        for i in range(1, len(acciones_tem)):
            if acciones_tem[i]==-1:
                acciones_tem[i] = acciones_tem[i-1]
        for i in range(0, len(acciones_tem)):
            i_n = len(acciones_tem) - i - 2
            if acciones_tem[i_n]==-1:
                acciones_tem[i_n] = acciones_tem[i_n+1]


        i = 0

        #if 0.7*len(acciones_tem) > len(acciones):
         #   i += 1
         #   return

        self.acciones = acciones_tem
        self.time = time_tem
        self.acciones_mean = EMA(self.acciones,5)
        self.acciones_mean2 = EMA(self.acciones,30)
        
    #Funcion que calcula el RSI para n
    def calculo_RSI_AVG(self, n):
        df = DF(self.acciones)
        self.datos_filtrados = relative_strength(df, n=14)        
        return

    #Funcion que calcula el RSI con el promedio para n datos
    def calculo_RSI(self, n):
        self.datos_filtrados = relative_strength(self.acciones, n)        
        return

    #Funcion que calcula el valor estocastico de promedio de la accion para una ventana de n
    def calculo_STO(self, n):
        self.datos_filtrados = STO(self.acciones, n)
        return

    #Funcion que calcula el valor estocastico de promedio de la accion para una ventana de n
    def calculo_RSI_EMA(self, n1, n2):
        self.datos_filtrados = EMA(self.acciones, n2)
        self.datos_filtrados = relative_strength(self.datos_filtrados, n1)
        return
    
    #Funcion que calcula el valor estocastico de promedio de la accion para una ventana de n
    def calculo_Normalizacion(self):
        df_calculado = DF(self.acciones)
        self.datos_filtrados = NORM(df_calculado)
        
        return
    
    #Funcion que calcula el valor estocastico de la accion para una ventana de n
    def calculo_STO_mean(self, n):
        df_calculado = DF(self.acciones)
        self.datos_filtrados = STO(df_calculado, n)
        return

    #Funcion que calcula el valor estocastico de la accion para una ventana de n
    def calculo_STO_EMA(self, n1, n2):
        
        df_calculado = EMA(self.acciones, n2)
        self.datos_filtrados = STO(df_calculado, n1)
        return
    
    def calculo_fitness(self, n_hora, stop_loss = 0, tipo = 'L'):
        largo = len(self.acciones)
        if stop_loss == 0:
            self.fitness = self.acciones[-1]-self.acciones[n_hora]
            return
        elif tipo == 'L':
            maximo = self.acciones[n_hora]
            pos = -1
            for i in range(n_hora, largo):
                if maximo < self.acciones[i]:
                    maximo = self.acciones[i]
                dd = (100*(maximo - self.acciones[i])/maximo)
                pos = i
                if dd > stop_loss:
                    self.drawdawn = drawdown_L(self.acciones[n_hora:pos])
                    self.fitness = self.acciones[pos]-self.acciones[n_hora]
                    #print 'sl: %.2f, %.2f, L'%(self.fitness,(maximo - self.acciones[i]))
                    return
        elif tipo == 'S':
            minimo = self.acciones[n_hora]
            pos = -1
            for i in range(n_hora, largo):
                if minimo > self.acciones[i]:
                    minimo = self.acciones[i]
                dd = (100*(self.acciones[i]-minimo)/minimo)
                pos = i
                if dd > stop_loss:
                    self.drawdawn = drawdown_S(self.acciones[n_hora:pos])
                    self.fitness = self.acciones[n_hora]-self.acciones[pos]
                    #print 'sl: %.2f, %.2f, S'%(self.fitness,(self.acciones[i]-minimo))
                    return 
        #print 'non stop loss'
        if tipo == 'L':
            self.drawdawn = drawdown_L(self.acciones[n_hora:pos])
            self.fitness = self.acciones[-1]-self.acciones[n_hora]
        else:
            self.drawdawn = drawdown_S(self.acciones[n_hora:pos])
            self.fitness = self.acciones[n_hora]-self.acciones[-1]
        return 

    def calculo_fitness_comp(self, n_hora,dia2, stop_loss = 0, tipo = 'L'):
        largo = len(self.acciones)
        conteo = 0
        if stop_loss == 0:
            self.fitness = self.acciones[-1]-self.acciones[n_hora]
            return
        elif tipo == 'L':
            maximo = self.acciones[n_hora]
            pos = -1
            for i in range(n_hora, largo):
                dato_dia2 = dia2.acciones_mean2[i]-dia2.acciones_mean[i]
                dato_self = self.acciones_mean2[i]-self.acciones_mean[i]
                if ((dato_dia2 < 0) & (dato_self > 0)) | ((dato_dia2 > 0) & (dato_self < 0)):
                    conteo += 1
                if maximo < self.acciones[i]:
                    maximo = self.acciones[i]
                dd = (100*(maximo - self.acciones[i])/maximo)
                pos = i
                if conteo > 5:
                    dd = 10000
                if dd > stop_loss:
                    self.drawdawn = drawdown_L(self.acciones[n_hora:pos])
                    self.fitness = self.acciones[pos]-self.acciones[n_hora]
                    #print 'sl: %.2f, %.2f, L'%(self.fitness,(maximo - self.acciones[i]))
                    return
        elif tipo == 'S':
            minimo = self.acciones[n_hora]
            pos = -1
            for i in range(n_hora, largo):
                dato_dia2 = self.acciones_mean2[i]-self.acciones_mean[i]
                dato_self = self.acciones_mean2[i]-self.acciones_mean[i]
                if ((dato_dia2 < 0) & (dato_self > 0)) | ((dato_dia2 > 0) & (dato_self < 0)):
                    conteo += 1

                if minimo > self.acciones[i]:
                    minimo = self.acciones[i]
                dd = (100*(self.acciones[i]-minimo)/minimo)
                pos = i
                if conteo > 5:
                    dd = 10000
                if dd > stop_loss:
                    self.drawdawn = drawdown_S(self.acciones[n_hora:pos])
                    self.fitness = self.acciones[n_hora]-self.acciones[pos]
                    #print 'sl: %.2f, %.2f, S'%(self.fitness,(self.acciones[i]-minimo))
                    return 
        #print 'non stop loss'
        if tipo == 'L':
            self.drawdawn = drawdown_L(self.acciones[n_hora:-1])
            self.fitness = self.acciones[-1]-self.acciones[n_hora]
        else:
            self.drawdawn = drawdown_S(self.acciones[n_hora:-1])
            self.fitness = self.acciones[n_hora]-self.acciones[-1]
        return 
    
    def calculo_DF(self):
        self.acciones_promedio = DF(self.acciones)
        
        return
 
#Funcion que calcula el Ema con n1 datos   
def EMA(acciones, n1):
    
    acciones_EMA = []
    alpha1 = 2.0/(n1+1.0)

    largo = len(acciones)
    acciones_EMA.append(acciones[0]) 
    
    for k in range(1, largo):
        acciones_EMA.append(alpha1*(acciones[k])+(1-alpha1)*(acciones_EMA[k-1]))
            
    return acciones_EMA

#Funcion que calcula el STO de una funcion con una ventana de n1 datos
def STO(acciones, n1):
    
    acciones_STO = []
    maxim = 0
    minim = 0
    for i in range(0, len(acciones)):
        if i < n1:
            maxim = max(acciones[0:(i+1)], key=float)
            minim = min(acciones[0:(i+1)], key=float)
            acciones_STO.append((acciones[i] - minim)/(maxim-minim+0.00001)*100)
        else:
            #Calculo del producto punto
            maxim = max(acciones[(i-n1):(i+1)], key=float)
            minim = min(acciones[(i-n1):(i+1)], key=float)
            acciones_STO.append((acciones[i] - minim)/(maxim-minim+0.00001)*100)

    return acciones_STO

#Funcion que calcula el Filtro digital de una funcion, con filtro = parametros del filtro
def DF(acciones, filtro = [0.2221803586398, 0.2150955813174, 0.1947576580403, 0.1640102584778, 0.1268737971429, 0.0879715408845, 0.0516931162201, 0.02146560853277, -0.000657819800706, -0.01412901919176, -0.01979299840545, -0.01949430025836, -0.01549572584747, -0.01447805575186]):
    #Da vuelta el filtro para calcular el producto punto
    filtro = filtro[::-1]
    largo_filtro = len(filtro)
    acciones_DF = []
    for i in range(0, len(acciones)):
        if i < largo_filtro:
            acciones_DF.append(acciones[i])
        else:
            #Calculo del producto punto
            acciones_DF.append(sum(p*q for p,q in zip(acciones[(i-largo_filtro+1):(i+1)],filtro)))

    return acciones_DF

#Se calcula la volatibilidad con n datos
def volatibilidad(self, n=10, C=13901):        
    largo_ts = len(self.acciones)
    resta_precios = []
    promedio = 0
    resta_precios.append(0)
    volatibilidad = []
    
    for i in range(1, largo_ts):
        resta_precios.append((math.log(self.acciones[i])-math.log(self.acciones[i-1]))*C)
    for i in range(0, n):
        volatibilidad.append(0)
    for i in range(n, largo_ts):
        for j in range(0, n):
            promedio += resta_precios[i-j]
        promedio = promedio/n
        if (promedio > 16) | (promedio < -16):
            print "volatibilidad muy alta, revisar..."
            print promedio
        volatibilidad.append(promedio)
        
    return volatibilidad

#Funcion que normaliza entre 0 y 100 los datos
def NORM(acciones):
    acciones_aux = []
    if len(acciones) == 0:
        return acciones    
    
    maximo = max(acciones)
    minimo = min(acciones)
    for i in range(0, len(acciones)):
        acciones_aux.append(100*(acciones[i]-minimo)/(maximo-minimo+0.000001))
    return acciones_aux
     
#Funcion que calcula el RSI           
def relative_strength(prices, n=14):
    """
    compute the n period relative strength indicator
    http://stockcharts.com/school/doku.php?id=chart_school:glossary_r#relativestrengthindex
    http://www.investopedia.com/terms/r/rsi.asp
    """

    deltas = np.diff(prices)
    seed = deltas[:n+1]
    up = seed[seed>=0].sum()/n
    down = -seed[seed<0].sum()/n+0.00000001
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:n] = 100. - 100./(1.+rs)

    for i in range(n, len(prices)):
        delta = deltas[i-1] # cause the diff is 1 shorter

        if delta>0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up*(n-1) + upval)/n
        down = (down*(n-1) + downval)/n

        rs = up/down
        rsi[i] = 100. - 100./(1.+rs)

    return rsi

#Calcula la estrategia optima para un maximo de n estrategias
def calc_estrategia(acciones, hora, n=10):
    estrategia = []
    
    if len(acciones) == 0:
        return estrategia    
    
    largo = len(acciones)
    
    desde = 0
    n2 = 1
    for i in range(1,n):
        
        acciones2 = acciones[desde:-1]
        maximo = max(acciones2)
        minimo = min(acciones2)
        
        index_max = acciones.index(maximo, desde)
        index_min = acciones.index(minimo, desde)
        
        maximo_index = max([index_max, index_min])
        
        if maximo_index > 0.85*largo:
            break
                                  
        if(index_max < index_min):
            estrategia.append([index_max, hora[index_max], acciones[index_max], 'S', n])
            estrategia.append([index_min, hora[index_min], acciones[index_min], 'C', n])
        elif(index_max > index_min):
            estrategia.append([index_min, hora[index_min], acciones[index_min], 'L', n])
            estrategia.append([index_max, hora[index_max], acciones[index_max], 'C', n])
        
        desde = maximo_index
        n2 += 1
    return estrategia

#Drawdown for Long position
def drawdown_L(prices):
    prevmaxi = 0
    prevmini = 0
    maxi = 0
    for i in range(len(prices))[1:]:
        if prices[i] >= prices[maxi]:
            maxi = i
        else:
            # You can only determine the largest drawdown on a downward price!
            if (prices[maxi] - prices[i]) > (prices[prevmaxi] - prices[prevmini]):
                prevmaxi = maxi
                prevmini = i
    return 100*(prices[prevmaxi]-prices[prevmini])/prices[maxi]

#Drawdown for Long position
def drawdown_S(prices):
    prevmaxi = 0
    prevmini = 0
    maxi = 0

    for i in range(len(prices))[1:]:
        if prices[i] <= prices[maxi]:
            maxi = i
        else:
            # You can only determine the largest drawdown on a downward price!
            if (prices[maxi] - prices[i]) < (prices[prevmaxi] - prices[prevmini]):
                prevmaxi = maxi
                prevmini = i
    return 100*(prices[prevmini]-prices[prevmaxi])/prices[prevmini]