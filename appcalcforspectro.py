import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO

# Set page config
st.set_page_config(page_title="Cr6+ Spectrophotometry Analysis", layout="wide")

# Title
st.title("Cr6+ Spectrophotometry Data Analysis")

# Sidebar for file upload
with st.sidebar:
    st.header("Upload Data")
    uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"])
    
    if uploaded_file:
        st.success("File uploaded successfully!")
    else:
        st.warning("Please upload an Excel file")
        st.stop()

# Function to load and process data
def load_data(file):
    try:
        # Read specific sheet
        df = pd.read_excel(file, sheet_name="Cr6+")
        
        # Extract standard curve data
        std_curve_df = df.iloc[15:21, [0, 3]].dropna()
        std_curve_df.columns = ['Concentration (mg/L)', 'Absorbance']
        
        # Extract sample data
        sample_df = df.iloc[27:29, [0, 2, 3, 7]].dropna()
        sample_df.columns = ['Replicate', 'Sample Weight (g)', 'Absorbance', 'Cr VI Content (mg/kg)']
        
        # Extract accuracy data
        accuracy_df = df.iloc[40:42, [2, 3, 5]].dropna()
        accuracy_df.columns = ['Absorbance', 'Calculated Conc (mg/L)', 'Spike Conc (mg/L)']
        
        # Get regression parameters
        r_value = df.iloc[21, 3]
        r_squared = df.iloc[21, 4]
        slope = df.iloc[22, 3]
        intercept = df.iloc[23, 3]
        
        return {
            'std_curve': std_curve_df,
            'samples': sample_df,
            'accuracy': accuracy_df,
            'regression': {
                'r': r_value,
                'r_squared': r_squared,
                'slope': slope,
                'intercept': intercept
            }
        }
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

# Load and process data
data = load_data(uploaded_file)

if data is None:
    st.stop()

# Display the data
tab1, tab2, tab3 = st.tabs(["Standard Curve", "Sample Analysis", "Accuracy Check"])

with tab1:
    st.header("Standard Curve Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Standard Curve Data")
        st.dataframe(data['std_curve'], hide_index=True)
        
        st.subheader("Regression Parameters")
        st.write(f"Correlation Coefficient (r): {data['regression']['r']:.4f}")
        st.write(f"R-squared: {data['regression']['r_squared']:.4f}")
        st.write(f"Slope: {data['regression']['slope']:.4f}")
        st.write(f"Intercept: {data['regression']['intercept']:.4f}")
    
    with col2:
        st.subheader("Standard Curve Plot")
        
        # Create plot
        fig, ax = plt.subplots()
        x = data['std_curve']['Concentration (mg/L)']
        y = data['std_curve']['Absorbance']
        
        ax.scatter(x, y, color='blue', label='Data points')
        
        # Plot regression line
        x_fit = np.linspace(0, max(x), 100)
        y_fit = data['regression']['slope'] * x_fit + data['regression']['intercept']
        ax.plot(x_fit, y_fit, 'r-', label='Regression line')
        
        ax.set_xlabel('Concentration (mg/L)')
        ax.set_ylabel('Absorbance')
        ax.set_title('Cr6+ Standard Curve')
        ax.legend()
        ax.grid(True)
        
        st.pyplot(fig)
        
        # Download plot
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=300)
        st.download_button(
            label="Download Plot",
            data=buf.getvalue(),
            file_name="standard_curve.png",
            mime="image/png"
        )

with tab2:
    st.header("Sample Analysis")
    
    st.subheader("Sample Data")
    st.dataframe(data['samples'], hide_index=True)
    
    # Calculate and display average
    avg_content = data['samples']['Cr VI Content (mg/kg)'].mean()
    st.subheader(f"Average Cr VI Content: {avg_content:.2f} mg/kg")
    
    # Calculate precision (RSD)
    std_dev = data['samples']['Cr VI Content (mg/kg)'].std()
    rsd = (std_dev / avg_content) * 100 if avg_content != 0 else 0
    st.subheader(f"Precision (RSD): {rsd:.2f}%")

with tab3:
    st.header("Accuracy Check (Spike Recovery)")
    
    st.subheader("Recovery Data")
    st.dataframe(data['accuracy'], hide_index=True)
    
    # Calculate recoveries
    recoveries = []
    for idx, row in data['accuracy'].iterrows():
        recovery = ((row['Calculated Conc (mg/L)'] - 0.3904) / row['Spike Conc (mg/L)']) * 100
        recoveries.append(recovery)
    
    avg_recovery = np.mean(recoveries)
    st.subheader(f"Average Recovery: {avg_recovery:.1f}%")
    
    # Interpretation
    st.subheader("Recovery Interpretation")
    if 80 <= avg_recovery <= 120:
        st.success("Recovery is within acceptable range (80-120%)")
    else:
        st.error("Recovery is outside acceptable range (80-120%)")

# Add some styling
st.markdown("""
<style>
    .stDataFrame {
        width: 100%;
    }
    .st-eb {
        padding: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)
