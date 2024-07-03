import eyed3

def get_artist(file_path):
    try:
        audio_file = eyed3.load(file_path)

        if audio_file.tag.artist:
            return audio_file.tag.artist
        else:
            return None
    except Exception as e:
        return f"Error : {e}"