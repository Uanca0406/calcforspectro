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
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

st.title("Regression: Absorbant vs Concentration")

uploaded_file = st.file_uploader("Upload CSV with 'concentration' and 'absorbant' columns", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    if 'concentration' not in df.columns or 'absorbant' not in df.columns:
        st.error("Your CSV must contain 'concentration' and 'absorbant' columns.")
    else:
        st.write("Data Preview:")
        st.dataframe(df[['concentration', 'absorbant']])

        # Reshape and fit model
        X = df[['concentration']].values
        y = df['absorbant'].values
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)

        mse = mean_squared_error(y, y_pred)
        r2 = r2_score(y, y_pred)

        st.write("Model Evaluation:")
        st.write(f"Mean Squared Error: {mse:.2f}")
        st.write(f"R-squared: {r2:.2f}")
        st.write(f"Regression Equation: absorbant = {model.coef_[0]:.4f} * concentration + {model.intercept_:.4f}")

        # Show scatter plot with regression line
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.scatter(df['concentration'], df['absorbant'], color='blue', label='Data')
        ax.plot(df['concentration'], y_pred, color='red', label='Regression Line')
        ax.set_xlabel("Concentration")
        ax.set_ylabel("Absorbant")
        ax.legend()
        st.pyplot(fig)
else:
    st.info("Please upload a CSV file to begin.")
