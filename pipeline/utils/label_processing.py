def get_single_label_infos(annotation_infos, label):
    infos, image_info = annotation_infos
    face_infos = []
    for info in infos:
        if info[0] == label:
            face_infos.append(info)
    return face_infos


def get_face_infos(annotation_infos):
    return get_single_label_infos(annotation_infos, "face")


def get_face_box(face_infos, mode="largest"):
    if mode == "largest":
        face_info = max(face_infos, key=lambda x: (x[1][2] - x[1][0]) * (x[1][3] - x[1][1]))
    elif mode == "left":
        face_info = min(face_infos, key=lambda x: x[1][0])
    elif mode == "right":
        face_info = max(face_infos, key=lambda x: x[1][2])
    
    return face_info[1]


def get_face_box_from_annotation(annotation_infos, mode="largest"):
    face_infos = get_face_infos(annotation_infos)
    return get_face_box(face_infos, mode)


def expand_bbox(bbox, image_info, expand_ratio=0.7, offset_x=0, offset_y=0):
    x1, y1, x2, y2 = bbox
    w = x2 - x1
    h = y2 - y1
    cx = (x1 + x2) / 2
    cy = (y1 + y2) / 2

    pandding_side = max(w, h) * (expand_ratio + 0.5)

    x1 = max(0, cx - pandding_side + offset_x * pandding_side)
    y1 = max(0, cy - pandding_side + offset_y * pandding_side)
    x2 = min(image_info[1] - 1, cx + pandding_side + offset_x * pandding_side)
    y2 = min(image_info[2] - 1, cy + pandding_side + offset_y * pandding_side)

    if x1 == 0:
        x2 = min(image_info[1] - 1, pandding_side * 2)
    if y1 == 0:
        y2 = min(image_info[2] - 1, pandding_side * 2)
    if x2 == image_info[1] - 1:
        x1 = max(0, x2 - pandding_side * 2)
    if y2 == image_info[2] - 1:
        y1 = max(0, y2 - pandding_side * 2)

    x1 = round(x1)
    y1 = round(y1)
    x2 = round(x2)
    y2 = round(y2)
    
    return [x1, y1, x2, y2]