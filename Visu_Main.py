# -*- coding: utf-8 -*-
"""
Created on Friday Aug 17 10:24:55 2018

@author: M1822764 - Marion Purrio
Last modified: 2018-08-17


Marposs-Analysis and BCG-Visualisation on Marposs-Data. 

"""


#------------------------------------------------------------------------------
# HEADER ** HEADER ** HEADER ** HEADER ** HEADER ** HEADER ** HEADER ** HEADER
#------------------------------------------------------------------------------

from tkinter import *
from PIL import ImageTk, Image
from matplotlib.figure import Figure
import matplotlib.pyplot as plt 
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.transforms import Affine2D
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
import pandas as pd
import time

import saved_Variable

#------------------------------------------------------------------------------
# MAIN ** MAIN ** MAIN ** MAIN ** MAIN ** MAIN ** MAIN ** MAIN ** MAIN ** MAIN
#------------------------------------------------------------------------------


def Visu_Main(panePoints, numberOfPanes, numberOfData, actualizationTime, \
              upperLimitX, lowerLimitX, upperLimitY, lowerLimitY, upperLimitRot, lowerLimitRot):
    
    global runflag
    
    # Basic definition of GUI
    root = Tk()
    img_logo = Image.open("Sekurit_Vision4.0-Logo.PNG")
          # do widget photos objects from images  
    photo_logo = ImageTk.PhotoImage(img_logo) 
    
    screen_width = root.winfo_screenwidth()-100
    screen_height = root.winfo_screenheight()-100
    
    root.geometry("%dx%d+0+0" % (screen_width, screen_height))
    root.title("Saint-Gobain Sekurit Deutschland 2018")       # add a title here
    root.configure(background = "white")


    #graph, simple line plot
    GraphAxes, GraphAxes2, GraphAxes3, Graph, VizAxes, Viz = graph(root, panePoints, 0)
            
    #Title, logo, body(color), quit-Button
    wdgts(root, photo_logo, "3D Positioning & Trends", GraphAxes, GraphAxes2, GraphAxes3, \
          Graph, VizAxes, Viz, numberOfPanes, numberOfData, actualizationTime, \
          upperLimitX, lowerLimitX, upperLimitY, lowerLimitY, upperLimitRot, lowerLimitRot)


    # Start GUI execution
    root.mainloop()
        

#------------------------------------------------------------------------------
# HELPER ** HELPER ** HELPER ** HELPER ** HELPER ** HELPER ** HELPER ** HELPER
#------------------------------------------------------------------------------

#---------------------------------------------------------------------

#---------------------------------------------------------------------
def wdgts(root, photo_logo, mytitle, GraphAxes, GraphAxes2, GraphAxes3, \
          Graph, VizAxes, Viz, numberOfPanes, numberOfData, actualizationTime, \
          upperLimitX, lowerLimitX, upperLimitY, lowerLimitY, upperLimitRot, lowerLimitRot): 

    titleCanvas = Canvas(root)
    titleCanvas.configure(bg = "white", bd=0, highlightthickness=0, relief="ridge")
    titleCanvas.create_text(200, 50, text = mytitle, font = ('Helvetica', '22', 'bold'))
    titleCanvas.place (relx=0, rely=0, relwidth=1, relheight=.15)  
   
    logo = Label(root, image = photo_logo)
    logo.configure(bd=0, highlightthickness=0, relief="ridge")
    logo.place(relx=.99, rely=0, anchor="ne") # @error: "pyimage... doesn't exist" comment that line, compile, close TK Window, decomment

    buttonQuit = Button(root, text = 'quit', command = lambda: close_window(root))
    buttonQuit.configure(bg = "lavender", fg = "black") #, height = 2, width = 10 )
    buttonQuit.place(relx=.95, rely=.95, relwidth=.05, relheight=.05, anchor="c")
    
    buttonStart = Button(root, text = 'start', command = lambda: viz(root, panePoints, numberOfPanes, numberOfData, \
                                                                     actualizationTime, GraphAxes, GraphAxes2, GraphAxes3, \
                                                                     Graph, VizAxes, Viz, -1, upperLimitX, lowerLimitX, \
                                                                     upperLimitY, lowerLimitY, upperLimitRot, lowerLimitRot))
    buttonStart.configure(bg = "lavender", fg = "black") #, height = 2, width = 10 )
    buttonStart.place(relx=.05, rely=.95, relwidth=.05, relheight=.05, anchor="c")
    
    buttonPause = Button(root, text = 'interrupt', command = lambda: pause_exec(buttonPause))
    buttonPause.configure(bg = "lavender", fg = "black") #, height = 2, width = 10 )
    buttonPause.place(relx=.15, rely=.95, relwidth=.05, relheight=.05, anchor="c")

#---------------------------------------------------------------------

def graph(root, panePoints, i):
    
    bodyCanvas = Canvas(root)
    bodyCanvas.configure(bg ="#97c7f1")
    bodyCanvas.place(relx=0, rely=.15, relwidth=1, relheight=.85)
    
    GraphFigure = Figure() #figsize=(16,6)
    GraphFigure.patch.set_facecolor("#97c7f1")
    GraphAxes = GraphFigure.add_subplot(311)
    GraphAxes2 = GraphFigure.add_subplot(312)
    GraphAxes3 = GraphFigure.add_subplot(313)
    GraphFigure.subplots_adjust(hspace=0)

    GraphAxes.set_title("X-Shift, Y-Shift and Rotational Shift")
    #GraphAxes.set_xlabel("Date")
    #GraphAxes.set_ylabel("Shifts")   
    Graph = FigureCanvasTkAgg(GraphFigure, root)
    Graph.draw()
    Graph.get_tk_widget().place(relx=.01, rely=.9, relwidth=.4, relheight=.7, anchor = "sw")

    VizFigure = Figure()
    VizFigure.patch.set_facecolor("#97c7f1")
    VizAxes = VizFigure.add_subplot(111)
    VizAxes.set_title('Visualization')
    VizAxes.set_xlabel('horizontal shift')
    VizAxes.set_ylabel('vertical shift')
    
    VizAxes.set_xlim((-2,2))
    VizAxes.set_ylim((-2,2))
    
    VizAxes.plot([0, 0], [-2, 2], linewidth=1, linestyle=":", color="grey", alpha=.3)
    VizAxes.plot([-2, 2], [0, 0], linewidth=1, linestyle=":", color="grey", alpha=.3)
    
    Viz = FigureCanvasTkAgg(VizFigure, root)
    Viz.draw()
    Viz.get_tk_widget().place(relx=.51, rely=.9, relwidth=.4, relheight=.7, anchor = "sw")
    
    return GraphAxes, GraphAxes2, GraphAxes3, Graph, VizAxes, Viz

#--------------------------------------------------------------------- 

def viz(root, panePoints, m, n, time, GraphAxes, GraphAxes2, GraphAxes3, Graph, \
        VizAxes, Viz, j, upperLimitX, lowerLimitX, upperLimitY, lowerLimitY, upperLimitRot, lowerLimitRot): 
    # m is the number of panes that should be followed, 
    # n is the number of data in the graph
    # time is the actualization time

    
   if runflag == 1: 
             
        paneSize = [.5, .3]
        ts = VizAxes.transData
            
        if j < 190: 
            j = j+1
        else:
            j = 0
    
        #Data size. To be replaced by actual data
        
        # Glasspane part
        # -------------------------------------------------------------------
        
        VizAxes.cla()
        VizAxes.set_xlim((lowerLimitX*1.5, upperLimitX*1.5))
        VizAxes.set_ylim((lowerLimitY*1.5, upperLimitY*1.5)) 
        VizAxes.plot([lowerLimitX*1.5, upperLimitX*1.5], [0, 0], linewidth=1, linestyle=":", color="grey", alpha=.3)
        VizAxes.plot([0, 0], [lowerLimitY*1.5, upperLimitY*1.5], linewidth=1, linestyle=":", color="grey", alpha=.3)
        VizAxes.set_title('Visualization')
        VizAxes.set_xlabel('horizontal shift')
        VizAxes.set_ylabel('vertical shift')
        
        VizAxes.plot([lowerLimitX, upperLimitX], [upperLimitY, upperLimitY], linewidth=1, linestyle=":", color="red", alpha=.6)
        VizAxes.plot([lowerLimitX, upperLimitX], [lowerLimitY, lowerLimitY], linewidth=1, linestyle=":", color="red", alpha=.6)
        VizAxes.plot([upperLimitX, upperLimitX], [lowerLimitY, upperLimitY], linewidth=1, linestyle=":", color="red", alpha=.6)
        VizAxes.plot([lowerLimitX, lowerLimitX], [lowerLimitY, upperLimitY], linewidth=1, linestyle=":", color="red", alpha=.6)
        
        for k in range(min(j,m)):
            
           if (panePoints["centerX"][j-k] >= upperLimitX) or \
              (panePoints["centerX"][j-k] <= lowerLimitX) or \
              (panePoints["centerY"][j-k] >= upperLimitY) or \
              (panePoints["centerY"][j-k] <= lowerLimitY): 
                dotColor = "red"
           else: 
                dotColor = "blue"
            
           centerPoint = [panePoints["centerX"][j-k], panePoints["centerY"][j-k]]
           centerPane = plt.Circle((centerPoint[0], centerPoint[1]), .03, color=dotColor, alpha=(1-(k/m)))
           VizAxes.add_artist(centerPane)
           
        centerPoint = [panePoints["centerX"][j], panePoints["centerY"][j]]
        centerPane = plt.Circle((centerPoint[0], centerPoint[1]), .03, color="blue", alpha=1)
        VizAxes.add_artist(centerPane)
        
        rotationDegree = 180* panePoints["rotation"][j]
        lowerLeftCorner = [centerPoint[0]-(paneSize[0]/2), centerPoint[1]-(paneSize[1]/2)]
        tr = Affine2D().rotate_deg_around(centerPoint[0],centerPoint[1], rotationDegree)
           
        t = tr + ts    
    
        rec0 = FancyBboxPatch((lowerLeftCorner[0],lowerLeftCorner[1]),paneSize[0],paneSize[1], edgecolor="blue", facecolor="none", alpha=.5, linestyle=":")
        VizAxes.add_patch(rec0)
        #Rotated rectangle patch
        rect1 = FancyBboxPatch((lowerLeftCorner[0],lowerLeftCorner[1]),paneSize[0],paneSize[1], edgecolor="none", facecolor="#97c7f1" ,alpha=.5, transform=t)
        VizAxes.add_patch(rect1)
        
        Viz.draw()
        
        
        # Lineplot part
        # -------------------------------------------------------------------
        
        GraphAxes.cla()
        GraphAxes2.cla()
        GraphAxes3.cla()
        GraphAxes.set_title("X-Shift, Y-Shift and Rotational Shift")
        GraphAxes.set_ylim((lowerLimitX*1.5, upperLimitX*1.5))
        GraphAxes2.set_ylim((lowerLimitY*1.5, upperLimitY*1.5))
        GraphAxes3.set_ylim((lowerLimitRot*1.5, upperLimitRot*1.5))
        
        GraphAxes.set_ylabel("X Shift")
        GraphAxes2.set_ylabel("Y Shift")
        GraphAxes3.set_ylabel("Rotation")
        
        GraphAxes.yaxis.set_label_position("right")
        GraphAxes2.yaxis.set_label_position("right")
        GraphAxes3.yaxis.set_label_position("right")
        
        GraphAxes.tick_params(axis="x", which="both", bottom=False, top=False, labelbottom=False)
        GraphAxes2.tick_params(axis="x", which="both", bottom=False, top=False, labelbottom=False)
        
        GraphAxes.tick_params(axis="y", which="both", labelsize=8)
        GraphAxes2.tick_params(axis="y", which="both", labelsize=8)
        GraphAxes2.tick_params(axis="y", which="both", labelsize=8)
        
        
        k = min(j, n)
        
        GraphAxes.plot([j-k, j], [0, 0], linewidth=1, linestyle=":", color="grey", alpha=.6)
        GraphAxes2.plot([j-k, j], [0, 0], linewidth=1, linestyle=":", color="grey", alpha=.6)
        GraphAxes3.plot([j-k, j], [0, 0], linewidth=1, linestyle=":", color="grey", alpha=.6)
        
        GraphAxes.plot([j-k, j], [upperLimitX, upperLimitX], linewidth=1, linestyle=":", color="red", alpha=.6)
        GraphAxes2.plot([j-k, j], [upperLimitY, upperLimitY], linewidth=1, linestyle=":", color="red", alpha=.6)
        GraphAxes3.plot([j-k, j], [upperLimitRot, upperLimitRot], linewidth=1, linestyle=":", color="red", alpha=.6)
        
        GraphAxes.plot([j-k, j], [lowerLimitX, lowerLimitX], linewidth=1, linestyle=":", color="red", alpha=.6)
        GraphAxes2.plot([j-k, j], [lowerLimitY, lowerLimitY], linewidth=1, linestyle=":", color="red", alpha=.6)
        GraphAxes3.plot([j-k, j], [lowerLimitRot, lowerLimitRot], linewidth=1, linestyle=":", color="red", alpha=.6)
            
        GraphAxes.plot(range(j-k,j), panePoints["centerX"].values[j-k:j], linewidth=1, color="#44abaf", marker="o", markersize=3) # "range(j-k,j)" to be replaced with date/time
        GraphAxes2.plot(range(j-k,j), panePoints["centerY"].values[j-k:j], linewidth=1, color="#da96e8", marker="o", markersize=3)  # "range(j-k,j)" to be replaced with date/time
        GraphAxes3.plot(range(j-k,j), panePoints["rotation"].values[j-k:j], linewidth=1, color="#e4032f", marker="o", markersize=3)  # "range(j-k,j)" to be replaced with date/time
        Graph.draw()
        
        root.after(time, viz, root, panePoints, m, n, time, GraphAxes, \
                   GraphAxes2, GraphAxes3, Graph, VizAxes, Viz, j, \
                   upperLimitX, lowerLimitX, upperLimitY, lowerLimitY, upperLimitRot, lowerLimitRot)
    #        time.sleep(.5)

       
    
#--------------------------------------------------------------------   
def pause_exec(ButtonPause):
    global runflag
   
    if runflag == 1:
        runflag = 0
        ButtonPause.configure(bg = "red", fg = "black")
    else: 
        runflag = 1
        ButtonPause.configure(bg = "lavender", fg = "black")
    
#--------------------------------------------------------------------   

    
#--------------------------------------------------------------------   
def close_window(root):
    root.destroy()
#--------------------------------------------------------------------   

runflag = 1

panePoints = saved_Variable.doPanePoints()
numberOfPanes = 10
numberOfData = 50
actualizationTime = 500

upperLimitX = 1
lowerLimitX = -1
upperLimitY = 1
lowerLimitY = -1
upperLimitRot = 0.5
lowerLimitRot = -0.5


Visu_Main(panePoints, numberOfPanes, numberOfData, actualizationTime, \
          upperLimitX, lowerLimitX, upperLimitY, lowerLimitY, upperLimitRot, lowerLimitRot)





