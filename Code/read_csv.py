# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.
__author__="acannia"
__date__ ="$16-02-2014 02:27:11 AM$"

import csv

class read_csv:
    
    def __init__(self, archivo):
        
        self.data_open = []
        self.data_close = []
        self.data_high = []
        self.data_low = []
        self.data_date = []
        self.data_time = []
        self.max_hora = 0
        self.min_hora = 100000
        
        if archivo == 'aa':
            return
        with open(archivo, 'rb') as f:
            f_csv = csv.DictReader(f)
            data = []
            
            data_open_v = []
            data_close_v = []
            data_high_v = []
            data_low_v = []
            data_date_v = []
            data_time_v = []
            
            date = []
            
            j = 0
            i = 0
            
            for row in f_csv:
                [a,b1,c] = row["Date"].split('/')
                if j > 0:
                    if  b2 != b1:
                        self.data_open.append(data_open_v)
                        self.data_close.append(data_close_v)
                        self.data_high.append(data_high_v)
                        self.data_low.append(data_low_v)
                        self.data_date.append(data_date_v)
                        self.data_time.append(data_time_v)
                        
                        data_open_v = []
                        data_close_v = []
                        data_high_v = []
                        data_low_v = []
                        data_date_v = []
                        data_time_v = []
                
                        self.data = []
                        self.date = []
                        #print data_final[i]
                        i = i + 1
                        j = -1
                
                b2 = b1
                    
                data_open_v.append(float(row["Open"]))
                data_close_v.append(float(row["Close"]))
                data_high_v.append(float(row["High"]))
                data_low_v.append(float(row["Low"]))
                data_date_v.append(row["Date"])
                data_time_v.append(int(row["Time"]))
                maximo = int(max(data_time_v))
                minimo = int(min(data_time_v))
                if self.max_hora < maximo: 
                    self.max_hora = maximo
                if self.min_hora > minimo: 
                    self.min_hora = minimo
                    
                j+=1
                
            print "Lectura de datos finalizada..."
        
        maximo = int(max(data_time_v))
        minimo = int(min(data_time_v))
        if self.max_hora < maximo: 
            self.max_hora = maximo
        if self.min_hora > minimo: 
            self.min_hora = minimo
        self.data_open.append(data_open_v)
        self.data_close.append(data_close_v)
        self.data_high.append(data_high_v)
        self.data_low.append(data_low_v)
        self.data_date.append(data_date_v)
        self.data_time.append(data_time_v)

    
