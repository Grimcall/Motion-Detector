from mo_detector_v1_4 import df
from bokeh.plotting import figure
from bokeh.io import output_file, show

#Decl. File, settings.
f = figure(x_axis_type = 'datetime', height = 100, width = 500, sizing_mode = "scale_width", time ="Event Times")

#Eliminating y axis.
f.yaxis.minor_tick_line_color = None
f.ygrid[0].ticker.desired_num_ticks = 1

#Create cuadrant where time events are painted.
quadrant = f.quad(left = df["Start"], right= df["End"], bottom = 0, top = 0, color = "red")

#Generate output, show to user.
output_file("Events_Recorded.html")
show(f)


