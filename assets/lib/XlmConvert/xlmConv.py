from pandas import ExcelWriter
import pandas as pd
import subprocess
import sys

sys.path.append('assets/lib/XlmConvert')

class Xlsx():
    def __init__(self,*args):
        self.pathRaw = 'assets/temp/rawsignal/'
        self.pathSA = 'assets/temp/SA'
        self.pathTBR = 'assets/temp/TRBi'

    def launch(self,name,*args):
        #subprocess.Popen(self.pathRaw+name+'.xlsx')
        subprocess.Popen(self.pathTBR+'.xlsx')
        subprocess.Popen(self.pathSA+'.xlsx')

    def raw(self,name,*args): 
        f = open(self.pathRaw+name, "r")
        Data = []
        while(True):
            linea = f.readline()
            if linea != '':
                linea = linea.replace('\n','')
                Data.append(linea.split(','))
            if not linea:
                break
        f.close()

        Data1,Data2,Data3,Data4,Data5,Data6,Data7,Data8 = [],[],[],[],[],[],[],[]
        for D in Data:
            Data1.append(float(D[0]))
            Data2.append(float(D[1]))
            Data3.append(float(D[2]))
            Data4.append(float(D[3]))
            Data5.append(float(D[4]))
            Data6.append(float(D[5]))
            Data7.append(float(D[6]))
            Data8.append(float(D[7]))


        df = pd.DataFrame({'CHNN1':Data1,'CHNN2':Data2,'CHNN3':Data3,'CHNN4':Data4,
                           'CHNN5':Data5,'CHNN6':Data6,'CHNN7':Data7,'CHNN8':Data8})

        df = df[['CHNN1','CHNN2','CHNN3','CHNN4','CHNN5','CHNN6','CHNN7','CHNN8']]

        pathS = self.pathRaw+name+'.xlsx'
        
        writer = ExcelWriter(pathS)
        df.to_excel(writer, '', index=False)
        writer.save()

    def SA(self,*args): 
        f = open(self.pathSA, "r")
        Data = []
        while(True):
            linea = f.readline()
            if linea != '':
                linea = linea.replace('\n','')
                Data.append(linea.split(','))
            if not linea:
                break
        f.close()

        Data1,Data2,Data3,Data4 = [],[],[],[]
        for D in Data:
            Data1.append(float(D[0]))
            Data2.append(float(D[1]))
            Data3.append(float(D[2]))
            Data4.append(float(D[3]))


        df = pd.DataFrame({'Act time':Data1,'Ist time':Data2,'R hits':Data3,'R mistakes':Data4})

        df = df[['Act time','Ist time','R hits','R mistakes']]

        pathS = self.pathSA+'.xlsx'
        
        writer = ExcelWriter(pathS)
        df.to_excel(writer, '', index=False)
        writer.save()

    def TBR(self,*args): 
        f = open(self.pathTBR, "r")
        Data = []
        while(True):
            linea = f.readline()
            if linea != '':
                linea = linea.replace('\n','')
                Data.append(linea.split(','))
            if not linea:
                break
        f.close()

        Data1,Data2,Data3 = [],[],[]
        for D in Data:
            Data1.append(float(D[0]))
            Data2.append(float(D[1]))
            Data3.append(float(D[2]))


        df = pd.DataFrame({'TBR':Data1,'TBR_Low':Data2,'TBR_High':Data3})

        df = df[['TBR','TBR_Low','TBR_High']]

        pathS = self.pathTBR+'.xlsx'
        
        writer = ExcelWriter(pathS)
        df.to_excel(writer, '', index=False)
        writer.save()
