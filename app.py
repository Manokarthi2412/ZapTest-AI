import streamlit as st
import pandas as pd
from io import StringIO
import os
import extract
import DocAgent
import TestCraftAgent
import json
import testApi 


path = "uploads/app.py"

st.markdown("<h1 style='color: lime;'>ZapTest AI</h1>", unsafe_allow_html=True)

def func(routes):
    for route in routes:
        str_=" "
        str_ += f"Function: {route['function_name']}"
        str_ +=f"Route: {route['route']}"
        str_ +=f"Methods: {route['methods']}"
        str_ +=f"Path Params: {route['path_params']}"
        str_ +=f"JSON Body Fields: {route['json_body_fields']}"
        content = str_
        response = DocAgent.docAgent(content)
        with open("documentation.md", "a") as file:
            file.write(response) 
    st.write("Successfully generated Documentation")

def testCases(routes):
    columns = ['Test Case', 'URL', 'Method', 'Request Body (JSON)', 'Expected Response']

    # Create an empty DataFrame with the specified columns
    df= pd.DataFrame(columns=columns)

    # print(routes)
    for route in routes:
        str_=""
        str_ += f"Function: {route['function_name']}"
        str_ +=f"Route: {route['route']}"
        str_ +=f"Methods: {route['methods']}"
        str_ +=f"Path Params: {route['path_params']}"
        str_ +=f"JSON Body Fields: {route['json_body_fields']}"
        content = str_
        response = TestCraftAgent.testgenAgent(content)
        # print(type(response))
        test_cases = json.loads(response)
        # Convert the 'Request Body (JSON)' string to a dictionary if it's not empty
        for test_case in test_cases:
            if test_case['Request Body (JSON)']:  # Only parse if the body is not empty
                test_case['Request Body (JSON)'] = json.loads(test_case['Request Body (JSON)'])
        for test in test_cases:
            df = pd.concat([df, pd.DataFrame([test])], ignore_index=True)

    st.dataframe(df)
    df.to_excel('test_cases.xlsx', index=False)
tab = st.selectbox("",("Home","Documentation and Testcases", "Test APIs"))
if tab =="Home":
    st.markdown("""
### Welcome to **ZapTest AI!**

ZapTest AI is an advanced, AI-powered solution tailored for **API testing**. It simplifies your workflow by:
- Generating **comprehensive API documentation**
- Creating **test cases** to validate APIs effectively

This application is specifically designed for **Flask-based applications**.

---

### **Steps to Get Started:**

#### **1. Documentation & Test Cases Tab**
- **Upload** the `app.py` file.
- Click **Extract Routes** to extract routes from the uploaded file.
- Click **Generate Documentation** to create a `documentation.md` file.
- Click **Generate Test Cases** to generate test cases, which can be downloaded as a `.csv` file.

#### **2. Test APIs Tab**
- **Upload** the `testcases.csv` file generated in the previous step.
- Enter the **base URL** of the server.
- Click **Test** to test all the cases.
- The **test results** will be displayed as a table and can be downloaded as a `.csv` file.

---

""")

    st.caption("⚠️ Ensure the file names match those mentioned in the steps above.")

if tab == "Documentation and Testcases":
    st.markdown("### **Documentation & Test Cases**")

    st.caption("⚠️ Ensure that the file name is ```app.py``` ")
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # Save the uploaded file locally
        save_path = os.path.join("uploads", uploaded_file.name)
        
        # Create 'uploads' directory if it doesn't exist
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        
        # Write the file to the local directory
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.write(f"File saved at: {save_path}")


    # Initialize session state for routes
    if "routes" not in st.session_state:
        st.session_state.routes = None

    # First button to extract routes
    if st.button("Extract routes"):
        # Assuming extract.extract_routes_with_inputs(path) returns a value
        # path = "your/path/here"  # Replace with actual path
        st.session_state.routes = extract.extract_routes_with_inputs(path)
        st.success("Extracted successfully")
        st.json(st.session_state.routes)

    # Second button to generate documentation
    if st.session_state.routes is not None:  # Ensure routes are available
        if st.button("Generate Documentation"):
            func(st.session_state.routes)
            st.success("Documentation generated successfully!")
            
            
            # Add download button
            with open("documentation.md", "r") as file:
                md_content = file.read()
            
            st.download_button(
                label="Download Documentation",
                data=md_content,
                file_name="documentation.md",
                mime="text/markdown"
            ) 
    # Second button to generate documentation
    if st.session_state.routes is not None:  # Ensure routes are available
        if st.button("Generate testcases"):
            testCases(st.session_state.routes)
            st.success("Test Cases generated successfully!")

elif tab == "Test APIs":
    st.markdown("This page allows you to test your APIs by uploading the generated test cases and specifying the server's base URL. Execute the tests and view detailed results.")
    st.caption("⚠️ Make sure the file name is `testcases.csv` and that the server is running.")

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # Save the uploaded file locally
        save_path = os.path.join("uploads", uploaded_file.name)
        
        # Create 'uploads' directory if it doesn't exist
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        
        # Write the file to the local directory
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.write(f"File saved at: {save_path}")
    else:
        st.write("Upload a file ")
    
    base_url = st.text_input("Enter the base url",placeholder="example: http://127.0.0.1:5000")
    
    if st.button("Test"):
        df = pd.read_csv(r"uploads/testcases.csv") # Ensure routes are available
        df = testApi.test_and_update_df(base_url, df)
        st.success("Tested successfullly")
        st.subheader("Test Results")
        st.dataframe(df)

        # Optionally allow the user to download the results
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Results", data=csv, file_name="test_results.csv", mime="text/csv")
        st.caption("⚠️ If the actual result differs from the expected result, it indicates that your endpoints do not handle those cases properly.")






