import pandas as pd
from pandas import DataFrame
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.palettes import Category20c
from bokeh.palettes import Spectral5
from bokeh.transform import factor_cmap
from bokeh.transform import cumsum
from math import pi

output_file('attack_types.html')

# attach the column names to the dataset
col_names = ["duration","protocol_type","service","flag","src_bytes",
    "dst_bytes","land","wrong_fragment","urgent","hot","num_failed_logins",
    "logged_in","num_compromised","root_shell","su_attempted","num_root",
    "num_file_creations","num_shells","num_access_files","num_outbound_cmds",
    "is_host_login","is_guest_login","count","srv_count","serror_rate",
    "srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
    "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count",
    "dst_host_same_srv_rate","dst_host_diff_srv_rate","dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate","dst_host_serror_rate","dst_host_srv_serror_rate",
    "dst_host_rerror_rate","dst_host_srv_rerror_rate","label"]

df = pd.read_csv('kddcup.data_10_percent.csv', header= None, names = col_names)
# print(df.label == 'normal')
# df.describe()
# df.columns.to_list()
print(df['label'].value_counts())

# """ back, land, teardrop, pod, imap, ftp_write, rootkit, buffer_overflow, guess_password, perl, loadmodule, phf,
#     multihop, spy, warezclient, warezmaster """

grouped = DataFrame({'count': df.groupby(["label"]).size()}).reset_index()

# Create new column to make plotting easier
#df2['class-date'] = df2['class'] + "-" + df2['year_month_id'].map(str)

# x and y axes
label = grouped['label'].tolist()
count = grouped['count'].tolist()

# Bokeh's mapping of column names and data lists
source = ColumnDataSource(data=dict(label=label, count=count, color=Spectral5))

# Bokeh's convenience function for creating a Figure object
p = figure(x_range=label, y_range=(0, 290000), plot_height=700, plot_width= 1500, title="Counts",
           toolbar_location=None, tools="")

# Render and show the vbar plot
p.vbar(x='label', top='count', width=0.9, color='color', source=source)
show(p)

# Pie Chart
#data = pd.Series(x).reset_index(name='value').rename(columns={'index':'country'})
grouped['angle'] = grouped['count']/grouped['count'].sum() * 2*pi
#grouped['color'] = Category20c[len(grouped)]

p1 = figure(plot_height=350, title="Pie Chart", toolbar_location=None,
           tools="hover", tooltips="@label: @count", x_range=(-0.5, 1.0))

p1.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend='country', source = source)

p1.axis.axis_label=None
p1.axis.visible=False
p1.grid.grid_line_color = None

#grouped = df['label'].value_counts()

# sample = df.sample(500)
# source = ColumnDataSource(sample)
show(p1)
