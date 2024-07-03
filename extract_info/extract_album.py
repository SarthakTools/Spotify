import eyed3, re

def get_album(file_path):
    try:
        audio_file = eyed3.load(file_path)

        if audio_file.tag.album:
            filtered_text = re.sub(r'\[[^\]]*\]', '', audio_file.tag.album)
            return filtered_text
        else:
            return None
    except Exception as e:
        return f"Error : {e}"