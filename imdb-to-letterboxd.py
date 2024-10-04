import pandas as pd
import argparse
import os
import time
import requests
import sys

def converter(args):
    if args.input is None:
        raise ValueError("Please provide an input file.")
    if not args.input.endswith('.csv'):
        raise ValueError("Input file must be a CSV file.")
    
    list_name = args.input.removesuffix('.csv')
    
    input_filepath = f"{list_name}.csv"
    output_filepath = os.path.join(os.path.abspath(os.getcwd()), args.output if args.output is not None else f"IMDb {list_name} to Letterboxd export ({time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())})")
    
    if not os.path.isfile(input_filepath):
        raise ValueError(f"Input file {input_filepath} not found.")
    if not os.access(os.path.dirname(os.path.abspath(input_filepath)), os.R_OK):
        raise ValueError(f"File path {input_filepath} exists but is not readable.")

    if os.path.exists(output_filepath):
        raise ValueError(f"File {output_filepath} already exists, and will not be overwritten.")
    if not os.access(os.path.dirname(os.path.abspath(output_filepath)), os.W_OK):
        raise ValueError(f"Cannot write to file {output_filepath}.")

    df = pd.read_csv(input_filepath)

    df = df[df['Title Type'].str.lower().str.contains('movie')]

    column_list = ['Your Rating', 'Title', 'Year', 'Directors', 'Const']
    if args.keep_dates:
        column_list.append('Date Rated')
        df = df.rename(columns={"Date Rated": "WatchedDate"})

    df = df[column_list]
    
    df.Year = df.Year.astype('Int64')
    df = df.rename(columns={"Your Rating": "Rating10", "Const": "imdbID"}) 
    
    df.to_csv(output_filepath, index=False)

    print(f"Exported {len(df)} entries to {output_filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser("netflix-to-letterboxd")
    parser.add_argument("--input", help="The input file to read", type=str)
    parser.add_argument("--output", help="The directory to write to (optional, writes to the working directory by default)", type=str)
    parser.add_argument("--keep-dates", help="Keep the dates from the input file as the log dates", action="store_true")
    if len(sys.argv) == 1:
        parser.print_help()
        exit(0)
    args = parser.parse_args()
    converter(args)

