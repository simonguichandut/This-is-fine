import os
import sys

def save():
    # os.system("ffmpeg -r 24 -i png/%06d.png -vcodec mpeg4 -y movie.mp4")
    # os.system("ffmpeg -r 24 -i curve/%06d.png -vcodec mpeg4 -y curve.mp4")
    os.system("ffmpeg -r 24 -i png/%06d.png movie.gif")
    os.system("ffmpeg -r 24 -i curve/%06d.png curve.gif")

if __name__ == "__main__":
    save()