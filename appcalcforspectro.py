import streamlit as st

st.title("Calculator for Spectrofotometry UV-VIS and Atomic Absorbstion Spectrofotometry")

import streamlit as st
import pandas as pd
import numpy as np

df = pd.DataFrame(
    np.random.randn(10, 2), columns=("col %d" % i for i in range(2))
)

st.table(df)

import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(np.random.randn(20, 2), columns=["a", "b"])

st.scatter_chart(chart_data)
