import streamlit as st
import pandas as pd
import numpy as np

def main():
    # Set page title
    st.title("My Simple Streamlit App")
    
    # Add a sidebar header
    st.sidebar.header("Settings")
    
    # Add text input
    user_name = st.text_input("Enter your name", "")
    
    # Add a button
    if st.button("Say Hello"):
        if user_name:
            st.success(f"Hello {user_name}! 👋")
        else:
            st.warning("Please enter your name!")
    
    # Add a slider
    number = st.slider("Select a number", 0, 100, 50)
    st.write(f"Selected number: {number}")
    
    # Add selectbox
    option = st.selectbox(
        "What's your favorite color?",
        ["Red", "Blue", "Green", "Yellow"]
    )
    st.write(f"Your favorite color is {option}")
    
    # Create two columns
    col1, col2 = st.columns(2)
    
    # Add content to first column
    with col1:
        st.subheader("Random Numbers")
        if st.button("Generate Random Numbers"):
            numbers = np.random.randn(10)
            st.line_chart(numbers)
    
    # Add content to second column
    with col2:
        st.subheader("Sample DataFrame")
        df = pd.DataFrame({
            'Name': ['John', 'Jane', 'Bob', 'Alice'],
            'Age': [25, 30, 35, 28],
            'City': ['New York', 'London', 'Paris', 'Tokyo']
        })
        st.dataframe(df)
    
    # Add a file uploader
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        st.write("File uploaded successfully!")
        
    # Add checkbox
    if st.checkbox("Show additional information"):
        st.info("""
        This is a simple Streamlit app demonstration.
        It shows various Streamlit components like:
        - Text inputs
        - Buttons
        - Sliders
        - Charts
        - DataFrames
        """)

if __name__ == "__main__":
    main()