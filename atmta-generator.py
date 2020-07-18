import argparse
import ffmpeg
import os


# Parse the input parameters
parser = argparse.ArgumentParser(
	description="""This script is (pretty much useless) generates ATMTA pictures, flipped by the specified side.""")

args = parser.parse_args()

# Process the specified file with ffmpeg
