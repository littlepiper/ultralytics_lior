import os

IMAGE_EXT = [".jpg", ".jpeg", ".webp", ".bmp", ".png"]
VIDEO_EXT = [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv", ".mpeg", ".mpg", ".m4v", ".qt"]
ANNOTATION_EXT = [".txt", ".xml", ".json"]

def get_file_list(path, valid_exts):
    file_names = []
    for maindir, subdir, file_name_list in os.walk(path):
        for filename in file_name_list:
            apath = os.path.join(maindir, filename)
            ext = os.path.splitext(apath)[1]
            if ext in valid_exts:
                file_names.append(apath)
    return file_names

def get_image_list(path):
    return get_file_list(path, IMAGE_EXT)

def get_video_list(path):
    return get_file_list(path, VIDEO_EXT)

def get_json_list(path):
    return get_file_list(path, [".json"])

def get_xml_list(path):
    return get_file_list(path, [".xml"])

