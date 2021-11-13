def frame_filter(frame, handler):
    def _filter(frm):
        if frm == frame:
            handler(frm)

    return _filter
