import pandas as pd
from pandas import DataFrame
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.palettes import Category20c
from bokeh.palettes import Spectral5
from bokeh.palettes import magma
from bokeh.transform import factor_cmap
from bokeh.transform import cumsum
from math import pi
from pathlib import Path

mypath = Path().absolute()
filepath = (mypath / "kddcup.data_10_percent.csv")

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

df = pd.read_csv(filepath, header= None, names = col_names)
print(df['label'].value_counts())

# Get counts of groups of 'labels' and fill in 'count' column
grouped = DataFrame({'count': df.groupby(["label"]).size()}).reset_index()

 # creating a list of the count column
others = list(grouped['count'])

#     back, land, teardrop, pod, imap, ftp_write, rootkit, buffer_overflow, guess_password, perl, loadmodule, phf,
#     multihop, spy, warezclient, warezmaster are labels with count values less than 9000

# Appending all count values less than 9000 to a list
other_column = []
for other in others:
    if other < 9000:
        other_column.append(other)

# Adding all values less than 9000
Sum = sum(other_column)
len(other_column)

# Dropping all rows with count values less than 9000
grouped = grouped[grouped['count'] > 9000]

# Adding 'other' row to grouoed dataframe for sum of values 'other_column'
grouped = grouped.append({'label' : 'other', 'count' : Sum} ,  ignore_index = True)

# x and y axes
label = grouped['label'].tolist()
count = grouped['count'].tolist()

# Bokeh's mapping of column names and data lists
source = ColumnDataSource(data=dict(label=label, count=count, color=Spectral5))

# Bokeh's convenience function for creating a Figure object
p = figure(title = "Bar Chart of the class composition KDD99 Dataset", x_range=label, y_range=(0, 290000), plot_height=500, plot_width= 700,
           toolbar_location=None, tools="")

# Render and show the vbar plot
p.vbar(x='label', top='count', width=0.9, color='color', source=source)
show(p)
