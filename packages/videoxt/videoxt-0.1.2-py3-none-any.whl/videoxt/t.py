from videoxt.extractors import VideoToGIF, VideoToImages


vtg = VideoToGIF(
    "W:\\Libraries\\Videos\\video.mp4",
    start_time=20,
    stop_time=22,
    bounce=True,
).create_gif()
