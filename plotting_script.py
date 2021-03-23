from motion_detector import motion_df, face_df
from bokeh.plotting import show, figure, output_file
from bokeh.models import HoverTool, ColumnDataSource

motion_df['Start_Str'] = motion_df['Start'].dt.strftime('%Y-%m-%d %H:%M:%S')
motion_df['End_Str'] = motion_df['End'].dt.strftime('%Y-%m-%d %H:%M:%S')

face_df['Start_Str'] = face_df['Start'].dt.strftime('%Y-%m-%d %H:%M:%S')
face_df['End_Str'] = face_df['End'].dt.strftime('%Y-%m-%d %H:%M:%S')

cds = ColumnDataSource(motion_df)
cds_f = ColumnDataSource(face_df)

p = figure(x_axis_type="datetime", height=200, width=500, title="Motion Detection Times")
p.yaxis.minor_tick_line_color=None
p.ygrid[0].ticker.desired_num_ticks=1

hover_motion = HoverTool(tooltips=[("Start", "@Start_Str"), ("End", "@End_Str")])
p.add_tools(hover_motion)

hover_face = HoverTool(tooltips=[("Start", "@Start_Str"), ("End", "@End_Str")])
p.add_tools(hover_face)

q1 = p.quad(left='Start',right='End',bottom=0,top=1,color="yellow",source=cds)
q1 = p.quad(left='Start',right='End',bottom=0,top=1,color="green",source=cds_f)

output_file("graph.html")
show(p)
