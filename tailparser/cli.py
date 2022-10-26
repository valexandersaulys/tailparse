import argparse
from tailparser.logparser import logparse


def cli():
    logparse(argparse.ArgumentParser(description="Process some SQL"))
