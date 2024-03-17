import streamlit as st
import pandas as pd 
from scipy.stats import norm 
import numpy as np 

data = pd.read_excel("data//AssignmentData.xlsx")


st.image("data//ingoj.png",width = 800)
def perform_ab_test(control_visitors, control_conversions, treatment_visitors, treatment_conversions, confidence_level):
    
    control_conversion_rate = control_conversions / control_visitors
    treatment_conversion_rate = treatment_conversions / treatment_visitors

    pooled_se = np.sqrt(control_conversion_rate * (1 - control_conversion_rate) / control_visitors 
                        + treatment_conversion_rate * (1 - treatment_conversion_rate) / treatment_visitors)
    
   
    z_score = norm.ppf(1 - (1 - confidence_level / 100) / 2)
    
    margin_of_error = z_score * pooled_se
   
    confidence_interval = (control_conversion_rate - treatment_conversion_rate - margin_of_error,
                           control_conversion_rate - treatment_conversion_rate + margin_of_error)
    
    # Perform hypothesis test
    if confidence_interval[0] > 0:
        return "Control Group is Better"
    elif confidence_interval[1] < 0:
        return "Experiment Group is Better"
    else:
        return "Indeterminate"

def main():
    st.title("A/B Test Analysis")
    st.sidebar.title("A/B Test Configuration")
    
    # Input fields for control group and treatment group data
    control_visitors = st.sidebar.number_input("Control Group Visitors", min_value=0, step=1)
    control_conversions = st.sidebar.number_input("Control Group Conversions", min_value=0, step=1)
    treatment_visitors = st.sidebar.number_input("Treatment Group Visitors", min_value=0, step=1)
    treatment_conversions = st.sidebar.number_input("Treatment Group Conversions", min_value=0, step=1)
    
  
    confidence_level = st.sidebar.radio("Confidence Level", [90, 95, 99])
    
    # Button to trigger A/B test
    if st.sidebar.button("Run A/B Test"):
        result = perform_ab_test(control_visitors, control_conversions, 
                                  treatment_visitors, treatment_conversions, 
                                  confidence_level)
        st.write("Result of A/B Test:", result)
if __name__ == "__main__":
    main()
