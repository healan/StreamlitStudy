import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

import matplotlib.pyplot as plt

st.write(1234, '3')

# ex1 df
data_frame = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40],
})

st.write('Below is a DataFrame:', data_frame,
         'Above is a dataframe.')  # multi argument


# ex2 chart with altair
df = pd.DataFrame(
    np.random.randn(200, 3),
    columns=['a', 'b', 'c'])

c = alt.Chart(df).mark_circle().encode(
    x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])

d = alt.Chart(df).mark_bar().encode(
    x='a', y='b', size='c', color='c', tooltip=['a', 'b', 'c'])
# The encode() method builds a key-value mapping between encoding channels (such as x, y, color, shape, size, etc.)

st.write(c)
st.write(d)


# ex3 chart with matplotlib
arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.write(fig)


st.sidebar.success("Here is my chart page.")
