import math
import os.path
import sys

import matplotlib
import numpy
from matplotlib import pyplot as plt, animation as ani

# Konstanten
# Anteil an min(x-Ausschnitt, y-Ausschnitt), um den Fahrzeuge auf ihrer Fahrspur von der Fahrbahnmitte verschoben werden
REL_LANE_OFFSET = 0.03
# Wartezeit zwischen den Zeitschritten beim Plot (je kleiner, desto schneller geht's)
PLOT_INTERVALL = 100
FILENAME_LINES = "Plan.txt"
FILENAME_VEH = "Fahrzeuge.txt"
START_STR_NEW_ITERATION = "*** t = "

# Ins Verzeichnis des Testfalls wechseln und ggf. plots-Verzeichnis erzeugen
if len(sys.argv) != 2:
    print('Dieses Skript erwartet mit dem absoluten Verzeichnisnamen des Testfalls genau einen Parameter.')
    exit(1)
os.chdir(sys.argv[1])
os.makedirs('plots', exist_ok=True)

# Linien einlesen
line_coords = []
min_x = 0.0
max_x = 0.0
min_y = 0.0
max_y = 0.0
filename = FILENAME_LINES
i = 0
veh_data = []  # x, y, naechste_kreuzung.x, naechste_kreuzung.y, id
t_list = []
try:
    with open(filename, mode='r') as file:
        line_nr = 0
        for line_plots in file:
            line_nr += 1
            line_plots = line_plots.strip()
            com_pos = line_plots.find('#')
            if com_pos != -1:
                line_plots = line_plots[0:com_pos]
            parts = line_plots.split()
            if len(parts) != 4:
                raise Exception()
            f_parts = [float(z) for z in parts]
            line_coords.append(f_parts)
            min_x = min(min_x, line_coords[-1][0], line_coords[-1][2])
            max_x = max(max_x, line_coords[-1][0], line_coords[-1][2])
            min_y = min(min_y, line_coords[-1][1], line_coords[-1][3])
            max_y = max(max_y, line_coords[-1][1], line_coords[-1][3])

    # Fahrzeuge einlesen
    filename = FILENAME_VEH
    with open(filename, mode='r') as file:
        line_nr = 0
        for line_plots in file:
            line_nr += 1
            line_plots = line_plots.strip()
            if line_plots == '':
                continue
            # Kommentare streichen
            com_pos = line_plots.find('#')
            if com_pos != -1:
                line_plots = line_plots[0:com_pos]
            # Nächster Interationsschritt ab "*** t = "
            new_t_pos = line_plots.find(START_STR_NEW_ITERATION)
            if new_t_pos != -1:
                t_list.append(int(line_plots[new_t_pos + len(START_STR_NEW_ITERATION):]))
                veh_data.append([])
                continue
            parts = line_plots.split()
            if len(parts) != 5:
                raise Exception()
            f_parts = [float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]), int(parts[4])]
            veh_data[-1].append(f_parts)
        i += 1
except (ValueError, IndexError, Exception) as E:
    print('Fehler in ' + filename + ' in Zeile ' + str(line_nr))
    exit(1)

fig = plt.figure()
plt.axis('square')
colors = list(matplotlib.colors.TABLEAU_COLORS.values())

# plot lines
line_plots = [plt.plot(line_coords[j][0::2], line_coords[j][1::2], 'b-')[0] for j in range(len(line_coords))]
plt.xlim(min_x - 1, max_x + 1)
plt.ylim(min_y - 1, max_y + 1)
time_label = plt.title('', )

circ_plots = plt.scatter([], [], marker='o')
max_num = -1


def update_plot(num):
    global max_num
    veh_count = len(veh_data[num])
    xy = []
    color_per_index = []
    for j in range(veh_count):
        x = veh_data[num][j][0]
        y = veh_data[num][j][1]
        # Vektor für Fahrspurverschiebung berechnen
        v_x = veh_data[num][j][3] - y
        v_y = x - veh_data[num][j][2]
        scaling_factor = REL_LANE_OFFSET * min(max_x - min_x, max_y - min_y) / math.sqrt(v_x ** 2 + v_y ** 2)
        v_x *= scaling_factor
        v_y *= scaling_factor
        xy.append([x + v_x, y + v_y])
        color_per_index.append(colors[veh_data[num][j][4] % len(colors)])
    time_label.set_text('t = ' + str(t_list[num]))
    if veh_count > 0:
        circ_plots.set_offsets(xy)
        circ_plots.set_color(color_per_index)
    else:
        # eine leere Liste kann man nicht uebergeben
        circ_plots.set_offsets(numpy.empty((1, 2)))
    # Aktuellen Stand in Datei speichern (aber nur ein Durchlauf)
    if num > max_num:
        plt.savefig(('plots/t{:0' + str(len(str(len(veh_data)))) + 'd}.png').format(t_list[num]))
        max_num = num


line_ani = ani.FuncAnimation(fig, update_plot, len(veh_data), interval=PLOT_INTERVALL, blit=False)
plt.show()
