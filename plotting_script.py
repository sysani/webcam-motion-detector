from motion_detector import motion_df, face_df
from bokeh.plotting import show, figure, output_file
from bokeh.models import HoverTool, ColumnDataSource

p = figure(x_axis_type="datetime", height=200, width=500, title="Motion Detection Times")
p.yaxis.minor_tick_line_color=None
p.ygrid[0].ticker.desired_num_ticks=1

if (len(motion_df) > 0):
    motion_df['Start_Str'] = motion_df['Start'].dt.strftime('%Y-%m-%d %H:%M:%S')
    motion_df['End_Str'] = motion_df['End'].dt.strftime('%Y-%m-%d %H:%M:%S')
    cds = ColumnDataSource(motion_df)
    q1 = p.quad(left='Start',right='End',bottom=0,top=1,color="yellow",source=cds)
    hover_motion = HoverTool(renderers=[q1], tooltips=[("Start", "@Start_Str"), ("End", "@End_Str")])
    p.add_tools(hover_motion)


if (len(face_df) > 0):
    cds_f = ColumnDataSource(data=dict(
    Start=face_df['Start'],
    End=face_df['End'],
    Start_Str=face_df['Start'].dt.strftime('%Y-%m-%d %H:%M:%S'),
    End_Str=face_df['End'].dt.strftime('%Y-%m-%d %H:%M:%S'),
    imgs= [
        './imgs/1592171906394.jpg'
    ]
    ))
    q2 = p.quad(left='Start',right='End',bottom=1,top=2,color="green",source=cds_f)
    hover_face = HoverTool(renderers=[q2], tooltips=[("Start", "@Start_Str"), ("End", "@End_Str"),
                                    ("Image", "<div><img src='@imgs', height=100, width=100></div>")])
    p.add_tools(hover_face)


output_file("graph.html")
show(p)
