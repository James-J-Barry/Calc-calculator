#Import modules.

# test test test

import math
import sympy
import PySimpleGUI as sg
import os.path
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Sets symbols for Sympy

x = sympy.Symbol("x")
y = sympy.Symbol("y")
expression = ("")

# Sets the manipulated elements to _VERS const.

_VARS = {'window': False,
         'fig_agg': False,
         'pltFig': False}

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# Sets up the empty figure for the graph to be drawn on.

w, h = figsize = (4, 3)
_VARS['pltFig'] = plt.figure(figsize=figsize)
dpi = _VARS['pltFig'].get_dpi()
size = (w*dpi, h*dpi)

# Creates the Layout with PySimpleGUI.

first_column = [
    [
        sg.Text("Equation/expression"),
        sg.In(default_text='(', size=(25, 1), enable_events=True, key="-EQUATION-"),
    ],
    [
        sg.HSeparator(),
    ],
    [
        sg.Button("Derivative"),
        sg.Button("Integral"),
        sg.Checkbox("Show original graph", False, key="-MAINCHECK-"),
    ],
    [
        sg.HSeparator(),
    ],
    [
        sg.Button("Definite Integral"),
        sg.Text("Bounds:  ["),
        sg.In(size=(2, 1), enable_events=True, key="-LOWERBOUND-"),
        sg.Text(", "),
        sg.In(size=(2, 1), enable_events=True, key="-UPPERBOUND-"),
        sg.Text("]"),
    ],
    [
        sg.HSeparator(),
    ],
    [
        sg.Text("Riemann Sums"),
    ],
    [
        sg.Text("Bounds:  ["),
        sg.In(size=(2, 1), enable_events=True, key="-RIELOWERBOUND-"),
        sg.Text(", "),
        sg.In(size=(2, 1), enable_events=True, key="-RIEUPPERBOUND-"),
        sg.Text("]"),
    ],
    [ 
        sg.Text("# of subintervals: "),
        sg.In(size=(3, 1), enable_events=True, key="-SUBINTERVALS-"),
    ],
    [ 
        sg.Button("Left"),
        sg.Button("Right"),
        sg.Button("Diagonal"),
    ],
]
second_column = [
    [sg.Text("Imput the Equation and press a button")],
    [sg.Text(size=(40, 1), key="-OUTPUT-")],
    [sg.Canvas(size=size, key='figCanvas')],
]
layout = [
    [
        sg.Column(first_column),
        sg.VSeperator(),
        sg.Column(second_column),
    ]
]

# Creates the window

_VARS['window'] = sg.Window("Jim's Calculus Calculator >:)", layout, finalize=True)

# Takes the function to be graphed and returns the x and y data for the figure to plot.

def makeData(function):
    xData = np.linspace(start=(-10), stop=(10), num=(100), dtype=float)
    yData = []
    for value in range(len(xData)):
        x = xData[value]
        yData.append(eval(function))
    return (xData, yData)

# Draws the initial graph

def drawChart(function, color):
    dataXY = makeData(function)
    plt.plot(dataXY[0], dataXY[1], color)
    _VARS['fig_agg']= draw_figure(
        _VARS['window']['figCanvas'].TKCanvas, _VARS['pltFig'])
    
# Draws the graph when the equasion is updated.

def updateChart(function, color):
    _VARS['fig_agg'].get_tk_widget().forget()
    dataXY = makeData(function)
    plt.clf()
    plt.plot(dataXY[0], dataXY[1], color)
    _VARS['fig_agg'] = draw_figure(
        _VARS['window']['figCanvas'].TKCanvas, _VARS['pltFig'])

#Draws the graph for the Derivative and Integral, including original function of not.

def updateChartEx(function, color, expre):
    _VARS['fig_agg'].get_tk_widget().forget()
    dataXY = makeData(function)
    plt.clf()
    dataAB = makeData(expre)
    plt.plot(dataAB[0], dataAB[1], '-g')
    plt.plot(dataXY[0], dataXY[1], color)
    _VARS['fig_agg'] = draw_figure(
        _VARS['window']['figCanvas'].TKCanvas, _VARS['pltFig'])

# Draws the initial graph that shows up when the program is opened
    
drawChart('x', '-k')

# Main loop, takes the imputs of the user and provides an output/graph

while True:
    event, values = _VARS['window'].read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "-EQUATION-":
        try:
            expression = values["-EQUATION-"].strip()
            updateChart(expression, '-g')
        except:
            pass

    elif event == "Derivative":
        try:
            x = sympy.Symbol("x")
            y = sympy.Symbol("y")
            de_dx = sympy.diff(expression, x)
            de_dx = str(de_dx)
            _VARS['window']["-OUTPUT-"].update(de_dx)
            if _VARS['window']["-MAINCHECK-"].get():
                updateChartEx(de_dx, '-r', expression)
            else:
                updateChart(de_dx, '-r')
        except:
            pass
        
    elif event == "Integral":
        try:
            x = sympy.Symbol("x")
            y = sympy.Symbol("y")
            inegex = sympy.integrate(expression, x)
            inegex = str(inegex)
            _VARS['window']["-OUTPUT-"].update(inegex)
            if _VARS['window']["-MAINCHECK-"].get():
                updateChartEx(inegex, '-b', expression)
            else:
                updateChart(inegex, '-b')
        except:
            pass
        
    elif event == "Definite Integral":
        try:
            lower = float(values["-LOWERBOUND-"].strip())
            upper = float(values["-UPPERBOUND-"].strip())
            defint = sympy.integrate(expression, (x, lower, upper))
            _VARS['window']["-OUTPUT-"].update(defint)
        except:
            pass
        
    elif event == "Left":
        try:
            lower = float(values["-RIELOWERBOUND-"].strip())
            upper = float(values["-RIEUPPERBOUND-"].strip())
            subint = float(values["-SUBINTERVALS-"].strip())
            changeX = ((upper - lower)/subint)
            theSum = 0
            while(lower < upper):
                x = lower
                theSum += changeX * eval(expression)
                lower += changeX
            _VARS['window']["-OUTPUT-"].update(theSum)
        except:
            pass
        
    elif event == "Right":
        try:
            lower = float(values["-RIELOWERBOUND-"].strip())
            upper = float(values["-RIEUPPERBOUND-"].strip())
            subint = float(values["-SUBINTERVALS-"].strip())
            changeX = ((upper - lower)/subint)
            theSum = 0
            lower += changeX
            while(lower <= upper):
                x = lower
                theSum += changeX * eval(expression)
                lower += changeX
            _VARS['window']["-OUTPUT-"].update(theSum)
        except:
            pass
        
    elif event == "Diagonal":
        try:
            lower = float(values["-RIELOWERBOUND-"].strip())
            upper = float(values["-RIEUPPERBOUND-"].strip())
            subint = float(values["-SUBINTERVALS-"].strip())
            changeX = ((upper - lower)/subint)
            theSum = 0
            preSum = 0
            while(lower <= upper):
                x = lower
                left = eval(expression)
                x = lower + changeX
                right = eval(expression)
                preSum += ((left + right)/2)
                lower += changeX
            theSum = preSum * changeX
            _VARS['window']["-OUTPUT-"].update(theSum)
        except:
            pass
        
_VARS['window'].close()
