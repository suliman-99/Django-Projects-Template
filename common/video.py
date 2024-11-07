import cv2


def get_video_duration_in_seconds(filename):
    video = cv2.VideoCapture(filename)
    if not video.isOpened():
        return None
    total_frames = video.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = video.get(cv2.CAP_PROP_FPS)
    if fps > 0:
        duration = total_frames / fps
    else:
        return None
    video.release()
    return duration
