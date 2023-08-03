import streamlit as st
import pandas as pd
import plotly.express as px
#import seaborn as sns
#import matplotlib.pyplot as plt
import warnings
#import io
import math
#adding title
st.title("Dizzy Doughnut")

df = pd.read_csv("Fifa.csv")

st.write(df.head(2))