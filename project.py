# Adjusted Cost Basis Calculator Final Project CS50

# Import libraries
import sys
import pandas as pd

# Although openpyxl was not explicitly used, it was an engine in pd.to_excel
import openpyxl
import argparse
from functools import partial
import re


def main():
    """
    Convert's Questrade CSV to aggregated pivot tables, calculates Adjusted Cost Basis of each symbol,
    and writes to .xlsx file if the user wishes

    :param name: filepath to csv file
    :type name: str
    :raise SystemExit: If filepath not found
    :return: An optional xlsx file if user prompted
    :rtype: xlsx file
    """
    # Must have atleast one system argument
    if len(sys.argv) < 2:
        sys.exit("Invalid Arguments")
    else:
        # Generate Parser Object
        parser = argparse.ArgumentParser(
            prog="Adjusted Cost Basis Calculator",
            description="Calculates Adjusted Cost Basis of each symbol from Questrade's Account Activity csv",
        )
        # Add filepath argument
        parser.add_argument("filename", type=str, help="filepath to csv input file")
        # Add csv argument
        parser.add_argument(
            "-x",
            "--xlsx",
            type=bool,
            default=0,
            help="If true, prints to xlsx",
        )
        # Add name argument
        parser.add_argument(
            "-n",
            "--name",
            type=str,
            default="Adjusted_Cost_Basis.xlsx",
            help="Specify the name of the output xlsx file",
        )
        # Add space argument
        parser.add_argument(
            "-s",
            "--space",
            type=int,
            default=3,
            help="Specify the space between the columns of the printed pivot table",
        )
        # Parse arguments
        args = parser.parse_args()
        # Read CSV into processed dict
        df = csv_to_dict(args.filename)
        # Get unique account #'s
        unique_acc = pd.unique(df["Account #"])
        # Loop through each unique account #
        for acc in unique_acc:
            # Create filtered dataframe for each account #
            new_df = df.loc[
                (
                    # Store only account's respective trades and dividend reinvestments,
                    (df["Account #"] == acc)
                    & (
                        (df["Activity Type"] == "Trades")
                        | (df["Activity Type"] == "Dividend reinvestment")
                    )
                ),
                [
                    # Storing the Account #, Account Type, Symbol, Activity Type, Quantity, Net Amount, and Currency
                    "Account #",
                    "Account Type",
                    "Symbol",
                    "Activity Type",
                    "Quantity",
                    "Net Amount",
                    "Currency",
                ],
            ]
            # Convert filtered dataframe to Pivot Table
            table_new_df = pivot_acc(new_df)
            # Print filtered dataframe with specified spaces
            print(add_space(table_new_df, args.space))
            # If user prompted a xlsx file
            if args.xlsx:
                # Print current dataframe to a sheet on final xlsx file
                print_xlsx(table_new_df, args, acc)


def csv_to_dict(file: str):
    """
    Convert's Questrade CSV to Dictionary and remove ".TO" to standardize symbols

    :param file: filepath to csv file
    :type file: str
    :raise SystemExit: If filepath not found, has no columns, or invalid keys
    :return: A dataframe with the original columns and symbol names standardized
    :rtype: dataframe object
    """
    if (
        re.search(
            r"^.*(\.csv)$",
            file.lower().strip(),
        )
        == None
    ):
        sys.exit("Invalid file")
    else:
        # If ".csv" is found at end of the string
        try:
            # Read csv into Pandas dataframe
            df = pd.read_csv(file.strip())
        except FileNotFoundError:
            # If file not found, exit
            sys.exit("File not found, or invalid filepath")
        except pd.errors.EmptyDataError:
            # If file has no columns
            sys.exit("File has no columns")
        try:
            # Create copy of symbols column
            symbol_col = df["Symbol"]
        except KeyError:
            # If invalid keys
            sys.exit("Invalid or unsupported keys in csv")
        # Remove .TO from Symbols
        cleaned_col = symbol_col.str.replace(r"(\.TO)", "", regex=True)
        # Update Symbol column in main dataframe
        df["Symbol"].update(cleaned_col)
        # Return Dataframe
        return df


def pivot_acc(new_df):
    """
    Converts dataframe to a pivot table, removes net quantities of zero, and formats data to be readable to user

    :param new_df: Dataframe to pivot
    :type new_df: dataframe object
    :raise SystemExit: If invalid data type was passed in "Net Amount" and/or "Quantity" column
    :return: A dataframe with the aggregated data
    :rtype: dataframe object
    """
    # Convert into pivot table
    table_new_df = pd.pivot_table(
        new_df,
        values=["Quantity", "Net Amount"],
        index=["Account #", "Account Type", "Symbol", "Currency"],
        aggfunc={"Quantity": "sum", "Net Amount": "sum"},
    )
    # Flip the sign of "Net Amount", since buying is considered negative
    table_new_df["Net Amount"] = table_new_df["Net Amount"] * -1
    try:
        # Add column of Adjusted Cost Basis calculation
        table_new_df["Adjusted Cost Basis"] = table_new_df["Net Amount"] / table_new_df["Quantity"]
    except TypeError:
        # If value is not an int
        sys.exit('Invalid integer in "Net Amount" or "Quantity" column')
    # Map $1,234.56 format to "Net Amount" and "Adjusted Cost Basis"
    table_new_df["Net Amount"] = table_new_df["Net Amount"].map("${:,.2f}".format)
    table_new_df["Adjusted Cost Basis"] = table_new_df["Adjusted Cost Basis"].map("${:,.2f}".format)
    # Map "Quantity" to a comma separated int
    table_new_df["Quantity"] = table_new_df["Quantity"].map("{:,.0f}".format)
    # Remove values with quantity 0
    table_new_df = table_new_df[(table_new_df["Quantity"] != "0")]
    # Return pivot table
    return table_new_df


def print_xlsx(table_new_df, args, acc):
    """
    Prints each account dataframe to a .xlsx file separated by sheets.

    :param table_new_df: Dataframe to write onto xlsx
    :type table_new_df: dataframe object
    :param args: Name of the xlsx file
    :type args: str
    :param acc: Unique account #'s
    :type acc: str
    """
    try:
        # Append to existing xlsx with sheet name as the account #
        with pd.ExcelWriter(
            args.name,
            mode="a",
            if_sheet_exists="new",
            engine="openpyxl",
        ) as writer:
            table_new_df.to_excel(writer, sheet_name=str(acc))
    # If file not found
    except FileNotFoundError:
        # Write to new xlsx file
        table_new_df.to_excel(args.name, sheet_name=str(acc))


def fmt_string(x: str, fill):
    """
    Formats the message with the desired fill

    :param x: The string you want to format
    :type x: str
    :param fill: Specified format
    :type fill: int
    :return: A formatted string
    :rtype: str
    """
    return "{message: >{fill}}".format(message=x, fill=fill)


def add_space(df, n: int):
    """
    Adds spaces between columns in inputted dataframe

    :param df: Dataframe to put spaces in between
    :type df: dataframe object
    :param n: Number of spaces you want to add in between columns
    :type n: int
    :return: A formatted dataframe with the specified number of columns
    :rtype: dataframe object
    """
    # Find max character length per column
    c_max = df.astype(str).agg(lambda x: x.str.len()).max()
    # Amount of space you want between columns
    space = n
    # Create empty dictionary
    fmts = {}
    # Loop through each column and strings inside column
    for idx, c_len in c_max.items():
        # Deal with MultIndex tuples or simple string labels.
        if isinstance(idx, tuple):
            # If tuple, get max length string
            lab_len = max([len(str(x)) for x in idx])
        else:
            # If simple string, get max length string
            lab_len = len(str(idx))
        fill = max(lab_len, c_len) + space - 1
        fmts[idx] = partial(fmt_string, fill=fill)
    # Return formatted dataframe with spaces
    return df.to_string(formatters=fmts)


# Call main only if explicitly called
if __name__ == "__main__":
    main()
