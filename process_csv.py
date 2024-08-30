import pandas as pd
import streamlit as st
import io

def remove_duplicates_from_csvs(file1, file2):
    """
    Remove duplicates from two CSV files and return the result as a DataFrame.
    
    Args:
    file1 (io.BytesIO): First uploaded CSV file
    file2 (io.BytesIO): Second uploaded CSV file
    
    Returns:
    pd.DataFrame: Deduplicated DataFrame
    """
    # Read both CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # Display information about the input files
    st.write(f"File 1 shape: {df1.shape}")
    st.write(f"File 2 shape: {df2.shape}")
    
    # Identify common columns
    common_columns = list(set(df1.columns) & set(df2.columns))
    st.write(f"Common columns: {common_columns}")
    
    # Use only common columns for deduplication
    df1 = df1[common_columns]
    df2 = df2[common_columns]
    
    # Concatenate the dataframes
    combined_df = pd.concat([df1, df2], ignore_index=True)
    st.write(f"Combined shape: {combined_df.shape}")
    
    # Remove duplicates based on the first column (URL)
    deduplicated_df = combined_df.drop_duplicates(subset=[combined_df.columns[0]])
    st.write(f"Deduplicated shape: {deduplicated_df.shape}")
    
    return deduplicated_df

def remove_duplicates_from_single_csv(file):
    """
    Remove duplicates from a single CSV file and return the result as a DataFrame.
    
    Args:
    file (io.BytesIO): Uploaded CSV file
    
    Returns:
    pd.DataFrame: Deduplicated DataFrame
    """
    # Read the CSV file
    df = pd.read_csv(file)
    
    # Display information about the input file
    st.write(f"Input file shape: {df.shape}")
    
    # Remove duplicates based on the first column (URL)
    deduplicated_df = df.drop_duplicates(subset=[df.columns[0]])
    st.write(f"Deduplicated shape: {deduplicated_df.shape}")
    
    return deduplicated_df

st.title("CSV Duplicate Remover")

st.write("Choose an option:")
option = st.radio("", ("Remove duplicates from two files", "Remove duplicates within a single file"))

if option == "Remove duplicates from two files":
    st.write("Upload two CSV files to remove duplicates")
    file1 = st.file_uploader("Choose the first CSV file", type="csv", key="file1")
    file2 = st.file_uploader("Choose the second CSV file", type="csv", key="file2")

    if file1 is not None and file2 is not None:
        if st.button("Remove Duplicates"):
            result_df = remove_duplicates_from_csvs(file1, file2)
            st.write("Duplicates removed. Preview of the result:")
            st.dataframe(result_df)
            
            # Provide download link for the result
            csv = result_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="output_without_duplicates.csv",
                mime="text/csv",
            )

else:
    st.write("Upload a single CSV file to remove duplicates within it")
    file = st.file_uploader("Choose a CSV file", type="csv", key="single_file")

    if file is not None:
        if st.button("Remove Duplicates"):
            result_df = remove_duplicates_from_single_csv(file)
            st.write("Duplicates removed. Preview of the result:")
            st.dataframe(result_df)
            
            # Provide download link for the result
            csv = result_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="output_without_duplicates_single.csv",
                mime="text/csv",
            )
