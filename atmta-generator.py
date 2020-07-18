import argparse
import ffmpeg
import os


# Parse the input parameters
parser = argparse.ArgumentParser(
	description="""This script is (pretty much useless) generates ATMTA pictures, flipped by the specified side.""")

parser.add_argument("SIDE", choices=["right", "left"],
	help="image will be flipped with this side")

parser.add_argument("FILE",
	help="file name of the picture")

args = parser.parse_args()
side = args.SIDE
filename = args.FILE


# Process the specified file with ffmpeg
