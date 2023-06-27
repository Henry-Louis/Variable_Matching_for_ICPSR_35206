# Project ICPSR_35206 Variable Matching 🎯

## Description

This project is designed to address variable naming inconsistencies across multiple datasets of the ICPSR_35206 agriculture data. Our approach is to match target variables of interest to the variable descriptions within each of the 46 sub-datasets, which allows for efficient cross-referencing of variables, even when naming conventions differ.

## High-Level Summary

The project's goal is to address inconsistencies in variable naming across the 46 sub-datasets in the ICPSR_35206 agriculture dataset. The provided Python code accomplishes this by:

1. **Loading PDF Files:** Reads PDF files in a specified directory into string variables. PDF files contain descriptions of the variables used in each dataset.

2. **Extracting Variable Descriptions:** Identifies and extracts variable descriptions from the loaded text. This information is saved in dictionaries with variable names as keys and descriptions as values, creating a kind of "lookup" for each dataset.

3. **Matching Interested Variables:** The script then matches a predefined list of "interested" variables - those which are of particular importance to the analysis - to variables in each of the 46 sub-datasets. It uses a Jaccard similarity function to measure the similarity between the descriptions of the interested variables and the descriptions of the variables in each sub-dataset. The function identifies the top 5 matches for each interested variable.

4. **Generating a Matched Table:** The final step of the script compiles this matching information into a Pandas DataFrame and saves it as a CSV file. This table includes the target variable of interest, the dataset number, and the top 5 matched variables. With this table, researchers can easily find which variables in each dataset best correspond to their variables of interest, simplifying the process of cross-referencing variables across different datasets.

## Audience

The primary users of this project will be researchers focusing on US agriculture data, and Data Analytics students who are dealing with multiple sub-datasets.

## Dependencies

To run this project, you will need Python 3.9 installed, along with the following packages:

- PyPDF2
- os
- re
- typing
- dask
- pandas
- json
- heapq

## Setup & Execution

First, ensure that Python 3.9 and all required packages are installed. Next, download the project files to your local machine. 

Before you run the code, please change the directory path in the script to match the location where you've stored the data sets on your local machine. The paths to be updated are located in the following lines:

```python
subfolders = list_subfolders("Your directory path here")
```

```python
df.to_csv("Your directory path here"+"variable_description_for_DS_{i+1}.csv", index=False)
```

```python
save_to_json(list_of_variable_description_dict, "Your directory path here")
```

```python
match_var_df.to_csv("Your directory path here"+"target_varible_matching_table.csv", index=False)
```

Once all directory paths are updated, you can simply run the entire Python script to generate a CSV file. This CSV will contain the top 5 matching variables for each interested variable description from each of the 46 datasets. 

## Future Improvements

While this script is functional for the current state of ICPSR_35206 data, it might be useful to expand the project to handle different matching algorithms or to adjust for potential changes in data formatting in future data updates. Also, the script could be further optimized or parallelized to handle even larger sets of data.
