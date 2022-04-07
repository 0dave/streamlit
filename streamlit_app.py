import streamlit as st
import pandas as pd
import numpy as np

# set your title
st.title('Uber pickups in NYC') 

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...') # notes when loading data
data = load_data(10000)
data_load_state.text("Done! (using st.cache)") # notes when data loaded

# show/hide raw data
if st.checkbox('Show raw data'): # use checkbox to show/hide data
    st.subheader('Raw data')
    st.write(data)

# chart 1: Histgram
st.subheader('Number of pickups by hour')
hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

# chart 2:area chart
st.subheader('Area of Number of pickups by hour')

chart_data = data[DATE_COLUMN].dt.hour.value_counts()

st.area_chart(chart_data)

st.subheader('Bar of Number of pickups by hour')
st.bar_chart(chart_data)

# chart 4:area chart
st.subheader('Bokeh of Number of pickups by hour')

chart_data = data[DATE_COLUMN].dt.hour.value_counts()

import streamlit as st
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from pandas import DataFrame

# Get counts of groups of 'class' and fill in 'year_month_id' column
df1 = DataFrame({'count': data.groupby(data[DATE_COLUMN].dt.hour).size()}).reset_index()

x = data[DATE_COLUMN].dt.hour
y = df1['count'].tolist()

df2 = {'x': x,'y': y}

# create a ColumnDataSource by passing the dict
sc = ColumnDataSource(df2)

p = figure(
     title='simple line example',
     x_axis_label='x',
     y_axis_label='y')

p.line(x='x', y='y', source=sc, legend_label='Trend', line_width=2)

st.bokeh_chart(p, use_container_width=True)


# chart 0: slider as filter for time (Some number in the range 0-23)
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
# chart 3: map displays
st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)







