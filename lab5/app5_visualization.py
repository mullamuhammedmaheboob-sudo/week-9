
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.title("Data Visualization")


df = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["Math", "Science", "English"]
)

st.subheader("Built-in Charts")
st.line_chart(df)
st.bar_chart(df)
st.area_chart(df)

st.subheader("Matplotlib Chart")
fig, ax = plt.subplots()
ax.hist(df["Math"], bins=10, color="skyblue")
ax.set_title("Math Score Distribution")
st.pyplot(fig)


fig = px.histogram(df, x="Math", nbins=10, title="Math Distribution")
st.plotly_chart(fig, use_container_width=True)


st.scatter_chart(df, x="Math", y="Science")


st.metric("Average Math Score", f"{df['Math'].mean():.2f}")
