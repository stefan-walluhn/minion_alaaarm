class Frame:
    KEEP_ALIVE = b'#'
    NEW_MESSAGE = b'!'
    RELOAD = b'R'
    ERROR = b'E'
    ANOTHER_SESSION = b'A'


def frame_to_str(frame):
    frames = {
        Frame.KEEP_ALIVE: 'KEEP ALIVE',
        Frame.NEW_MESSAGE: 'NEW MESSAGE',
        Frame.RELOAD: 'RELOAD',
        Frame.ERROR: 'ERROR',
        Frame.ANOTHER_SESSION: 'ANOTHER SESSION'
    }

    return frames[frame]
