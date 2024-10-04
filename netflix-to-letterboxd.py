import pandas as pd
import argparse
import os
import time
import requests

def converter(args):
    input_filepath = args.input if args.input is not None else os.path.join(os.getcwd(), "NetflixViewingHistory.csv")
    output_filepath = args.input if args.output is not None else os.path.join(os.getcwd(), f"Netflix to Letterboxd export ({time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})")
    if not os.path.isfile(input_filepath):
        raise ValueError(f"Input file {input_filepath} not found.")
    if not os.access(os.path.dirname(input_filepath), os.R_OK):
        raise ValueError(f"File path {input_filepath} exists but is not readable.")

    if os.path.exists(output_filepath):
        raise ValueError(f"File {output_filepath} already exists, and will not be overwritten.")
    if not os.access(os.path.dirname(output_filepath), os.W_OK):
        raise ValueError(f"Cannot write to file {output_filepath}.")

    df = pd.read_csv(input_filepath)

    df["Title"] = df["Title"].str.replace("\"\"", "")
    try:
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=True).dt.strftime("%Y-%m-%d") 
    except pandas._libs.tslibs.parsing.DateParseError:
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=False).dt.strftime("%Y-%m-%d")
    except pandas._libs.tslibs.parsing.DateParseError:
        raise ValueError("Could not parse date column. Please ensure that the date column is in a format that pandas can parse.")
    df = df[~df.Title.str.contains(r": Season \d+: ")]

    with open("titles.txt", "r") as file:
        titles_to_remove = [line.strip() for line in file]

    for title in titles_to_remove:
        df = df[~df.Title.str.contains(rf"{title}")]

    df = df.rename(columns={"Date": "WatchedDate"})
    
    df.to_csv(output_filepath, index=False)

    print(f"Exported {len(df)} entries to {output_filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser("netflix-to-letterboxd")
    parser.add_argument("--input", help="The file path to read (optional, searches for an appropriately named file in the working directory by default)", type=str)
    parser.add_argument("--output", help="The file path to write to (optional, writes to the working directory by default)", type=str)
    args = parser.parse_args()
    converter(args)

