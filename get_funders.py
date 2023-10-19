# # # Retrieves all funding information for a project from supported sources

# # import argparse
# # from datetime import datetime

# # from sources.config import PRODUCTION_FINDERS


# # def get_project_funders(repo_name: str) -> list:
# #     """
# #     Attempts to retrieve funding data from each source for matching projects. When funding sources are found, adds the
# #     source's name, a boolean is_funded field with value True, and the date the funding data was retrieved to the
# #     metadata of each source of funding that was found
# #     :param repo_name: Github identifier for the project (e.g. georgetown-cset/funder-finder)
# #     :return: An array of funding metadata
# #     """
# #     project_funders = []
# #     for finder_class in PRODUCTION_FINDERS:
# #         finder = finder_class()
# #         funding = finder.run(repo_name)
# #         if funding:
# #             for source in funding:
# #                 source["type"] = finder_class.name
# #                 source["is_funded"] = True
# #                 source["date_of_data_collection"] = datetime.now().strftime("%Y-%m-%d")
# #                 project_funders.append(source)
# #     return project_funders


# # if __name__ == "__main__":
# #     parser = argparse.ArgumentParser()
# #     parser.add_argument(
# #         "repo_name",
# #         help="Identifier for GitHub repo, in the form `owner_name/repo_name` "
# #         "(e.g. georgetown-cset/funder-finder)",
# #     )
# #     args = parser.parse_args()

# #     print(get_project_funders(args.repo_name))


# it is the code for get_funders.py to get single repo's funding information


# import os
# import json
# from datetime import datetime

# from sources.config import PRODUCTION_FINDERS

# def get_project_funders(repo_name: str) -> list:
#     """
#     Attempts to retrieve funding data from each source for matching projects. When funding sources are found, adds the
#     source's name, a boolean is_funded field with value True, and the date the funding data was retrieved to the
#     metadata of each source of funding that was found
#     :param repo_name: Github identifier for the project (e.g. georgetown-cset/funder-finder)
#     :return: An array of funding metadata
#     """
#     project_funders = []
#     for finder_class in PRODUCTION_FINDERS:
#         finder = finder_class()
#         funding = finder.run(repo_name)
#         if funding:
#             for source in funding:
#                 source["type"] = finder_class.name
#                 source["is_funded"] = True
#                 source["date_of_data_collection"] = datetime.now().strftime("%Y-%m-%d")
#                 project_funders.append(source)
#     return project_funders

# if __name__ == "__main__":
#     import argparse

#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "repo_name",
#         help="Identifier for GitHub repo, in the form `owner_name/repo_name` "
#         "(e.g. georgetown-cset/funder-finder)",
#     )
#     args = parser.parse_args()

#     repo_name = args.repo_name

#     # Call the function and print the result as JSON
#     funding_data = get_project_funders(repo_name)
#     print(json.dumps(funding_data, indent=2))




# it is the code for get_funders.py to get through single repo's funding information over multiple dates

# import os
# import json
# from datetime import datetime, timedelta

# from sources.config import PRODUCTION_FINDERS

# def get_project_funders(repo_name: str, dates: list) -> list:
#     """
#     Attempts to retrieve funding data from each source for matching projects for multiple dates.
#     :param repo_name: Github identifier for the project (e.g. georgetown-cset/funder-finder)
#     :param dates: List of dates in string format (e.g., ["2023-09-12", "2023-09-13"])
#     :return: An array of funding metadata for each date
#     """
#     all_project_funders = []

#     for date_str in dates:
#         project_funders = []
        
#         for finder_class in PRODUCTION_FINDERS:
#             finder = finder_class()
#             funding = finder.run(repo_name)
#             if funding:
#                 for source in funding:
#                     source["type"] = finder_class.name
#                     source["is_funded"] = True
#                     source["date_of_data_collection"] = date_str
#                     project_funders.append(source)
        
#         all_project_funders.append({
#             "date": date_str,
#             "funding_data": project_funders
#         })

#     return all_project_funders

# if __name__ == "__main__":
#     import argparse

#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "repo_name",
#         help="Identifier for GitHub repo, in the form `owner_name/repo_name` "
#         "(e.g. georgetown-cset/funder-finder)",
#     )
#     args = parser.parse_args()

#     repo_name = args.repo_name

#     # Define a list of dates for which you want to collect funding data
#     # Example: ["2023-09-12", "2023-09-13"]
#     dates = ["2023-09-12", "2023-09-13"]

#     # Call the function for each date and print the result as JSON
#     for date_str in dates:
#         funding_data = get_project_funders(repo_name, [date_str])
#         print(f"Funding data for date {date_str}:")
#         print(json.dumps(funding_data, indent=2))



# it is the code for get_funders.py to get through the repo name for different dates and gives only the total funding in USD

# import os
# import json
# from datetime import datetime, timedelta

# from sources.config import PRODUCTION_FINDERS

# def get_total_funding_usd(repo_name: str, dates: list) -> dict:
#     """
#     Attempts to retrieve the total funding in USD for a repository for multiple dates.
#     :param repo_name: Github identifier for the project (e.g. georgetown-cset/funder-finder)
#     :param dates: List of dates in string format (e.g., ["2023-09-12", "2023-09-13"])
#     :return: A dictionary where keys are dates and values are the total funding in USD
#     """
#     total_funding = {}

#     for date_str in dates:
#         total_usd = 0
        
#         for finder_class in PRODUCTION_FINDERS:
#             finder = finder_class()
#             funding = finder.run(repo_name)
#             if funding:
#                 for source in funding:
#                     if "total_funding_usd" in source:
#                         total_usd += source["total_funding_usd"]
        
#         total_funding[date_str] = total_usd

#     return total_funding

# if __name__ == "__main__":
#     import argparse

#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "repo_name",
#         help="Identifier for GitHub repo, in the form `owner_name/repo_name` "
#         "(e.g. georgetown-cset/funder-finder)",
#     )
#     args = parser.parse_args()

#     repo_name = args.repo_name

#     # Define a list of dates for which you want to collect funding data
#     # Example: ["2023-09-12", "2023-09-13"]
#     dates = ["2023-09-12", "2023-09-13"]

#     # Call the function for each date and print the total funding in USD
#     total_funding_data = get_total_funding_usd(repo_name, dates)
#     for date_str, total_usd in total_funding_data.items():
#         print(f"Total funding in USD for {date_str}: {total_usd}")





# # it is the code for get_funders.py to get through the repo name for different dates and gives only the total funding in USD 
# #and the total funding in USD for each source with plotting
# import os
# import json
# from datetime import datetime, timedelta
# import matplotlib.pyplot as plt  # Import Matplotlib

# from sources.config import PRODUCTION_FINDERS

# def get_total_funding_usd(repo_name: str, dates: list) -> dict:
#     """
#     Attempts to retrieve the total funding in USD for a repository for multiple dates.
#     :param repo_name: Github identifier for the project (e.g. georgetown-cset/funder-finder)
#     :param dates: List of dates in string format (e.g., ["2023-09-12", "2023-09-13"])
#     :return: A dictionary where keys are dates and values are the total funding in USD
#     """
#     total_funding = {}

#     for date_str in dates:
#         total_usd = 0
        
#         for finder_class in PRODUCTION_FINDERS:
#             finder = finder_class()
#             funding = finder.run(repo_name)
#             if funding:
#                 for source in funding:
#                     print(source)
#                     if "total_funding_usd" in source:
#                         total_usd += source["total_funding_usd"]
        
#         total_funding[date_str] = total_usd

#     return total_funding

# if __name__ == "__main__":
#     import argparse

#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "repo_name",
#         help="Identifier for GitHub repo, in the form `owner_name/repo_name` "
#         "(e.g. georgetown-cset/funder-finder)",
#     )
#     args = parser.parse_args()
#     dates = ["2001-01-12","2012-02-12","2023-03-12","2023-04-12",
#              "2023-05-12","2023-06-12","2023-07-12","2023-08-12","2023-09-12","2023-10-12", "2023-11-12","2023-12-12"]

#     repo_name = args.repo_name
#     print(get_total_funding_usd(repo_name, dates))

#     # Define a list of dates for which you want to collect funding data
#     # Example: ["2023-09-12", "2023-09-13"]
#     dates = ["2001-01-12","2012-02-12","2023-03-12","2023-04-12",
#              "2023-05-12","2023-06-12","2023-07-12","2023-08-12","2023-09-12","2023-10-12", "2023-11-12","2023-12-12"]

#     # Call the function for each date and print the total funding in USD
#     total_funding_data = get_total_funding_usd(repo_name, dates)
#     for date_str, total_usd in total_funding_data.items():
#         print(f"Total funding in USD for {date_str}: {total_usd}")

#     # Extract data for plotting
#     x = dates
#     y = [total_funding_data[date] for date in dates]

#     # Create a simple line plot
#     plt.figure(figsize=(10, 6))  # Set the figure size
#     plt.plot(x, y, marker='o', linestyle='-')
#     plt.title("Total Funding in USD Over Time for  Cantera/cantera")
#     plt.xlabel("Date")
#     plt.ylabel("Total Funding in USD")
#     plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
#     plt.tight_layout()

#     # Save or display the plot
#     plt.savefig("funding_plot.png")  # Save the plot as an image
#     plt.show()  # Display the plot on screen



# it is the code for get_funders.py to get through the repo name for different dates and 
# gives only the total funding in USD and plotting 2nd version

# import os
# import json
# from datetime import datetime, timedelta
# import matplotlib.pyplot as plt

# from sources.config import PRODUCTION_FINDERS

# def get_total_funding_usd(repo_name: str, dates: list) -> dict:
#     """
#     Attempts to retrieve the total funding in USD for a repository until multiple dates.
#     :param repo_name: Github identifier for the project (e.g. georgetown-cset/funder-finder)
#     :param dates: List of dates in string format (e.g., ["2023-09-12", "2023-09-13"])
#     :return: A dictionary where keys are dates and values are the total funding in USD until that date
#     """
#     total_funding = {}

#     for date_str in dates:
#         total_usd = 0
        
#         for finder_class in PRODUCTION_FINDERS:
#             finder = finder_class()
#             funding = finder.run(repo_name)
#             if funding:
#                 for source in funding:
#                     if "total_funding_usd" in source and "date_of_data_collection" in source:
#                         funding_date = datetime.strptime(source["date_of_data_collection"], "%Y-%m-%d")
#                         if funding_date <= datetime.strptime(date_str, "%Y-%m-%d"):
#                             #print(source["total_funding_usd"])
#                             total_usd += source["total_funding_usd"]
        
#         total_funding[date_str] = total_usd

#     return total_funding

# if __name__ == "__main__":
#     import argparse

#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "repo_name",
#         help="Identifier for GitHub repo, in the form `owner_name/repo_name` "
#         "(e.g. georgetown-cset/funder-finder)",
#     )
#     args = parser.parse_args()

#     repo_name = args.repo_name

#     # Define a list of dates for which you want to collect funding data
#     dates = ["2001-01-12","2012-02-12","2023-03-12","2023-04-12",
#              "2023-05-12","2023-06-12","2023-07-12","2023-08-12","2023-09-12","2023-10-12", "2023-11-12","2023-12-12"]

#     # Call the function for each date and print the total funding in USD until that date
#     total_funding_data = get_total_funding_usd(repo_name, dates)
#     for date_str, total_usd in total_funding_data.items():
#         print(f"Total funding in USD until {date_str}: {total_usd}")

#     # Extract data for plotting
#     x = dates
#     y = [total_funding_data[date] for date in dates]

#     # Create a simple line plot
#     plt.figure(figsize=(10, 6))  # Set the figure size
#     plt.plot(x, y, marker='o', linestyle='-')
#     plt.title(f"Total Funding in USD Until a Specific Date for {repo_name}")
#     plt.xlabel("Date")
#     plt.ylabel("Total Funding in USD")
#     plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
#     plt.tight_layout()

#     # Save or display the plot
#     plt.savefig("funding_plot.png")  # Save the plot as an image
#     plt.show()  # Display the plot on the screen


# it is the code for get_funders.py to get through the repo name for different dates and
# gives only the total funding in USD and plotting 3rd version

# import os
# import requests
# import datetime
# import matplotlib.pyplot as plt

# # Define your GitHub token and repository information
# GITHUB_TOKEN = os.environ.get("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")
# REPO_OWNER = "Cantera"
# REPO_NAME = "cantera"

# # Define the date range for which you want to calculate funding amounts
# start_date = datetime.date(2023, 1, 1)
# end_date = datetime.date(2015, 12, 31)

# # Initialize lists to store dates and funding amounts
# dates = []
# funding_amounts = []

# # Make API requests to retrieve funding data for the GitHub repository
# while start_date <= end_date:
#     # Format the date as YYYY-MM-DD
#     formatted_date = start_date.strftime("%Y-%m-%d")

#     # Construct the API URL
#     api_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/community/profile"
#     headers = {"Authorization": f"Bearer {GITHUB_TOKEN}"}
#     params = {"from": formatted_date, "to": formatted_date}

#     # Make the API request
#     response = requests.get(api_url, headers=headers, params=params)

#     if response.status_code == 200:
#         data = response.json()
#         funding_amount = data.get("sponsorship_total_in_cents", 0) / 100  # Convert to USD
#         dates.append(formatted_date)
#         funding_amounts.append(funding_amount)

#     # Increment the date
#     start_date += datetime.timedelta(days=1)

# # Plot the funding amounts over time
# plt.plot(dates, funding_amounts, marker='o', linestyle='-')
# plt.xlabel("Date")
# plt.ylabel("Funding Amount (USD)")
# plt.title(f"Funding Over Time for {REPO_OWNER}/{REPO_NAME}")
# plt.xticks(rotation=45)
# plt.tight_layout()
# plt.show()


# it is the code for get_funders.py to get through the repo name for different dates and
# gives only the total funding in USD and plotting 4th version
# import json
# import matplotlib.pyplot as plt
# from datetime import datetime

# # Define a function to read data from a JSONL file
# def read_jsonl(file_path):
#     data = []
#     with open(file_path, 'r') as json_file:
#         for line in json_file:
#             data.append(json.loads(line))
#     return data

# # Define a function to calculate cumulative funding amounts for each year
# def calculate_cumulative_funding(data, repository_name, years):
#     cumulative_funding = 0
#     cumulative_funding_by_year = []
#     for year in years:
#         for entry in data:
#             print(entry)
#             if 'funding_date' in entry and 'funding_amount' in entry:
#                 date = datetime.strptime(entry['funding_date'], '%Y-%m-%d')
#                 if date.year <= year and entry['name'] == repository_name:
#                     cumulative_funding += float(entry['funding_amount'])
#         cumulative_funding_by_year.append(cumulative_funding)
#     return cumulative_funding_by_year

# jsonl_file_path = 'D:/open@rit/funder-finder/funderfinder/data/numfocus.jsonl'
# # Read data from the JSONL file
# data = read_jsonl(jsonl_file_path)

# # Define the repository name
# repository_name = "conda"

# # Create a list of years from 2015 to 2023
# years = list(range(2015, 2024))

# # Calculate cumulative funding for each year
# cumulative_funding_by_year = calculate_cumulative_funding(data, repository_name, years)

# # Create the plot
# plt.figure(figsize=(12, 6))
# plt.plot(years, cumulative_funding_by_year, marker='o', linestyle='-')

# # Add labels and title
# plt.xlabel('Year')
# plt.ylabel('Cumulative Funding Amount')
# plt.title(f'Cumulative Funding for {repository_name} (2015-2023)')

# # Show the plot
# plt.grid(True)
# plt.tight_layout()
# plt.show()





# it is code for get_funders.py to get through all the repos in the json file



# import os
# import json
# from datetime import datetime

# from sources.config import PRODUCTION_FINDERS

# def get_project_funders(repo_name: str) -> list:
#     """
#     Attempts to retrieve funding data from each source for matching projects. When funding sources are found, adds the
#     source's name, a boolean is_funded field with value True, and the date the funding data was retrieved to the
#     metadata of each source of funding that was found
#     :param repo_name: Github identifier for the project (e.g. georgetown-cset/funder-finder)
#     :return: An array of funding metadata
#     """
#     project_funders = []
#     for finder_class in PRODUCTION_FINDERS:
#         finder = finder_class()
#         funding = finder.run(repo_name)
#         if funding:
#             for source in funding:
#                 source["type"] = finder_class.name
#                 source["is_funded"] = True
#                 source["date_of_data_collection"] = datetime.now().strftime("%Y-%m-%d")
#                 project_funders.append(source)
#     return project_funders

# if __name__ == "__main__":
#     import argparse

#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "json_file_path",
#         help="data/numfocus.jsonl",
#     )
#     args = parser.parse_args()

#     json_file_path = args.json_file_path

#     # Initialize a list to store the funding data for all repositories
#     all_funding_data = []

#     # Read JSON objects from the file and extract 'github_name' from each object
#     with open(json_file_path, 'r') as json_file:
#         for line in json_file:
#             data = json.loads(line)
#             if 'github_name' in data:
#                 repo_name = data['github_name']
#                 funding_data = get_project_funders(repo_name)
#                 all_funding_data.extend(funding_data)

#     # Print the result as JSON
#     print(json.dumps(all_funding_data, indent=2))
# Retrieves all funding information for a project from supported sources

# import argparse
# from datetime import datetime

# from sources.config import PRODUCTION_FINDERS


# def get_project_funders(repo_name: str) -> list:
#     """
#     Attempts to retrieve funding data from each source for matching projects. When funding sources are found, adds the
#     source's name, a boolean is_funded field with value True, and the date the funding data was retrieved to the
#     metadata of each source of funding that was found
#     :param repo_name: Github identifier for the project (e.g. georgetown-cset/funder-finder)
#     :return: An array of funding metadata
#     """
#     project_funders = []
#     for finder_class in PRODUCTION_FINDERS:
#         finder = finder_class()
#         funding = finder.run(repo_name)
#         if funding:
#             print(funding)
#             for source in funding:
#                 source["type"] = finder_class.name
#                 source["is_funded"] = True
#                 source["date_of_data_collection"] = datetime.now().strftime("%Y-%m-%d")
#                 project_funders.append(source)
#     return project_funders


# if __name__ == "__main__":
#     # parser = argparse.ArgumentParser()
#     # parser.add_argument(
#     #     "repo_name",
#     #     help="Identifier for GitHub repo, in the form `owner_name/repo_name` "
#     #     "(e.g. georgetown-cset/funder-finder)",
#     # )
#     # args = parser.parse_args()

#     print(get_project_funders('conda'))



# import argparse
# from datetime import datetime

# from sources.config import PRODUCTION_FINDERS


# def get_project_funders(repo_name: str, dates: list = None) -> list:
#     """
#     Attempts to retrieve funding data from each source for matching projects. When funding sources are found, adds the
#     source's name, a boolean is_funded field with value True, and the date the funding data was retrieved to the
#     metadata of each source of funding that was found
#     :param repo_name: Github identifier for the project (e.g. georgetown-cset/funder-finder)
#     :param dates: List of dates to collect funding data for (optional)
#     :return: An array of funding metadata
#     """
#     project_funders = []
#     for finder_class in PRODUCTION_FINDERS:
#         finder = finder_class()
#         funding = finder.run(repo_name, dates)
#         if funding:
#             print(funding)
#             for source in funding:
#                 source["type"] = finder_class.name
#                 source["is_funded"] = True
#                 source["date_of_data_collection"] = datetime.now().strftime("%Y-%m-%d")
#                 project_funders.append(source)
#     return project_funders


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "repo_name",
#         help="Identifier for GitHub repo, in the form `owner_name/repo_name` "
#         "(e.g., georgetown-cset/funder-finder)",
#     )
#     parser.add_argument(
#         "--dates",
#         nargs='+',  # Accept multiple dates as arguments
#         help="List of dates to collect funding data for (e.g., 2015-02-12 2016-03-15)",
#         default=[],
#     )
#     args = parser.parse_args()

#     print(get_project_funders(args.repo_name, args.dates))


import argparse
from datetime import datetime

from sources.config import PRODUCTION_FINDERS

def get_project_funders(repo_name: str, dates: list = None) -> list:
    """
    Attempts to retrieve funding data from each source for matching projects. When funding sources are found, adds the
    source's name, a boolean is_funded field with value True, and the date the funding data was retrieved to the
    metadata of each source of funding that was found
    :param repo_name: Github identifier for the project (e.g. georgetown-cset/funder-finder)
    :param dates: An optional list of dates in YYYY-MM-DD format
    :return: An array of funding metadata
    """
    project_funders = []
    
    for finder_class in PRODUCTION_FINDERS:
        finder = finder_class()
        funding = finder.run(repo_name, dates)
        if funding:
            for source in funding:
                source["type"] = finder_class.name
                source["is_funded"] = True
                source["date_of_data_collection"] = datetime.now().strftime("%Y-%m-%d")
                project_funders.append(source)
    
    return project_funders

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Retrieve funding data for a GitHub repository.")
    
    parser.add_argument(
        "repo_name",
        help="GitHub repository identifier in the format 'owner/repo_name'",
    )
    
    parser.add_argument(
        "--dates",
        nargs='+',
        help="List of dates in YYYY-MM-DD format (optional)",
    )
    
    args = parser.parse_args()

    # Check if dates are provided, and if not, use the default date
    if args.dates is None:
        args.dates = [datetime.now().strftime("%Y-%m-%d")]

    print(get_project_funders(args.repo_name, args.dates))
