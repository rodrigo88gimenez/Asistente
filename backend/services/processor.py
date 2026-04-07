def process_file(path, content_type):
    return read_text(path)


def read_text(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return "[Archivo no legible como texto]"