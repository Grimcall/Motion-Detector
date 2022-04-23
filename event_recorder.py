from mo_detector_v1_4_1b import df
from bokeh.plotting import figure
from bokeh.io import output_file, show
from bokeh.models import HoverTool, ColumnDataSource

#Alter end source.
df["Start_string"] = df["Start"].dt.strftime("%Y-%m-%d %H:%M:%S")
df["End_string"] = df["End"].dt.strftime("%Y-%m-%d %H:%M:%S")

csrc = ColumnDataSource(df)

#Decl. File, settings.
f = figure(x_axis_type = 'datetime', height = 100, width = 500, sizing_mode = "scale_width", time ="Event Times")

#Eliminating y axis.
f.yaxis.minor_tick_line_color = None
f.ygrid[0].ticker.desired_num_ticks = 1

#Hovertool Decl.
hover = HoverTool(tooltips=[("Start: ", "@Start_string"), ("End: ", "@End_string")])
f.add_tools(hover)

#Create cuadrant where time events are painted.
quadrant = f.quad(left = "Start", right= "End", bottom = 0, top = 1, color = "red")

#Generate output, show to user.
output_file("Events_Recorded.html")
show(f)


