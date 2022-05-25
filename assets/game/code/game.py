from PIL import ImageTk, Image
import tkinter as tk
import time, sys

sys.path.append('assets/game')
sys.path.append('assets/game/assets/')
sys.path.append('assets/game/assets/media')

class mainGame(object):
    def __init__(self,*args):
        self.root = tk.Tk()
        self.root.resizable(0,0)
        self.root.title('Game GUI')
        self.root.geometry('700x500')
        self.root.config(bg='#07F0FF')
        self.root.tk.call('wm', 'iconphoto', self.root._w, tk.PhotoImage(file='assets/media/icon.png'))

        self.ground = ImageTk.PhotoImage(Image.open('assets/media/ground.png'))
        self.airplane = ImageTk.PhotoImage(Image.open('assets/media/airplane.png'))
        self.asteroid = ImageTk.PhotoImage(Image.open('assets/media/asteroid.png'))
        
        self.obj = tk.Label(image=self.airplane, bg='#07F0FF')
        self.obj.place(relx=0.30,rely=0.70)

        self.grd = tk.Label(image=self.ground, bg='#07F0FF')
        self.grd.place(relx=-0.1,rely=0.9)

        self.i = 0
        self.pos = [-0.1,-0.15,-0.2,-0.25]
        self.AL = 0

        f = open('assets/var/SA','r')
        self.SA_n = int(f.read())
        f.close()

        f = open('assets/temp/SA','w')
        f.write(''); f.close()

        self.SA_i = self.AL
        self.i_SA = 0

        self.hide = False

        self.t = time.time()
        self.tv = 0
        
        self.scoreP = 0
        self.scoreM = 0

        self.SP = 0
        self.SM = 0

        self.ast = tk.Label(image=self.asteroid, bg='#07F0FF')
        self.ast.place(relx=0.6,rely=0.72-(0.72)*self.SA_i,relwidth=0.12,relheight=0.2)

        self.root.after(1,self.groundLoop())
        self.root.mainloop()

    def groundLoop(self,*args):
        self.grd.place(relx=self.pos[self.i],rely=0.9)
        self.i += 1; self.alt()
        if self.i > 3: self.i = 0

        if self.i_SA == int((600)/self.SA_n) and self.hide == True:
            self.SA_i = self.AL
            self.ast.place(relx=0.6,rely=0.72-(0.72)*self.SA_i,relwidth=0.12,relheight=0.2)
            self.i_SA = 0; self.t = time.time()
            self.hide = False

        if ((0.70-(0.7)*self.AL)+0.02) < (0.72-(0.72)*self.SA_i) and self.hide == False:
            self.t = self.t-time.time()
            if self.t < 0: self.t = -self.t
            self.obj.config(bg='#07F0FF')
            self.ast.place(relx=0.6,rely=0.72-(0.72)*20,relwidth=0.12,relheight=0.2)
            self.hide = True; self.SP += 1
            self.scoreP = self.SP/self.SA_n
            self.saveScores()
            
        if ((0.70-(0.7)*self.AL)) > (0.7-(0.7)*self.SA_i) and self.hide == False:
            self.t = self.t-time.time()
            if self.t < 0: self.t = -self.t
            self.tv += self.t
            self.obj.config(bg='#FF0000')
            self.ast.place(relx=0.6,rely=0.72-(0.72)*20,relwidth=0.12,relheight=0.2)
            self.hide = True; self.SM += 1
            self.scoreM = self.SM/self.SA_n
            self.saveScores()
            
        self.root.after(100,self.groundLoop)

    def alt(self,*args):
        try:
            f = open('assets/temp/TRB', 'r')
            self.AL = f.read(); f.close()
            self.AL = float(self.AL)
        except: pass
        self.obj.place(relx=0.30,rely=0.70-(0.7)*self.AL)
        self.i_SA += 1

    def saveScores(self,*args):
        f = open('assets/temp/SA','a')
        self.tv += self.t
        f.write(str(self.tv)+','+str(self.t)+','+str(self.scoreP)+','+str(self.scoreM)+'\n')
        f.close()
        
if __name__=='__main__':
    mainGame()
