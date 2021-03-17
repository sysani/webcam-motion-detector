from motion_detector import motion_df
from bokeh.plotting import show, figure, output_file

p = figure(x_axis_type="datetime", height=100, width=500, title="Motion Detection Times")
p.yaxis.minor_tick_line_color=None
p.ygrid[0].ticker.desired_num_ticks=1

q = p.quad(left=motion_df['Start'],right=motion_df['End'],bottom=0,top=1,color="green")

output_file("graph.html")
show(p)
