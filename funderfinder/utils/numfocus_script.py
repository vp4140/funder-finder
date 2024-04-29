import json

import pandas as pd

# Read the Excel file
df = pd.read_excel("../data/Small Development Grants - NumFOCUS.xlsx")

# Initialize an empty dictionary to store the aggregated results
result_dict = {}


# Define a function to convert the round to dates
def round_to_dates(round_number, year):
    if round_number == 1 or round_number == 2:
        return f"{year}-01-01T00:00:00Z", f"{year}-07-01T00:00:00Z"
    elif round_number == 3:
        return f"{year}-07-01T00:00:00Z", f"{year + 1}-01-01T00:00:00Z"


# Iterate over each row in the DataFrame
for index, row in df.iterrows():
    # Get the year based on the round number
    year = row["Year"]

    # Get the dates based on the round number and year
    dates_from, dates_to = round_to_dates(row["Round"], year)

    # Create a unique key using project name, year, and round number
    key = (row["Project"], year, row["Round"])  # Include year and round in the key

    # If the key already exists, accumulate the amount
    if key in result_dict:
        result_dict[key]["Amount_of_funding_usd"] += row["Amount"]
    else:
        # Otherwise, add a new entry
        result_dict[key] = {
            "Amount_of_funding_usd": row["Amount"],
            "Project": row["Project"],
            "Description": row["Proposal Title"],
            "datesFrom": dates_from,
            "datesTo": dates_to,
        }

# Convert the dictionary to a list of values
result = list(result_dict.values())

# Specify the path for the new JSON file
output_json_file = "../data/output.json"

# Write the result to the JSON file
with open(output_json_file, "w") as json_file:
    json.dump(result, json_file, indent=4)

print(f"Data has been saved to '{output_json_file}'.")
