import argparse
from tailparse.logparser import logparse


def cli():
    logparse(argparse.ArgumentParser(description="Process logs as if they were SQL."))
