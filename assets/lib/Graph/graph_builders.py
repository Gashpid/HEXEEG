import numpy as np

# Taken from https://matplotlib.org/3.5.0/tutorials/advanced/blitting.html#sphx-glr-tutorials-advanced-blitting-py
class BlitManager:
    def __init__(self, canvas, animated_artists=()):
        """
        Parameters
        ----------
        canvas : FigureCanvasAgg
            The canvas to work with, this only works for sub-classes of the Agg
            canvas which have the `~FigureCanvasAgg.copy_from_bbox` and
            `~FigureCanvasAgg.restore_region` methods.

        animated_artists : Iterable[Artist]
            List of the artists to manage
        """
        self.canvas = canvas
        self._bg = None
        self._artists = []

        for a in animated_artists:
            self.add_artist(a)
        # grab the background on every draw
        self.cid = canvas.mpl_connect("draw_event", self.on_draw)

    def on_draw(self, event):
        """Callback to register with 'draw_event'."""
        cv = self.canvas
        if event is not None:
            if event.canvas != cv:
                raise RuntimeError
        self._bg = cv.copy_from_bbox(cv.figure.bbox)
        self._draw_animated()

    def add_artist(self, art):
        """
        Add an artist to be managed.

        Parameters
        ----------
        art : Artist

            The artist to be added.  Will be set to 'animated' (just
            to be safe).  *art* must be in the figure associated with
            the canvas this class is managing.

        """
        if art.figure != self.canvas.figure:
            raise RuntimeError
        art.set_animated(True)
        self._artists.append(art)

    def _draw_animated(self):
        """Draw all of the animated artists."""
        fig = self.canvas.figure
        for a in self._artists:
            fig.draw_artist(a)

    def update(self):
        """Update the screen with animated artists."""
        cv = self.canvas
        fig = cv.figure
        # paranoia in case we missed the draw event,
        if self._bg is None:
            self.on_draw(None)
        else:
            # restore the background
            cv.restore_region(self._bg)
            # draw all of the animated artists
            self._draw_animated()
            # update the GUI state
            cv.blit(fig.bbox)
        # let the GUI event loop process anything it has to do
        cv.flush_events()


    
class Subplot_RT_grapher_single_dot():
    def __init__(self,canvas,ax,*args):
        self.x,self.ax = np.linspace(0, 10, int(1/(1/240))),ax; self.canvas,self.data = canvas,self.x*0
        self.y = np.linspace(0, 0, int(1/(1/240))); self.index = True
        """ *** """; (self.ln,) = self.ax.plot(self.x, self.y, 'm-', animated=True, linewidth=0.5)
        """ ************************************* """; self.bm = BlitManager(self.canvas, [self.ln])

    def add_point(self,point,*args):
        if self.index:self.data[2] = point;self.index = False
        """"""; self.data = np.append(self.data[1:], [point])
        """ ** """; miny,maxy = min(self.data),max(self.data)
        miny = miny+(miny*0.2)
        maxy = maxy+(maxy*0.2)
        
        if miny == 0: miny -= 0.00025
        if maxy == 0: maxy += 0.00025
        
        try: self.ax.set_ylim([miny+0.002,maxy+0.004])
        except: self.ax.set_ylim([miny+0.002,maxy+0.004])
        """"""; self.ln.set_ydata(self.data);self.bm.update()
        """ ******************** """; self.canvas.draw_idle()
        return self.data


class Subplot_RT_grapher_shot():
    def __init__(self,canvas,ax,*args):
        """""";self.x,self.canvas,self.ax = np.linspace(0, 1, int(1/(1/240))),canvas,ax
        (self.ln1,) = self.ax.plot(self.x, self.x*0, 'b-*', animated=True, linewidth=0.5)
        (self.ln2,) = self.ax.plot(self.x, self.x*0, 'r-*', animated=True, linewidth=0.5)
        """ ************************ """; self.bm = BlitManager(self.canvas, [self.ln1,self.ln2])

    def add_shot(self,t,p,m,tlim,*args):
        self.ln1.set_xdata(t);self.ln1.set_ydata(p)
        self.ln2.set_xdata(t);self.ln2.set_ydata(m)
        maxy = max([max(p),max(m)])
        self.ax.set_ylim([0,maxy])
        self.ax.set_xlim([0,tlim])
        self.bm.update(); self.canvas.draw_idle()

class Subplot_RT_grapher_PSDW():
    def __init__(self,canvas,ax,mode=False,*args):
        self.mode = mode
        if self.mode:
            """""";self.x,self.canvas,self.ax = ['Theta','Beta','Low_Beta','High_Beta'],canvas,ax
            self.ax.bar(self.x, [0,0,0,0],color=['#DD3511', '#4810A5','#8810A5','#A510A0'])
        else:
            """""";self.x,self.canvas,self.ax = np.linspace(0, 1, int(1/(1/240))),canvas,ax
            (self.ln0,) = self.ax.plot(self.x, self.x*0, '-', color='#DD3511', animated=True, linewidth=0.5)
            (self.ln1,) = self.ax.plot(self.x, self.x*0, '-', color='#4810A5', animated=True, linewidth=0.5)
            (self.ln2,) = self.ax.plot(self.x, self.x*0, '-', color='#8810A5', animated=True, linewidth=0.5)
            (self.ln3,) = self.ax.plot(self.x, self.x*0, '-', color='#A510A0', animated=True, linewidth=0.5)
            """ ************************ """; self.bm = BlitManager(self.canvas, [self.ln0,self.ln1,self.ln2,self.ln3])
            

    def add_shot(self,f1=None,p1=None,f2=None,p2=None,f3=None,p3=None,f4=None,p4=None,L=None,*args):
        if self.mode:
            self.ax.cla()
            self.ax.set_title('TBR INDEX', color='#FFC107',fontweight="bold", size=12)
            self.ax.bar(self.x,p1,color=['#DD3511', '#4810A5','#8810A5','#A510A0'],label=L[0])
            self.ax.bar(self.x,p1,color=['#DD3511', '#4810A5','#8810A5','#A510A0'],label=L[1])
            self.ax.bar(self.x,p1,color=['#DD3511', '#4810A5','#8810A5','#A510A0'],label=L[2])
            self.ax.legend()
            self.canvas.draw_idle()
        else:
            self.ln0.set_xdata(f1);self.ln0.set_ydata(p1)
            self.ln1.set_xdata(f2);self.ln1.set_ydata(p2)
            self.ln2.set_xdata(f3);self.ln2.set_ydata(p3)
            self.ln3.set_xdata(f4);self.ln3.set_ydata(p4)
            
            p = [p1,p2,p3,p4]
            
            maxy = [max(p[i]) for i in range(4)]
            maxy = max(maxy); self.ax.set_ylim([0,maxy])
            self.bm.update(); self.canvas.draw_idle()























        
        
    
