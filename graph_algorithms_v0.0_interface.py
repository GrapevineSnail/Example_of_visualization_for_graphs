from tkinter import *
from tkinter import messagebox
import math
import networkx as nx
from networkx import *
import matplotlib.pyplot as plot

def matrix_to_string(Matrix):
    n = len(Matrix)
    m = len(Matrix[0])
    string = ""
    max_width = 3
    for i in range(n):
        for j in range(m):
            if(len(str(Matrix[i][j])) > max_width):
                max_width = len(str(Matrix[i][j]))
    for i in range(n):
        for j in range(m):
            string += "{:{fill}{align}{width}}".format(
                Matrix[i][j],fill = ' ', align='^', width=max_width+1)
        string += '\n'
    string = string[:-1]
    return string

def find_center_of_graph(Matrix_of_shortest_paths):
    n = len(Matrix_of_shortest_paths)
    eccentricities = [0 for j in range(n)]
    for j in range(n):
        for d in [Matrix_of_shortest_paths[i][j] for i in range(n)]:
            if(d > eccentricities[j]):
                eccentricities[j] = d
    min_eccentricity = math.inf
    for e in eccentricities:
        if(e < min_eccentricity):
            min_eccentricity = e
    center_nodes = []
    for j in range(n):
        if(min_eccentricity == eccentricities[j]):
            center_nodes.append(j)
    return center_nodes

def visualize_graph(Adjacency_matrix, center):
    plot.clf()
    n = len(Adjacency_matrix)
    graph = nx.DiGraph()
    for i in range(n):
        graph.add_node(i+1)
        for j in range(n):
            if(i!=j and Adjacency_matrix[i][j] != math.inf):
                graph.add_edge(i+1,j+1,weight = Adjacency_matrix[i][j])
    color_map = []
    center_names = [c+1 for c in center]
    for node in graph:
        if node in center_names:
            color_map.append('orange')
        else: color_map.append(button_background)
    position = nx.circular_layout(graph) #position = nx.planar_layout(graph)
    nx.draw_networkx(
        graph,
        pos=position,
        width=1,
        node_color=color_map,
        node_shape='h',
        node_size=1000,
        edgecolors="black",
        font_size=11,
        font_color='k',
        font_family='serif',
        with_labels=True)
    labels = nx.get_edge_attributes(graph, "weight")
    nx.draw_networkx_edge_labels(
        graph,
        pos=position,
        label_pos=0.2,
        font_size=9,
        edge_labels=labels)
    plot.show()
    
def FloydWarshall(Adjacency_matrix):
    n = len(Adjacency_matrix)
    A = [[Adjacency_matrix[i][j] for j in range(n)] for i in range(n)] 
    for k in range(n): #новая включаемая вершина
        for i in range(n):
            for j in range(n):
                if(A[i][k] < math.inf and A[k][j] < math.inf):
                    A[i][j] = min(A[i][j], A[i][k] + A[k][j])
    return A #матрица кратчайших путей

def read_matrix():
    global center, center_str
    center_str = ""
    n = len(entry2)
    adjacency_matrix = [ [math.inf for j in range(n)] for i in range(n)]
    number_of_elements = 0
    error_color = '#FFCCCC'
    def entry_ij_accepted(i,j):
        entry2[i][j].delete(0,last=END)
        entry2[i][j].insert(0, str(adjacency_matrix[i][j]))
        entry2[i][j].config(state = DISABLED, background='white')
    for i in range(n):
        for j in range(n):
            entry_str = entry2[i][j].get()
            if(entry_str == '' or entry_str == "inf"):
                if (i==j):
                    adjacency_matrix[i][j] = 0.0
                #длина пути из вершины в саму себя равна 0
                #(в противном случае это петля)
                entry_ij_accepted(i,j)
                number_of_elements+=1
            elif(entry_str.replace('.','',1).isdigit()):
                adjacency_matrix[i][j] = float(entry_str)
                if(i!=j or (i==j and adjacency_matrix[i][j]==0)):
                    entry_ij_accepted(i,j)
                    number_of_elements+=1
                else:
                    entry2[i][j].config(background=error_color)
            else:
                entry2[i][j].config(background=error_color)
    print(matrix_to_string(adjacency_matrix), end="\n\n")###
    if(number_of_elements == n*n):
        matrix_of_shortest_paths = FloydWarshall(adjacency_matrix)
        center = find_center_of_graph(matrix_of_shortest_paths)
        center_str = str([v+1 for v in center])
        print("Центр графа:", center_str, end="\n\n")###
        spinbox1.delete(0, END)
        label1.grid_forget()
        label2['text'] = "Центр графа:\n"+center_str
        label2.grid(
            **place_optsW,
            row = 0, column = 1,
            columnspan = 1)        
        label3['text'] = "Матрица кратчайших путей:\n"+\
                         matrix_to_string(matrix_of_shortest_paths)
        label3.grid(
            **place_optsNW,
            row = 1, column = 1,
            rowspan = 3)
        label3.update()
        visualize_graph(adjacency_matrix, center)
    else:
        messagebox.showinfo("", "Введите кооректные данные")

def activate_entry2():
    label1.grid(
        **place_optsW,
        row = 2, column = 0,
        columnspan = 1)
    label2.grid_forget()
    label3.grid_forget()
    spinbox1.delete(0, END)
    n = len(entry2)
    for i in range(n):
        for j in range(n):
            entry2[i][j].config(state = NORMAL)
            if(entry2[i][j].get() == "inf"):
                entry2[i][j].delete(0,last=END)

def enter_matrix(n):
    global entry2, matrix_fromfile
    label1.grid(
        **place_optsW,
        row = 2, column = 0,
        columnspan = 1)
    label2.grid_forget()
    label3.grid_forget()
    button_forfile['state'] = DISABLED
    button_forfile['background'] = '#D9D9D9'
    entry_forfile.config(state = DISABLED)
    button2['state'] = NORMAL
    button3['state'] = NORMAL
    button2['background'] = button_background
    button3['background'] = button_background
    ### задание управляющих элементов
    if 'entry2' in globals():
        for i in range(len(entry2)):
            for j in range(len(entry2)):
                entry2[i][j].grid_forget()
    entry2 = [[Entry(frame3, width=6, background='white')
               for j in range(n)]
              for i in range(n)]
    for i in range(n):
        entry2[i][i].delete(0,last=END)
        entry2[i][i].insert(0, '0.0')
    if 'matrix_fromfile' in globals() and len(matrix_fromfile) > 0:
        for i in range(n):
            for j in range(n):
                entry2[i][j].delete(0,last=END)
                entry2[i][j].insert(0, matrix_fromfile[i][j])
        matrix_fromfile = []
    ### размещение управляющих элементов
    for i in range(n):
        for j in range(n):
            entry2[i][j].grid(
                row = i, column = j,
                padx = 1, pady = 1)
    entry2[0][0].focus()
    
def read_number_of_nodes():
    n = spinbox1.get()
    if(n.isdigit() and n!='0'):
        n = int(n)
        spinbox1.delete(0, END)
        entry_width = 40*2
        entry_height = 21
        canvas1.config(scrollregion=(0, 0,
                                     2*w/3 + n*entry_width,
                                     2*h/3 + n*entry_height))
        frame0.config(width=2*w/3 + n*entry_width,
                      height=2*h/3 + n*entry_height)
        enter_matrix(n)
    else:
        messagebox.showinfo("", "Введите кооректные данные")
        window1.lift()

def enter_number_of_nodes():
    spinbox1.focus()
    button2['state'] = DISABLED
    button3['state'] = DISABLED
    button2['background'] = '#D9D9D9'
    button3['background'] = '#D9D9D9'
    
def read_file():
    global matrix_fromfile
    matrix_fromfile = []
    s = entry_forfile.get()
    try:    
        matrix_fromfile = []
        f = open(s,'r')  
        matrix_fromfile.append(list(map(str,f.readline().split())))
        n = len(matrix_fromfile[0])
        spinbox1.delete(0, END)
        for i in range(n-1):
            matrix_fromfile.append(list(map(str,f.readline().split())))
        f.close()
        if(len(matrix_fromfile[n-1]) != len(matrix_fromfile)):
            matrix_fromfile = []
            messagebox.showwarning("", "Файл некорректен")
        else:
            entry_forfile.config(state = DISABLED)
            button_forfile.config(state = DISABLED)
            enter_matrix(n)
    except:
        messagebox.showwarning("", "Файл не найден")

def init_and_place_control_elements():
    ### задание и первичное размещение управляющих элементов
    global place_optsNW, place_optsW,\
           frame1, frame2, frame3,\
           frame11, frame12,\
           entry_forfile,\
           button_forfile, button1, button2, button3, button4,\
           spinbox1,\
           label1, label2, label3,\
           scrollbar1, canvas1, frame0
    ### Для скорллинга
    # холст
    canvas1 = Canvas(window1,
                     background=window_background,
                     width=300, height=200,
                     scrollregion=(0, 0, 2*w/3, 2*h/3))
    # скроллбары
    scrollbarY1 = Scrollbar(window1, command=canvas1.yview,
                            orient=VERTICAL)
    scrollbarX1 = Scrollbar(window1, command=canvas1.xview,
                            orient=HORIZONTAL)
    canvas1.config(yscrollcommand=scrollbarY1.set,
                   xscrollcommand=scrollbarX1.set)
    scrollbarY1.pack(side=RIGHT, fill=Y)
    scrollbarX1.pack(side=BOTTOM, fill=X)
    canvas1.pack(side=LEFT, expand=YES, fill=BOTH)
    # главный фрейм
    frame0 = Frame(canvas1,
                   bd=0, background=window_background,
                   width=2*w/3, height=2*h/3)
    canvas1.create_window((0, 0), window=frame0, anchor=NW)
    ###
    frame_opts = {'master':frame0, 'background':window_background}
    button_opts = {'background':button_background,
                   'relief':RAISED,
                   'borderwidth':button_borderwidth,
                   'font':(font, font_size)}
    place_optsNW = {'sticky':NW, 'padx':2, 'pady':2}
    place_optsW = {'sticky':W, 'padx':2, 'pady':2}
    ###
    frame1 = Frame(**frame_opts)
    frame1.grid(
        **place_optsNW,
        row = 0, column = 0,
        rowspan = 1, columnspan = 1
        )
    frame2 = Frame(**frame_opts)
    frame2.grid(
        **place_optsNW,
        row = 1, column = 0,
        rowspan = 1, columnspan = 1
        )
    frame3 = Frame(**frame_opts)
    frame3.grid(
        **place_optsNW,
        row = 3, column = 0,
        rowspan = 3, columnspan = 1
        )
    frame11 = Frame(
        frame1,
        background=window_background)
    frame11.grid(
        **place_optsNW,
        row = 0, column = 0
        )
    frame12 = Frame(
        frame1,
        background=window_background)
    frame12.grid(
        **place_optsNW,
        row = 1, column = 0
        )
    entry_forfile = Entry(
        frame11,
        width=30)
    entry_forfile.grid(
        **place_optsW,
        row = 0, column = 1
        )
    button_forfile = Button(
        frame11,
        text = "Ввод матрицы из файла:",
        **button_opts,
        command=read_file)
    button_forfile.grid(
        **place_optsW,
        row = 0, column = 0
        )
    spinbox1 = Spinbox(
        frame12,
        from_=1,
        to=99,
        width=6)
    spinbox1.grid(
        **place_optsW,
        row = 0, column = 1
        )
    button1 = Button(
        frame12,
        text = "Ввод количества вершин графа:",
        **button_opts,
        command=read_number_of_nodes)
    button1.grid(
        **place_optsW,
        row = 0, column = 0
        )
    button2 = Button(
        frame2,
        text = "Ввод матрицы из ячеек",
        **button_opts,
        command=read_matrix)
    button2.grid(
        **place_optsW,
        row = 0, column = 0
        )
    button3 = Button(
        frame2,
        text = "Изменить матрицу",
        **button_opts,
        command=activate_entry2)
    button3.grid(
        **place_optsW,
        row = 0, column = 1
        )
    label1 = Label(
        **frame_opts,
        text="Введите матрицу смежности графа\nЕсли ребра нет, оставьте клетку пустой или введите inf",
        font=(font, font_size-2)
        )
    label2 = Label(
        **frame_opts,
        text="Центр графа:\n",
        font=(font, font_size)
        )
    label3 = Label(
        **frame_opts,
        text="Матрица кратчайших путей:\n",
        font=(font_mono, font_size)
        )

### характеристики управляющих элементов
window_background = 'antique white'
button_background = 'bisque'
button_borderwidth = 5
font = "Book Antiqua"
font_mono = 'Courier New'
font_size = 12
window1_exists = False
###
def if_close_window1():
    global window1_exists
    window1.destroy()
    window1_exists = False
def main():
    global window1, w, h, window_exists
    ### главное окно
    window1 = Tk()
    window1_exists = True
    w = 2*window1.winfo_screenwidth()//3
    h = window1.winfo_screenheight()//2
    window1.config(
        background=window_background,
        relief=SUNKEN,
        borderwidth=3)
    window1.geometry('{}x{}'.format(w, h))
    window1.title("Центр графа: количество вершин")
    window1.protocol("WM_DELETE_WINDOW", if_close_window1)
    ###
    init_and_place_control_elements()
    enter_number_of_nodes()
    window1.mainloop()
main()
