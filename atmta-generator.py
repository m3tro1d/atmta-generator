import argparse
import ffmpeg
import os


def get_name(filename):
    """Returns file's name w/o extension"""
    return ".".join(filename.split(".")[:-1])


def get_ext(filename):
    """Returns file's extension"""
    return filename.split(".")[-1]


def output_name(filename):
    """Returns a nicely formatted output filename"""
    return "{}-{}flipped.{}".format(get_name(filename),
                                    side,
                                    get_ext(filename))


def parse_arguments():
    """Processes input arguments"""
    parser = argparse.ArgumentParser(
        description="""This script is (pretty much useless) generates ATMTA
        pictures, flipped by the specified side.""")
    parser.add_argument("SIDE",
                        choices=["right", "left"],
                        help="image will be flipped with this side")
    parser.add_argument("FILE",
                        help="name of the picture file")
    return parser.parse_args()


def process_file(filename, side):
    """Processes the file using the specified side"""
    in_file = ffmpeg.input(filename)
    overlay_file = ffmpeg.input(filename)

    if side == "right":
        # Prepare the overlay
        overlay = (
            ffmpeg
            .hflip(overlay_file)
            .filter('crop', 'iw/2', 'ih', '0', '0')
        )
        # Join the files
        (
            ffmpeg
            .overlay(in_file, overlay)
            .output(output_name(filename))
            .run()
        )
    elif side == "left":
        # Prepare the overlay
        overlay = (
            ffmpeg
            .hflip(overlay_file)
            .filter('crop', 'iw/2', 'ih', 'iw/2', '0')
        )
        # Join the files
        (
            ffmpeg
            .overlay(in_file, overlay, x="main_w/2")
            .output(output_name(filename))
            .run()
        )



def main():
    """Entry point of the script"""
    # Parse the input parameters
    args = parse_arguments()
    side = args.SIDE
    filename = args.FILE
    # Process the file
    process_file(filename, side)


# Entry point
if __name__ == "__main__":
    main()
