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
import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
# If using PyCaret:
# from pycaret.regression import *
# Example: Linear Regression
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Data Preview:")
    st.dataframe(df.head())

    features = st.multiselect("Select Features:", df.columns)
    target = st.selectbox("Select Target Variable:", df.columns)

    if features and target:
        X = df[features]
        y = df[target]
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        model = LinearRegression()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)

        st.write("Model Evaluation:")
        st.write(f"Mean Squared Error: {mse:.2f}")
        st.write(f"R-squared: {r2:.2f}")

        # Visualization (example)
        st.scatter_chart(pd.DataFrame({'Actual': y_test, 'Predicted': y_pred}))
