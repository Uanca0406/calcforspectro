import streamlit as st

st.title("Calculator for Spectrofotometry UV-VIS and Atomic Absorbstion Spectrofotometry")

import streamlit as st
import pandas as pd
import numpy as np

df = pd.DataFrame(
    np.random.randn(10, 2), columns=("col %d" % i for i in range(2))
)

st.table(df)
