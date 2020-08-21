
from cv2 import VideoWriter, VideoWriter_fourcc, imread
from flask import Flask, send_file, send_from_directory

app = Flask(__name__)
# Image of heart at rest (non-beat frames).
small = imread('small-heart.png')
# Image of heart beating (beat frames).
large = imread('large-heart.png')
# Dimensions of video frame.
height = width = 1080
# Video title.
title = lambda x: 'heartbeat-video(%dBPM).mp4' % x
# Define MP4 video codec.
fourcc = VideoWriter_fourcc(*'mp4v')


def get_frame_rates(tempo):
    """
    Given a 4/4 tempo in beats per minute, return the optimal frame rate and frames per beat.
    """
    frames_per_second = -1
    frames_per_beat = -1
    sync_error = 1

    for fps in range(10, 31):
        fpb = (fps * 60.0) / tempo
        rounded_fpb = round(fpb)
        err = abs(rounded_fpb - fpb)
        if err < sync_error and rounded_fpb > 2:
            frames_per_second = fps
            frames_per_beat = rounded_fpb
            sync_error = err

    return frames_per_second, frames_per_beat


def create_video(tempo):
    """
    Create heartbeat animation synced to given tempo.
    """
    fps, fpb = get_frame_rates(tempo)
    print("Frames per second: ", fps)
    print("Frames per beat: ", fpb)

    # OpenCV video object to write frames to.
    output_video = VideoWriter(title(tempo), fourcc, fps, (height, width))

    # Create a minute-length animation.
    for i in range(fps * 60):
        if i % fpb == 0:
            output_video.write(large)
        else:
            output_video.write(small)

    output_video.release()
    return title(tempo)


@app.route('/')
def index():
    return 'This is the home page.'


@app.route('/<int:tempo>')
def get_video(tempo):
    return 'Creating a video with a heartbeat tempo of %d BPM' % tempo


if __name__ == '__main__':
    app.run(debug=True)
