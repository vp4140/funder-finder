import argparse
import json
import os

"""
Get funding stats for NumFOCUS-affiliated or sponsored projects. At the moment, this is equivalent to a boolean
"is_affiliated" field that is true if the project is sponsored by or affiliated with NumFOCUS.

To determine whether a project is affiliated with NumFOCUS, we compare its name, slug, or github identifier
to the list of NumFOCUS-affiliated projects maintained in ../data/numfocus.jsonl. This dataset is automatically
updated on a weekly basis via a Github Action (.github/workflows/update_datasets.yml).
"""


def get_funding_stats(args: dict) -> dict:
    """
    Determines whether a project is sponsored or affiliated with NumFOCUS based on our scraped dataset and
    a project name, slug, or github owner and repo name
    :param args: Dict of metadata that we can use to match a numfocus project
    :return: Dict of funding stats
    """
    is_affiliated = False
    with open(
        os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "data", "numfocus.jsonl"
        )
    ) as f:
        for line in f:
            meta = json.loads(line.strip())
            for key in args:
                if not (meta[key] and args[key]):
                    continue
                is_affiliated |= meta[key].lower() == args[key].lower()
                # In some cases the NumFOCUS affiliation is at the GitHub organization level rather than at the repo
                # level. So also allow match on repo owner
                if key == "github_name":
                    owner = args[key].split("/")[0].lower()
                    is_affiliated |= meta[key].lower() == owner
    return {
        "num_contributors": None,
        "amount_received_usd": None,
        "is_affiliated": is_affiliated,
        "type": "numfocus",
    }


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
    stats = get_funding_stats(vars(args))
    print(stats)
