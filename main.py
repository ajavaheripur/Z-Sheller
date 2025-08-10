#-------------------------------------------------------------------------------
# Name:        Electron Configuration v2.0 (GUI based)
# Purpose:     Finds electron configuration of a chemical element and draws
#              the Bohr model of its atom.
#
# Author:      Arvin Javaheripur
#
# Created:     11/09/2023
# Copyright:   (c) 2023 Arvin Javaheripur
# License:     GNU Lesser General Public License v3.0
#-------------------------------------------------------------------------------


from time import sleep
import PySimpleGUI as sg
from math import sin, cos, pi
def electron_configuration(electron_num):
    filling_order = ["1s", "2s", "2p", "3s", "3p", "4s", "3d", "4p", "5s", "4d",
                    "5p", "6s", "4f", "5d", "6p", "7s", "5f", "6d", "7p", "8s"]
    configuration = []
    run = True
    i = 0
    remaining_electrons = electron_num
    while run:
        subshell = str(filling_order[i])[1]
        shell = str(filling_order[i])[0]
        if subshell == "s":
            orbital_capacity = 2
            orbital_fill = 2
            if shell < "6":
                if (remaining_electrons - 11 == 0 and filling_order[i+1][1] == "d") or (remaining_electrons - 6 == 0 and filling_order[i+1][1] == "d"):
                    orbital_fill = 1
            elif (remaining_electrons - 30 == 0 and filling_order[i+2][1] == "d") or (remaining_electrons - 20 == 0 and filling_order[i+2][1] == "d"):
                orbital_fill = 1
        elif subshell == "p":
            orbital_capacity = 6
        elif subshell == "d":
            orbital_capacity = 10
        elif subshell == "f":
            orbital_capacity = 14
        if subshell != "s":
            orbital_fill = orbital_capacity
        if remaining_electrons < orbital_capacity:
            orbital_fill = remaining_electrons
            run = False
        remaining_electrons -= orbital_fill
        if orbital_fill != 0:
            configuration.append(filling_order[i]+str(orbital_fill))
        i += 1
    for counter in range(0, len(configuration)):
        configuration[counter]=configuration[counter].replace("s", "a")
        configuration[counter]=configuration[counter].replace("p", "b")
        configuration[counter]=configuration[counter].replace("d", "c")
        configuration[counter]=configuration[counter].replace("f", "z")
    configuration.sort()
    for counter in range(0, len(configuration)):
        configuration[counter]=configuration[counter].replace("a", "s")
        configuration[counter]=configuration[counter].replace("b", "p")
        configuration[counter]=configuration[counter].replace("c", "d")
        configuration[counter]=configuration[counter].replace("z", "f")
    configuration_str = ""
    return configuration

def convert_superscript(number):
    return "¹²³⁴⁵⁶⁷⁸⁹⁰"["1234567890".find(str(number))]

def integer_test(string):
    for i in string:
        if not i in "1234567890":
            return False
    return True

def remove_letters(string):
    new_string = ""
    for i in string:
        if i in "1234567890":
            new_string += i
    return new_string

def draw_bohr_model():
    GRAPH_SIZE = (400, 400)
    configuration_str = "Electron Configuration:"
    layout = [
    [sg.Text("Atomic Number of Element:"),
    sg.Input("", size=(5,20), key="inp"),
    sg.Button("Show Electron Configuration", bind_return_key=True, key="start")],
    [sg.Text(configuration_str+"\n\n", font=("Helvetica", 14), key="config")],
    [sg.Graph(
    canvas_size=GRAPH_SIZE,
    graph_bottom_left=(0,0),
    graph_top_right=(GRAPH_SIZE[0]+150, GRAPH_SIZE[1]+150),
    enable_events=False,
    background_color="white",
    key="GRAPH",)]
    ]
    window = sg.Window("Bohr Model", layout, finalize=True)
    graph = window["GRAPH"]
    electrons = []

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        inp = layout[0][1].get()
        window["inp"].update(remove_letters(layout[0][1].get()))
        if inp == layout[0][1].get():
            entered_letter = False
        else:
            entered_letter = True
        inp = layout[0][1].get()
        if "start" in event and inp != "" and inp != "0":
            if not entered_letter:
                window["inp"].update("")
            if int(inp) < 119:
                configuration_str = "Electron Configuration: "
                graph.erase()
                configuration = electron_configuration(int(inp))
                nucleus = graph.draw_circle((275, 275), 30, fill_color="red")
                n = 4
                m = 2
                for i in configuration:
                    if len(i) == 4:
                        i = i[0:2]+convert_superscript(i[2])+convert_superscript(i[3])
                    else:
                        i = i[0:2]+convert_superscript(i[2])
                    if n%9 == 0:
                        configuration_str += "\n" + i + " "
                        m-=1
                    else:
                        configuration_str += i + " "
                    n += 1
                configuration_str += "\n"*m
                window["config"].update(configuration_str)
                electrons = []
                electrons_num = 0
                prev_shell = 1
                for i in configuration:
                    shell = int(i[0])
                    if shell != prev_shell:
                        angle_increment = pi*2/electrons_num
                        graph.draw_circle((275,275), (prev_shell+1)*30)
                        for j in range(0, electrons_num):
                            graph.draw_circle((cos(angle_increment*j-pi/2)*(prev_shell+1)*30+275, sin(angle_increment*j-pi/2)*(prev_shell+1)*30+275), 7, fill_color="blue")
                        prev_shell = shell
                        electrons_num = 0
                    electrons_num += int(i[2:])
                angle_increment = 2*pi/electrons_num
                graph.draw_circle((275,275), (prev_shell+1)*30)
                for j in range(0, electrons_num):
                    graph.draw_circle((cos(angle_increment*j-pi/2)*(prev_shell+1)*30+275, sin(angle_increment*j-pi/2)*(prev_shell+1)*30+275), 7, fill_color="blue")
            else:
                sg.popup("Invalid Element","Atomic number shoud be less than or equal to 118.")
                window["config"].update("Electron Configuration:\n\n")
                graph.erase()
        else:
            window["config"].update("Electron Configuration:\n\n")
            graph.erase()
    window.close()
draw_bohr_model()
