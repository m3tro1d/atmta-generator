from textwrap import dedent
import argparse
import os

try:
    import ffmpeg
except ImportError:
    print("'ffmpeg' module not found")
    sys.exit(1)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Classes
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

class CustomArgumentParser(argparse.ArgumentParser):
    """Override ArgumentParser's help message"""
    def format_help(self):
        help_text = dedent(f"""\
        ATMTA generator. Nuff said.

        Usage: {self.prog} SIDE FILE

        SIDE:
          Which side of the image is used for mirroring (right|left)

        FILE:
          Image to flip

        Options:
          -h,  --help     show help

        For more information visit:
        https://github.com/m3tro1d/atmta-generator
        """)
        return help_text

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Functions
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def get_name(filename):
    """Returns file's name w/o extension"""
    return ".".join(filename.split(".")[:-1])


def get_ext(filename):
    """Returns file's extension"""
    return filename.split(".")[-1]


def output_name(filename, side):
    """Returns a nicely formatted output filename"""
    return f"{get_name(filename)}-{side}flipped.{get_ext(filename)}"


def valid_file(string):
    """Converts the string to a valid file path"""
    path = os.path.abspath(string)
    if not os.path.exists(path):
        error = f"File does not exist: {path}"
        raise argparse.ArgumentTypeError(error)
    if not os.path.isfile(path):
        error = f"Not a file: {path}"
        raise argparse.ArgumentTypeError(error)
    return path


def parse_arguments():
    """Processes input arguments"""
    parser = CustomArgumentParser(usage="%(prog)s SIDE FILE")

    parser.add_argument("side", choices=["right", "left"])

    parser.add_argument("file", type=valid_file)

    args = parser.parse_args()
    return args


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
            .output(output_name(filename, side))
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
            .output(output_name(filename, side))
            .run()
        )

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Main script
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def main():
    """Main script"""
    process_file(args.filename, args.side)


# Entry point
if __name__ == "__main__":
    args = parse_arguments()

    try:
        main()
    except KeyboardInterrupt:
        print("\nUser interrupt", file=sys.stderr)
        sys.exit(1)
