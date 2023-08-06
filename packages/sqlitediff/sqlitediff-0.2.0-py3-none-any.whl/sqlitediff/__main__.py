import sys

import argparse

from sqlitediff.Controller import Controller
from sqlitediff.diff.SqliteDiff import SqliteDiff
from sqlitediff.print.Printer import Printer

def main(args_=None):
    """The main routine."""
    if args_ is None:
        args_ = sys.argv[1:]

    parser = argparse.ArgumentParser()
    parser.add_argument("--pathBefore", "-b", type=str, required=True, help="Path to sqlite file before action")
    parser.add_argument("--pathAfter", "-a", type=str, required=True, help="Path to sqlite file after action")
    parser.add_argument("--primaryKey", "-p", type=str, default="rowid", help="Name of the primary key column")
    args = parser.parse_args()

    ctrl = Controller(args.pathBefore, args.pathAfter)
    ctrl.printHeader()
    
    diff = SqliteDiff(args.primaryKey, args.pathBefore, args.pathAfter)
    tableResult = diff.processTables()

    printer = Printer()
    printer.print(tableResult)

 #   printer.printSnapshot(diff.afterSnapshot)

    ctrl.printExecutionTime()

if __name__ == "__main__":
    sys.exit(main())
