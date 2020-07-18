import argparse
import ffmpeg
import os


def get_name(filename):
	"""Returns file's name w/o extension"""
	return ".".join(filename.split(".")[:-1])


def get_ext(filename):
	"""Returns file's extension"""
	return filename.split(".")[-1]


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


# Process the specified file
in_file = ffmpeg.input(filename)
overlay_file = ffmpeg.input(filename)
# Prepare the overlay
(
	overlay_file
	.hflip()
	.filter('crop', 'iw/2', 'ih', '0', '0')
)
# Join the files
(
	in_file
	.overlay(overlay_file)
	.output("{}-{}flipped.{}", get_name(filename), side, get_ext(filename)).
	run()
)
