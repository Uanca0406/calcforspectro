import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from io import BytesIO

# Configure page settings
st.set_page_config(
    page_title="Spectrophotometry Analysis",
    page_icon="📊",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
    .header {
        font-size: 24px !important;
        font-weight: bold !important;
        color: #2E86C1 !important;
    }
    .metric-card {
        padding: 15px;
        border-radius: 10px;
        background-color: #F2F4F4;
        margin-bottom: 20px;
    }
    .sidebar .sidebar-content {
        background-color: #F8F9F9;
    }
    .stButton button {
        background-color: #2874A6;
        color: white;
    }
    .highlight {
        background-color: #F9E79F;
        padding: 2px 5px;
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.title("🖲️ Spectrophotometry Data Analysis")
st.markdown("Analyze absorbance data to determine sample concentrations using Beer's Law")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Data Input")
    
    st.subheader("Standard Curve Data")
    
    # Manual data entry option
    manual_entry = st.checkbox("Enter data manually")
    
    if manual_entry:
        # Create a dataframe for standards
        standards_data = pd.DataFrame(
            index=range(1, 6),
            columns=['Concentration (ppm)', 'Absorbance']
        )
        
        # Allow editing of standards data
        edited_standards = st.data_editor(
            standards_data, 
            hide_index=True,
            column_config={
                "Concentration (ppm)": st.column_config.NumberColumn(format="%.3f"),
                "Absorbance": st.column_config.NumberColumn(format="%.4f")
            }
        )
        
        st.caption("Enter at least 3 standard concentrations with corresponding absorbance values")
        uploaded_file = None
    else:
        uploaded_file = st.file_uploader("Or upload CSV/Excel file", type=["csv", "xlsx"])
    
    # Sample entry
    st.subheader("Sample Data")
    num_samples = st.number_input("Number of samples", min_value=1, max_value=10, value=2)
    
    st.markdown("---")
    st.caption("Developed by [Your Name] | Version 1.0")

# Main content area
if manual_entry or (uploaded_file is not None):
    # Load or create data
    if manual_entry:
        std_df = edited_standards.dropna().reset_index(drop=True)
        if len(std_df) < 3:
            st.error("Please enter data for at least 3 standard concentrations")
            st.stop()
    else:
        try:
            if uploaded_file.name.endswith('.csv'):
                std_df = pd.read_csv(uploaded_file)
            else:
                std_df = pd.read_excel(uploaded_file)
        except Exception as e:
            st.error(f"Error reading file: {e}")
            st.stop()
    
    # Verify required columns exist
    required_cols = {'Concentration (ppm)', 'Absorbance'}
    if not required_cols.issubset(std_df.columns):
        st.error(f"Data must include columns: {required_cols}")
        st.stop()
    
    # Calculate regression parameters
    try:
        slope, intercept, r_value, p_value, std_err = linregress(
            std_df['Concentration (ppm)'], 
            std_df['Absorbance']
        )
        r_squared = r_value**2
    except Exception as e:
        st.error(f"Error calculating regression: {e}")
        st.stop()
    
    # Create tabs
    tab1, tab2 = st.tabs(["📈 Calibration Analysis", "🧪 Sample Analysis"])
    
    with tab1:
        st.subheader("Calibration Curve Analysis")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("### Calibration Data")
            st.dataframe(std_df.style.format({
                'Concentration (ppm)': '{:.3f}',
                'Absorbance': '{:.4f}'
            }), height=300)
            
            # Display regression parameters in a card
            st.markdown("### Regression Parameters")
            
            st.markdown("""
            <div class="metric-card">
                <div>Slope (ε·l): <span class="highlight">{:.4f}</span></div>
                <div>Intercept: <span class="highlight">{:.4f}</span></div>
                <div>R-value: <span class="highlight">{:.4f}</span></div>
                <div>R-squared: <span class="highlight">{:.4f}</span></div>
            </div>
            """.format(slope, intercept, r_value, r_squared), unsafe_allow_html=True)
        
        with col2:
            st.markdown("### Calibration Curve")
            
            # Create plot
            fig, ax = plt.subplots(figsize=(8, 5))
            
            # Plot standards
            ax.scatter(
                std_df['Concentration (ppm)'], 
                std_df['Absorbance'],
                color='#2874A6',
                label='Standards'
            )
            
            # Plot regression line
            x_fit = np.linspace(0, std_df['Concentration (ppm)'].max()*1.1, 100)
            y_fit = slope * x_fit + intercept
            ax.plot(
                x_fit, 
                y_fit,
                '--',
                color='#7B241C',
                label=f'Fit: y = {slope:.2f}x + {intercept:.2f}'
            )
            
            ax.set_xlabel('Concentration (ppm)', fontsize=12)
            ax.set_ylabel('Absorbance', fontsize=12)
            ax.set_title('Calibration Curve', fontsize=14)
            ax.legend(loc='best', frameon=True)
            ax.grid(True, linestyle='--', alpha=0.7)
            
            # Display plot
            st.pyplot(fig)
            
            # Download options
            col21, col22 = st.columns(2)
            with col21:
                buf = BytesIO()
                fig.savefig(buf, format="png", dpi=150)
                st.download_button(
                    label="Download Plot",
                    data=buf.getvalue(),
                    file_name="calibration_curve.png",
                    mime="image/png",
                    use_container_width=True
                )
            
            with col22:
                st.download_button(
                    label="Download Data",
                    data=std_df.to_csv(index=False).encode('utf-8'),
                    file_name="calibration_data.csv",
                    mime="text/csv",
                    use_container_width=True
                )
    
    with tab2:
        st.subheader("Sample Concentration Calculation")
        
        # Create input fields for samples
        sample_entries = []
        with st.form("sample_form"):
            st.markdown("### Enter Sample Absorbance Values")
            
            cols = st.columns(2)
            for i in range(num_samples):
                if i % 2 == 0:
                    col = cols[0]
                else:
                    col = cols[1]
                
                with col:
                    absorbance = st.number_input(
                        f"Sample {i+1} Absorbance", 
                        min_value=0.0, 
                        max_value=3.0, 
                        value=0.0,
                        format="%.4f",
                        key=f"sample_{i}"
                    )
                    sample_entries.append(absorbance)
            
            submitted = st.form_submit_button("Calculate Concentrations")
        
        if submitted:
            # Calculate concentrations
            sample_results = []
            for i, absorbance in enumerate(sample_entries):
                conc = (absorbance - intercept) / slope if slope != 0 else 0
                sample_results.append({
                    "Sample": f"S-{i+1}",
                    "Absorbance": absorbance,
                    "Concentration (ppm)": conc if conc > 0 else 0
                })
            
            results_df = pd.DataFrame(sample_results)
            
            # Display results
            st.markdown("### Calculation Results")
            
            # Format results table
            st.dataframe(
                results_df.style.format({
                    "Absorbance": "{:.4f}",
                    "Concentration (ppm)": "{:.3f}"
                }),
                hide_index=True,
                height=min(300, 75*num_samples)
            )
            
            # Summary statistics
            st.markdown("### Summary Statistics")
            
            mean_conc = results_df["Concentration (ppm)"].mean()
            std_dev = results_df["Concentration (ppm)"].std()
            rsd = (std_dev / mean_conc * 100) if mean_conc > 0 else 0
            
            summ_col1, summ_col2, summ_col3 = st.columns(3)
            
            with summ_col1:
                st.metric(label="Mean Concentration", value=f"{mean_conc:.3f} ppm")
            
            with summ_col2:
                st.metric(label="Standard Deviation", value=f"{std_dev:.3f} ppm")
            
            with summ_col3:
                st.metric(label="Relative SD", value=f"{rsd:.1f}%")
            
            # Download results
            st.download_button(
                label="Download Results",
                data=results_df.to_csv(index=False).encode('utf-8'),
                file_name="sample_results.csv",
                mime="text/csv",
                use_container_width=True
            )

else:
    st.info("Please enter standard curve data manually or upload a file to begin analysis")
    st.markdown("""
    ### Expected File Format
    Your data file should contain at least these columns:
    - `Concentration (ppm)` - Standard concentrations in ppm
    - `Absorbance` - Corresponding absorbance values
    
    Example:
    """)
    
    example_data = pd.DataFrame({
        'Concentration (ppm)': [0, 0.5, 1.0, 2.0, 4.0],
        'Absorbance': [0.001, 0.125, 0.246, 0.492, 0.983]
    })
    
    st.dataframe(example_data.style.format({
        'Concentration (ppm)': '{:.1f}',
        'Absorbance': '{:.3f}'
    }), hide_index=True)
