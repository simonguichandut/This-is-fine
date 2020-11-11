import os
import sys

def save(format):
    if format == 'mp4':
        if os.path.exists('./box/'):
            os.system("ffmpeg -r 15 -i box/%06d.png -vcodec mpeg4 -y box.mp4")
        if os.path.exists('./curve/'):
            os.system("ffmpeg -r 15 -i curve/%06d.png -vcodec mpeg4 -y curve.mp4")
    elif format == 'gif':
        if os.path.exists('./box/'):
            os.system("ffmpeg -i box/000100.png -vf palettegen=16 palette.png")
            os.system("ffmpeg -i box/%06d.png -i palette.png -filter_complex 'fps=15,scale=720:-1:flags=lanczos[x];[x][1:v]paletteuse' box.gif")
            os.system("rm palette.png")
        if os.path.exists('./curve/'):
            os.system("ffmpeg -i curve/000100.png -vf palettegen=16 palette.png")
            os.system("ffmpeg -i curve/%06d.png -i palette.png -filter_complex 'fps=15,scale=720:-1:flags=lanczos[x];[x][1:v]paletteuse' curve.gif")
            os.system("rm palette.png")

# command line call : python3 make_movies.py mp4 gif
if __name__ == "__main__":
    if len(sys.argv) >= 2:
        for format in sys.argv[1:]:

            if format not in ('gif','mp4'):
                sys.exit('video format not supported')

            save(format)

    else:
        save('mp4') # default format