# Credits: This code was inspired by Data Professor (http://youtube.com/dataprofessor)
import numpy as np
import pandas as pd
import streamlit as st
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

# Title and information of the App
st.markdown('''
     # EDA App

     This app is to make exploratory data analysis of databases using the 'ydata-profiling' library.

     ---
     ''')

     # Upload CSV file
with st.header("Upload your data in CSV format"):
    uploaded_file = st.file_uploader("Upload you file", type=["csv"])

type_report = st.selectbox("Select the type of report", ['minimal', 'explorative'])

# Pandas Profiling Report
if uploaded_file is not None:
    @st.cache_data
    def load_csv():
        csv = pd.read_csv(uploaded_file)
        return csv
    df = load_csv()
    if type_report == "minimal":
        pr = ProfileReport(df, minimal=True)
    else:
        pr = ProfileReport(df, explorative=True)
    st.header("Input DataFrame")
    st.write(df)
    st.write("---")
    st.header("Report")
    st_profile_report(pr)
    pr = ProfileReport(df)
    report_json = pr.to_json()
    st.download_button(
        label="Download Report in json",
        data=report_json,
        file_name="EDA_Report.json",
        mime="text/json",
    )
    report_html = pr.to_html()
    st.download_button(
        label="Download Report in html",
        data=report_json,
        file_name="EDA_Report.html",
        mime="text/html",
    )
else:
    st.info("Waiting CSV file")
    if st.button("Use Example Dataset"):
        @st.cache_data
        def load_data():
            exm = pd.DataFrame(
                np.random.rand(100, 5),
                columns = ["First", "Second", "Third", "Fourth", "Fifth"]
            )
            return exm
        df = load_data()
        if type_report == "minimal":
            pr = ProfileReport(df, minimal=True)
        elif type_report == "explorative":
            pr = ProfileReport(df, explorative=True)
        st.header("Example DataFrame")
        st.write(df)
        st.write("---")
        st.header("Report")
        st_profile_report(pr, navbar=True)
    pr = ProfileReport(df)
    report_json = pr.to_json()
    st.download_button(
        label="Download Report",
        data=report_json,
        file_name="EDA_Report.json",
        mime="text/json",
    )
    report_html = pr.to_html()
    st.download_button(
        label="Download Report in html",
        data=report_json,
        file_name="EDA_Report.html",
        mime="text/html",
    )