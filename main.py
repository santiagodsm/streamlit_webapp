# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import streamlit as st
import pandas as pd
import numpy as np

# App title
st.title("🚀 Hello Streamlit!")

# Welcome message
st.write("This is your first Streamlit app. Let’s build something awesome together!")

# Text input
name = st.text_input("What's your name?")

# Greet user
if name:
    st.success(f"Nice to meet you, {name}!")

# Create random data
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["Metric A", "Metric B", "Metric C"]
)

# Show chart
st.line_chart(chart_data)