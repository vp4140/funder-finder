import argparse
import json
import os
from datetime import datetime, timedelta
from typing import Union

from pytz import timezone

from ._finder import Finder

"""
Get funding stats for NumFOCUS-affiliated or sponsored projects. At the moment, this is equivalent to a boolean
"is_affiliated" field that is true if the project is sponsored by or affiliated with NumFOCUS.

To determine whether a project is affiliated with NumFOCUS, we compare its name, slug, or github identifier
to the list of NumFOCUS-affiliated projects maintained in ../data/numfocus.jsonl. This dataset is automatically
updated on a weekly basis via a Github Action (.github/workflows/update_datasets.yml).
"""


class NumFocusFinder(Finder):
    name = "NumFOCUS"

    @staticmethod
    def get_funding_stats(search_params: dict, dates: list = None) -> Union[dict, None]:
        """
        Determines whether a project is sponsored or affiliated with NumFOCUS based on our scraped dataset and
        a project name, slug, or github owner and repo name
        :param search_params: Dict of user-provided metadata that we can use to match a numfocus project
        :return: Dict of funding stats
        """
        # if given github name  find the actual project name.
        # now with that name get the details from the json and send that arr
        # split by slash if lens greater than 1 then use first one.
        print(search_params, "search_params")

        listing_file = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "data", "output.json"
        )
        with open(listing_file) as json_file:
            # with open('../data/output.json', 'r') as json_file:
            data = json.load(json_file)

        # Filter data based on project name
        matching_objects = [
            item
            for item in data
            if item.get("Project").lower() == search_params["slug"].lower()
        ]
        # print(matching_objects,"matching")

        return matching_objects

        # print(search_params,"search params")
        # is_affiliated = False
        # listing_file = os.path.join(
        #     os.path.dirname(os.path.abspath(__file__)), "..", "data", "numfocus.jsonl"
        # )
        # with open(listing_file) as f:
        #     for line in f:
        #         project_metadata = json.loads(line.strip())
        #         for key in search_params:
        #             # In this block, we iterate through metadata fields provided by the user to match a numfocus project.
        #             # Some of these fields may be null either in the user-provided input (`search_params`), or in the
        #             # metadata we have for the current numfocus project (`project_metadata`). If either of these values
        #             # are null, run no further checks
        #             if not (project_metadata[key] and search_params[key]):
        #                 continue
        #             is_affiliated |= (
        #                 project_metadata[key].lower() == search_params[key].lower()
        #             )
        #             # In some cases the NumFOCUS affiliation is at the GitHub organization level rather than at the repo
        #             # level. So also allow match on repo owner
        #             if key == "github_name":
        #                 owner = search_params[key].split("/")[0].lower()
        #                 is_affiliated |= project_metadata[key].lower() == owner
        # if is_affiliated:
        #     return {
        #         "is_funded": True,
        #     }
        #
        # {'num_contributors': 2, 'Amount_of_funding_usd': 0, 'datesFrom': '2018-01-01T00:00:00Z',
        #  'datesTo': '2018-07-01T00:00:00Z'}

    def fill_missing_data(self, data):
        sorted_data = sorted(data, key=lambda x: datetime.fromisoformat(x["datesFrom"]))

        updated_data = []
        # print(sorted_data,"sorted data is here")
        for idx in range(len(sorted_data) - 1):
            current_end_date = datetime.fromisoformat(sorted_data[idx]["datesTo"])
            next_start_date = datetime.fromisoformat(sorted_data[idx + 1]["datesFrom"])

            # print(current_end_date,"Current end date")
            # print(next_start_date,"next sstart date ")

            while current_end_date < next_start_date:
                # Determine the next start date's year
                next_start_year = next_start_date.year

                if next_start_date.month <= 6:
                    next_start_year -= 1

                missing_period = {
                    "Amount_of_funding_usd": 0,
                    "datesFrom": current_end_date.strftime("%Y-%m-%dT%H:%M:%S%z"),
                    # Adjusting 'datesTo' based on the next start date's year
                    "datesTo": datetime(
                        next_start_year, 1 if next_start_date.month > 6 else 7, 1
                    ).strftime("%Y-%m-%dT%H:%M:%S%z"),
                }
                updated_data.append(missing_period)

                if (
                    (current_end_date.year % 400 == 0)
                    or (current_end_date.year % 100 != 0)
                    and (current_end_date.year % 4 == 0)
                ):

                    if current_end_date.month <= 6:
                        current_end_date += timedelta(days=182)
                    else:
                        current_end_date += timedelta(days=184)

                else:
                    if current_end_date.month <= 6:
                        current_end_date += timedelta(days=181)
                    else:
                        current_end_date += timedelta(days=184)

                # print(current_end_date)

        final_data = sorted(
            sorted_data + updated_data,
            key=lambda x: datetime.fromisoformat(x["datesFrom"]),
        )
        # print(final_data,"Final data is here")

        return final_data

    def run(self, gh_project_slug: Union[str, None] = None, dates: list = None) -> list:
        stats = self.get_funding_stats(
            {
                "name": None,
                "slug": self.get_repo_name(gh_project_slug),
                "github_name": gh_project_slug,
            },
            dates,
        )
        # // add the six month breaks between te data
        stats = self.fill_missing_data(stats)
        # breakpoint()
        return [stats] if stats else []


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--name", help="Case-insensitive name of the project, for example NiBabel"
    )
    parser.add_argument(
        "--slug", help="Case-insensitive project slug, for example nibabel"
    )
    parser.add_argument(
        "--github_name",
        help="Case-insensitive github owner and repo name, for example nipy/nibabel",
    )
    args = parser.parse_args()

    assert (
        args.name or args.slug or args.github_name
    ), "You must specify at least one of name, slug, or github_name"
    finder = NumFocusFinder()
    stats = finder.get_funding_stats(vars(args))
    print(stats)
