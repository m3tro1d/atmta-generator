# atmta-generator
This little script generates ATMTA-like pictures via ffmpeg.

## Requirements
- Python 3
- [ffmpeg-python](https://github.com/kkroening/ffmpeg-python)

## Usage
```
atmta-generator.py [-h] {right,left} FILE

positional arguments:
  {right,left}  image will be flipped with this side
  FILE          file name of the picture

optional arguments:
  -h, --help    show this help message and exit
```

By the default, the output files will be placed in the same directory as the original file.

## Example
Original:

![Original image](example/original.jpg?raw=true)

Right-flipped:

![Right-flipped image](example/original-rightflipped.jpg?raw=true)

Left-flipped:

![Left-flipped image](example/original-leftflipped.jpg?raw=true)
