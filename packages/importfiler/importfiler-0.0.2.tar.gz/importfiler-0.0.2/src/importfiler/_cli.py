import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "module_name",
        help="Module to profile. ex: 'json'.",
    )
    parser.add_argument(
        "--unit",
        choices=["%", "s", "ms", "us"],
        default="%",
    )
    parser.add_argument(
        "--mode",
        choices=["all_modules", "dependencies"],
        default="dependencies",
    )
    return parser.parse_args()
