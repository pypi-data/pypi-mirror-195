def get_duration(file):
    try:
        import audioread
        with audioread.audio_open(file) as f:
            return f.duration
    except:
        pass

    return 0
