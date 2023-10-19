# import argparse
# import os
# from typing import Union

# import requests

# from ._finder import Finder

# """
# Retrieves project funding statistics from Opencollective. To run this script, you must first set
# an OPENCOLLECTIVE_API_KEY environment variable. See: https://graphql-docs-v2.opencollective.com/access
# """


# class OpenCollectiveFinder(Finder):
#     name = "Open Collective"
#     API_KEY_NAME = "OPENCOLLECTIVE_API_KEY"

#     def __init__(self):
#         assert os.environ.get(
#             self.API_KEY_NAME
#         ), "Please `export OPENCOLLECTIVE_API_KEY=<your opencollective api key>"
#         self.api_key = os.environ.get(self.API_KEY_NAME)

#     def get_funding_stats(self, project_slug: str) -> dict:
#         """
#         Retrives funding statistics for a project. See: https://graphql-docs-v2.opencollective.com/queries/collective
#         :param project_slug: identifier for the project (like 'babel' in 'https://opencollective.com/babel')
#         :return: Dict of funding stats
#         """
#         query = """
#           query (
#             $slug: String!
#             $date1: DateTime!
#             $date2: DateTime!
#           ) {
#             collective (slug: $slug) {
#               id
#               stats {
#                 contributionsCountDate1:contributionsCount(
#                   dateFrom: $date1
#                   dateTo: $date1
#                   includeChildren: false
#                 )
#                 totalAmountReceivedDate1: totalAmountReceived(
#                   dateFrom: $date1
#                   dateTo: $date1
#                   includeChildren: false
#                 ) {
#                   currency
#                   value
#                 }
#                 contributorsCountDate2: contributionsCount(
#                   dateFrom: $date2
#                   dateTo: $date2
#                   includeChildren: false
#                 ) 
#                 totalAmountReceivedDate2: totalAmountReceived(
#                   dateFrom: $date2
#                   dateTo: $date2
#                   includeChildren: false
#                 ) {
#                   currency
#                   value
#                 } 
#               }
#             }
#           }
#         """
#         variables = {
#             "slug": project_slug, 
#             "date1": "2019-01-01T00:00:00.000Z",
#             "date2": "2020-01-01T00:00:00.000Z"
#             }
   
#         result = requests.post(
#             f"https://api.opencollective.com/graphql/v2/{self.api_key}",
#             json={"query": query, "variables": variables},
#         )
#         data = result.json()
#         print(data)
#         stats = data["data"]["collective"]
#         if stats:
#             return {
#                 "num_contributors": stats["totalFinancialContributors"],
#                 "total_funding_usd": stats["stats"]["totalAmountReceived"]["value"],
#             }

#     def run(self, gh_project_slug: Union[str, None] = None) -> list:
#         stats = self.get_funding_stats(self.get_repo_name(gh_project_slug))
#         return [stats] if stats else []


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
    
#     parser.add_argument(
#         "project_slug",
#         help="identifier for the project (like 'babel' in 'https://opencollective.com/babel')",
#     )
#     args = parser.parse_args()
#     finder = OpenCollectiveFinder()
#     stats = finder.get_funding_stats(args.project_slug)
#     print(stats)



# import argparse
# import os
# import requests
# from typing import Union

# class OpenCollectiveFinder:
#     # Constants for API key and GraphQL endpoint
#     API_KEY_NAME = "OPENCOLLECTIVE_API_KEY"
#     API_ENDPOINT = "https://api.opencollective.com/graphql/v2"

#     def __init__(self):
#         api_key = os.environ.get(self.API_KEY_NAME)
#         if not api_key:
#             raise EnvironmentError("Please set the OPENCOLLECTIVE_API_KEY environment variable.")
#         self.api_key = api_key

#     def get_funding_stats(self, project_slug: str, date1: str, date2: str) -> dict:
#         query = """
#             query (
#                 $slug: String!
#                 $date1: DateTime!
#                 $date2: DateTime!
#             ) {
#                 collective(slug: $slug) {
#                     id
#                     stats {
#                         contributionsCountDate1: contributionsCount(
#                             dateFrom: $date1
#                             dateTo: $date1
#                             includeChildren: false
#                         )
#                         totalAmountReceivedDate1: totalAmountReceived(
#                             dateFrom: $date1
#                             dateTo: $date1
#                             includeChildren: false
#                         ) {
#                             currency
#                             value
#                         }
#                         contributorsCountDate2: contributionsCount(
#                             dateFrom: $date2
#                             dateTo: $date2
#                             includeChildren: false
#                         ) 
#                         totalAmountReceivedDate2: totalAmountReceived(
#                             dateFrom: $date2
#                             dateTo: $date2
#                             includeChildren: false
#                         ) {
#                             currency
#                             value
#                         } 
#                     }
#                 }
#             }
#         """
#         variables = {
#             "slug": project_slug, 
#             "date1": date1,
#             "date2": date2,
#         }
   
#         result = requests.post(
#             self.API_ENDPOINT,
#             json={"query": query, "variables": variables},
#             headers={"Authorization": self.api_key}
#         )
        
#         data = result.json()
        
#         if "data" in data and "collective" in data["data"]:
#             collective_data = data["data"]["collective"]
#             return {
#                 "num_contributors": collective_data["stats"]["contributorsCountDate2"],
#                 "total_funding_usd": collective_data["stats"]["totalAmountReceivedDate2"]["value"],
#             }
#         else:
#             return {}  # Handle the case where data is missing or the query failed

#     def run(self, gh_project_slug: Union[str, None] = None) -> dict:
#         if not gh_project_slug:
#             print("GitHub project slug is missing.")
#             return {}

#         stats = self.get_funding_stats(
#             self.get_repo_name(gh_project_slug),
#             date1="2023-01-01",
#             date2="2022-01-01T00:00:00.000Z"
#         )
#         return stats

#     def get_repo_name(self, gh_project_slug: str) -> str:
#         # Implement your logic to extract the repository name from the GitHub project slug
#         pass
 
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
    
#     parser.add_argument(
#         "project_slug",
#         help="Identifier for the project (like 'babel' in 'https://opencollective.com/babel')",
#     )
#     args = parser.parse_args()
    
#     finder = OpenCollectiveFinder()
#     stats = finder.run(args.project_slug)
#     print(stats)


import argparse
import os
import requests
from typing import Union
import matplotlib.pyplot as plt
from ._finder import Finder

class OpenCollectiveFinder(Finder):
    # Constants for API key and GraphQL endpoint
    API_KEY_NAME = "OPENCOLLECTIVE_API_KEY"
    API_ENDPOINT = "https://api.opencollective.com/graphql/v2"

    def __init__(self):
        api_key = os.environ.get(self.API_KEY_NAME)
        if not api_key:
            raise EnvironmentError("Please set the OPENCOLLECTIVE_API_KEY environment variable.")
        self.api_key = api_key

    def get_funding_stats(self, project_slug: str, dates: list = None) -> dict:
        funding_stats = []
        
        query = """
            query (
                $slug: String!
                $dates: [DateTime!]!
            ) {
                collective(slug: $slug) {
                    id
                    stats {
                        contributionsCounts(dates: $dates)
                        totalAmountReceived(dates: $dates) {
                            currency
                            value
                        }
                    }
                }
            }
        """

        for date in dates:
            variables = {
                "slug": project_slug,
                "dates": [date],
            }

            result = requests.post(
                self.API_ENDPOINT,
                json={"query": query, "variables": variables},
                headers={"Authorization": self.api_key}
            )

            data = result.json()
            collective_data = data.get("data", {}).get("collective", {})
            
            if collective_data:
                stats = {
                    "date": date,
                    "num_contributors": collective_data["stats"]["contributionsCounts"][0],
                    "total_funding_usd": collective_data["stats"]["totalAmountReceived"][0]["value"],
                }
                funding_stats.append(stats)

        return funding_stats

    def plot_funding_graph(self, funding_stats: list):
        # Extract data for plotting
        dates = [entry["date"] for entry in funding_stats]
        total_funding = [entry["total_funding_usd"] for entry in funding_stats]

        # Create and show the plot
        plt.figure(figsize=(10, 6))
        plt.plot(dates, total_funding, marker='o')
        plt.xlabel("Date")
        plt.ylabel("Total Funding (USD)")
        plt.title("Funding Over Time")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.show()

    def run(self, gh_project_slug: Union[str, None] = None, dates: list = None) -> list:
        funding_stats = self.get_funding_stats(self.get_repo_name(gh_project_slug), dates)
        if funding_stats:
            self.plot_funding_graph(funding_stats)
        return funding_stats

    def get_repo_name(self, gh_project_slug: str) -> str:
        parts = gh_project_slug.split('/')
    if len(parts) == 2:
        return parts[1]
    return gh_project_slug

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument(
        "project_slug",
        help="Identifier for the project (like 'babel' in 'https://opencollective.com/babel')",
    )
    args = parser.parse_args()
    
    finder = OpenCollectiveFinder()
    stats = finder.run(args.project_slug)
    print(stats)

