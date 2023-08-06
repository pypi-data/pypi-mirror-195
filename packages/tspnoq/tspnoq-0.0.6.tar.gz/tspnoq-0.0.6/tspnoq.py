# this "Solving TSP with Integer Linear Program" python snippet was sourced by the site of Sandipanweb:
# https://sandipanweb.wordpress.com/2020/12/08/travelling-salesman-problem-tsp-with-python/

from mip import Model, xsum, minimize, BINARY
from itertools import product
import time

import xml.etree.ElementTree as ET
import re
import geopy.distance
import matplotlib.pyplot as plt
import itertools
import networkx as nx
import sys
    
def TSP_ILP(G):
    
    start = time.time()
    V1 =  range(len(G))
    n, V = len(G), set(V1)
    model = Model()
    # binary variables indicating if arc (i,j) is used 
    # on the route or not
    x = [[model.add_var(var_type=BINARY)
    for j in V] for i in V] 
    # continuous variable to prevent subtours: each city will have a
    # different sequential id in the planned route except the 1st one
    y = [model.add_var() for i in V]   # objective function: minimize the distance
    model.objective = minimize(xsum(G[i][j]*x[i][j] \
    for i in V for j in V))
    
    # constraint : leave each city only once
    for i in V:
        model += xsum(x[i][j] for j in V - {i}) == 1   # constraint : enter each city only once
    for i in V:
        model += xsum(x[j][i] for j in V - {i}) == 1   # subtour elimination
    for (i, j) in product(V - {0}, V - {0}):
        if i != j:
            model += y[i] - (n+1)*x[i][j] >= y[j]-n   # optimizing
    model.optimize()   # checking if a solution was found
    if model.num_solutions:
        print('Total distance {}'.format(model.objective_value))
        nc = 0 # cycle starts from vertex 0
        cycle = [nc]
    while True:
        nc = [i for i in V if x[nc][i].x >= 0.99][0]
        cycle.append(nc)
        if nc == 0:
            break
     
    return (model.objective_value, cycle)
    
# input file parcing
while True:
    try:
        fileinput = input('Type the full .csv or .kml input file:  ')
        
        if re.match(r".+\.kml", fileinput) is not None:
            # KML parse
            tree = ET.parse(fileinput)
            root = tree.getroot()
             # Identify default namespace
            namespace = re.match('\{(.*?)\}kml', root.tag).group(1)
            ns = {'def': namespace}
    
              # Define coordinates RegEx
            coord_ex = '(-?\d+\.\d+),'
            heig_ex = '(\d+)'
            regex = coord_ex + coord_ex + heig_ex
      
            coord_tab = []
            nod_name = []
            # Find coordinates
            for i in root.findall('.//def:Placemark', ns):
                name = i.find('def:name', ns).text
                coord = i.find('.//def:coordinates', ns)
                nod_name.append(name)
                # Check for placeless placemark     
                if not coord is None:
                    coord = coord.text.strip()
                    coord = re.findall(regex, coord)
                # Save data
                    for (long, lat, heig) in coord:      
                        if i.find('.//def:Point', ns):
                            coord_tab.append((float(lat), float(long)))
                            
                        
        elif re.match(r".+\.csv", fileinput) is not None:
            coord_tab= []
            nod_name = []
            nod_height = []
            file1 = open(fileinput, 'r')
            Lines = file1.readlines()
            i = 0

            for line in Lines:
                
                slist=line.split(';')
                coord_tab.append((float(slist[0]), float(slist[1])))
                nod_height.append((int(slist[2])))
                nod_name.append(i)
                i+=1
        
        else:
            raise FileNotFoundError
        
    except FileNotFoundError:
        print('something went wrong! Try again.')
    else:
        break

                
# create coordinates dictionary
n = len(coord_tab)
dict_coord = {i: {} for i in range(n)}
for i, j in itertools.combinations(range(n), 2):
    x1, y1 = coord_tab[i]
    x2, y2 = coord_tab[j]
    weight = geopy.distance.geodesic(coord_tab[i], coord_tab[j]).m
    dict_coord[i][j] = round(weight, 2)
    dict_coord[j][i] = round(weight, 2)
    print ('Length of edge ', i,'-', j, ':', dict_coord[i][j])

# Define the list of vertices and edges for the graph
vertices = list(range(n))

edges_temp = []
edges = []
for i in range(n):
    for j in range(n):
        if i!=j:
            edges_temp.append((nod_name[i],nod_name[j]))
        else:
            continue

for i in edges_temp:
    i_r = i[::-1] # reverse the element

    # check that it doesn't appear in the list, reversed or not... 
    if i_r not in edges and i not in edges:
        edges.append(i)

# Define the positions for each vertex
pos_lalo= dict(map(lambda i,j : (i,j) , nod_name, coord_tab))

#invert long / lat to plot points correctly
pos = {city:(long, lat) for (city, (lat,long)) in pos_lalo.items()}
        
# Create a graph using NetworkX
G = nx.Graph()
G.add_nodes_from(nod_name)
G.add_edges_from(edges)


def visualize_graph(graph, coordinates):
    # Draw the graph using NetworkX
    nx.draw(graph, coordinates, with_labels=True, node_color='skyblue',alpha=0.6, node_size=400, edge_color='grey', width=0.6)

    # Show the plot
    plt.show()
    
# Visualize the graph
visualize_graph(G, pos)

def create_input_graph(n):
    G = [[0 for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            G[i][j] = round(geopy.distance.geodesic(coord_tab[i], coord_tab[j]).m,2)
            G[j][i] = G[i][j]
    return G

G = create_input_graph(n)

#create a variable to place the result suggested by TSP function
result = list(TSP_ILP(G))
xy = result.pop(1)

# print the result and export a .txt file
# with the coordinates of the tsp path
TSP_points = []

pas = list(pos_lalo.items())
for i in xy:
    TSP_points.append(coord_tab[i])
    print(pas[i]) 


print('\n The total distance is:', result, 'meters')

if re.match(r".+\.csv", fileinput) is not None:
    coord_x, coord_y = list(zip(*coord_tab)) #unzip coord_tab list
    TSP_comb = [(coord_x[i], coord_y[i], nod_height[i]) for i in xy] #make a list of tuples with xyz
    


# input the name of the text file to be exported
while True:
    try:
        
        filename = input("\nType the name of the .csv or .txt file to export coordinates:  ")
        
        if re.match(r".+\.csv", fileinput) is not None:
            with open (filename, 'x') as f:
                f.write( '\n'.join(';'.join(str(x) for x in tu) for tu in TSP_comb))
        else:
            with open (filename, 'x') as f:
                f.write( '\n'.join(','.join(str(x) for x in tu) for tu in TSP_points))
            
    except FileExistsError:
        print( "\n This name already exists! Type something different. \n")
        continue
    else:
        break
        
#generate a graph with the TSP solution
tsp_edges = []
i = 1
while i in range(len(xy)):
    tsp_edges.append((nod_name[xy[i]],nod_name[xy[i-1]]))
    i+=1

G = nx.Graph()
G.add_nodes_from(nod_name)
G.add_edges_from(tsp_edges)

def visualize_graph(dict_coord, pos):
    # Draw the graph using NetworkX
    nx.draw(dict_coord, pos, with_labels=True, node_color='skyblue',alpha=0.6, node_size=400, edge_color='lightgreen', width=5)

    # Show the plot
    plt.show()


visualize_graph(G, pos)

del sys.modules['tspnoq'] # clear module tspnoq


