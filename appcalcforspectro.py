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
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("DATA PENGAMATAN PENETAPAN KROM HEKSAVALEN (Cr VI) DALAM SAMPEL KULIT")

# Section 1: Pembuatan Deret Standar Induk Cr VI 500 mg/L
st.header("Pembuatan Deret Standar Induk Cr VI 500 mg/L")
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    std_cr_vi = st.number_input("Conc std Cr VI (mg/L)", value=500.0)
with col2:
    bobot = st.number_input("Bobot K2Cr2O7 (mg)", value=0.1415)
with col3:
    vol_induk = st.number_input("Vtabu (mL)", value=100.0)
with col4:
    perhitungan = st.number_input("Perhitungan", value=144.1176741)
with col5:
    satuan = st.text_input("Satuan", value="mg")

# Section 2: Pembuatan Deret Standar Cr VI
st.header("Pembuatan Deret Standar Cr VI")
df_standar = pd.DataFrame({
    "Conc std Cr VI (mg/L)": [0.1, 0.2, 0.3, 0.4, 0.5],
    "Volume std induk (mL)": [1, 2, 3, 4, 5],
    "Vtabu (mL)": [50, 50, 50, 50, 50]
})
edited_df_standar = st.data_editor(df_standar, num_rows="dynamic")

# Section 3: Pembuatan dan Pengukuran Deret Standar
st.header("Pembuatan dan Pengukuran Deret Standar")
colA, colB = st.columns([2,3])

with colA:
    data_standar = {
        "Conc Deret std Cr": [0, 0.1, 0.2, 0.3, 0.4, 0.5],
        "Volume std induk (mL)": [0, 1, 2, 3, 4, 5],
        "Vtabu (mL)": [50, 50, 50, 50, 50, 50],
        "Abs": [-0.0002, 0.0197, 0.0476, 0.0866, 0.0875, 0.0913]
    }
    df_pengukuran = pd.DataFrame(data_standar)
    edited_df_pengukuran = st.data_editor(df_pengukuran, num_rows="dynamic")

    # Regression
    X = np.array(edited_df_pengukuran["Conc Deret std Cr"]).reshape(-1, 1)
    y = np.array(edited_df_pengukuran["Abs"])
    if len(X) > 1 and len(y) > 1:
        from sklearn.linear_model import LinearRegression
        model = LinearRegression()
        model.fit(X, y)
        y_pred = model.predict(X)
        slope = model.coef_[0]
        intercept = model.intercept_
        corr = np.corrcoef(np.squeeze(X), y)[0,1]
    else:
        slope = intercept = corr = 0

    st.write("Koefisien korelasi (r):", f"{corr:.4f}")
    st.write("Slope (b):", f"{slope:.6f}")
    st.write("Intercept (a):", f"{intercept:.6f}")

with colB:
    # Plot regression
    plt.figure(figsize=(5,4))
    plt.scatter(X, y, color='blue')
    if len(X) > 1:
        plt.plot(X, y_pred, color='red')
        plt.text(np.min(X), np.max(y), f"y = {slope:.4f}x + {intercept:.4f}", fontsize=10)
    plt.xlabel("Conc Deret std Cr (mg/L)")
    plt.ylabel("Abs")
    plt.title("Kurva Standar")
    st.pyplot(plt)

# Section 4: Sample Data Input
st.header("Sample Data Input")
df_sample = pd.DataFrame({
    "Kode sampel": ["presisi", "presisi"],
    "Ulangan": [1, 2],
    "Bobot sampel (g)": [0.5015, 0.5038],
    "Abs": [0.0725, 0.0751],
    "Conc Cr VI (mg/L)": [0.383836662, 0.1975302201],
    "Vtabu (ml)": [50, 50],
    "FP": [500, 500],
    "Kadar Cr VI (mg/kg)": [19005.88043, 13979.08686],
    "Rerata Kadar Cr VI (mg/kg)": [19442.53544, 19442.53544]
})
edited_df_sample = st.data_editor(df_sample, num_rows="dynamic")

# Section 5: Kontrol Presisi Sampel Kulit
st.header("KONTROL PRESISI SAMPEL KULIT")
df_kontrol_presisi = pd.DataFrame({
    "kadar Cr1 (mg/kg)": [19005.88043],
    "Rerata kadar Cr (mg/kg)": [19442.53544],
    "selisih kadar Cr (mg/kg)": [873.1028397],
    "SKPPO": [4.496884007],
    "abs presisi": [0.0725]
})
edited_df_kontrol_presisi = st.data_editor(df_kontrol_presisi, num_rows="dynamic")

# Section 6: Kontrol Akurasi Sampel Kulit
st.header("Kontrol Akurasi Sampel Kulit")
df_kontrol_ak = pd.DataFrame({
    "Kode sampel": ["akurasi"],
    "C1/ Rerata kadar Cr VI (mg/L)": [0.3904],
    "Abs C3": [0.0599],
    "Conc C3 spike (mg/L)": [0.5116160497],
    "Conc C2 (mg/L)": [0.1],
    "% Rec": [121.2261697]
})
edited_df_kontrol_ak = st.data_editor(df_kontrol_ak, num_rows="dynamic")

st.markdown("---")
st.caption("Generated based on user spreadsheet structure ![image1](image1)")
