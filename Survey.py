# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).
import csv # The 'csv' module handles quoting/escaping so commas in answers don't break the file.

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    category_input = st.text_input("Enter a category (e.g., your class year or favorite subject):")
    value_input = st.text_input("How many hours of sleep do you get each night? (enter a number):")

    # The submit button for the form.
    submitted = st.form_submit_button("Submit Data")

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        # --- YOUR LOGIC GOES HERE ---
        # 1. Create a new row of data from 'category_input' and 'value_input'.
        # 2. Append this new row to the 'data.csv' file.
        #    - Using Python's built-in 'csv' module, opened in 'append' mode ('a').
        #    - newline='' lets the csv module write the line endings itself.

        category_clean = category_input.strip()
        value_clean = value_input.strip()

        # Validate the input before saving anything.
        if not category_clean or not value_clean:
            st.error("Please fill out both fields.")
        else:
            try:
                value_number = float(value_clean)  # Value must be numeric so it can be graphed.
            except ValueError:
                st.error("The value must be a number (e.g., 7.5).")
            else:
                # Write the header only if the file is new or empty.
                write_header = not (os.path.exists('data.csv') and os.path.getsize('data.csv') > 0)

                with open('data.csv', 'a', newline='') as f:
                    writer = csv.writer(f)
                    if write_header:
                        writer.writerow(['Category', 'Value'])
                    writer.writerow([category_clean, value_number])

                st.success("Your data has been submitted!")
                st.write(f"You entered: **Category:** {category_clean}, **Value:** {value_number}")


# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists('data.csv') and os.path.getsize('data.csv') > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv('data.csv')
    # Display the DataFrame as a table.
    st.dataframe(current_data_df)
else:
    # Nothing has been saved yet.
    st.warning("The 'data.csv' file is empty or does not exist yet.")
