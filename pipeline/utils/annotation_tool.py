import os
import json

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from lxml.etree import Element, SubElement, tostring

def save_xanylabeling(save_path, info):
    data = dict(
        version="2.3.6",
        flags={},
        shapes=[],
        imagePath=info['file_name'],
        imageData=None,
        imageHeight=info['height'],
        imageWidth=info['width'],
    )
    for bbox_info in info['annotation']:
        x1, y1, x2, y2 = bbox_info[1]
        points = [
            [x1, y1],
            [x2, y1],
            [x2, y2],
            [x1, y2],
        ]
        score = bbox_info[2] if len(bbox_info) == 3 else None
        shape = {
                "label": bbox_info[0],
                "score": score,
                "description": "",
                "points": points,
                "group_id": None,
                "difficult": False,
                "shape_type": "rectangle",
                "flags": {},
            }
        data["shapes"].append(shape)
    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_xanylabeling(file_path):
    infos = []
    filename, width, height = None, None, None
    with open(file_path, 'r') as json_file:
        json_data = json.load(json_file)
        filename = json_data['imagePath']
        width = json_data['imageWidth']
        height = json_data['imageHeight']
        for shape in json_data['shapes']:
            label = shape['label']
            score = shape['score'] if shape.get('score') else None
            points = shape['points']
            x1, y1, x2, y2 = map(round, [points[0][0], points[0][1], points[2][0], points[2][1]])
            infos.append([label, [x1, y1, x2, y2], score])
    return infos, (filename, width, height)


def save_pascalvoc(save_path, info):
    node_root = Element('annotation')
    node_folder = SubElement(node_root, 'folder')
    node_filename = SubElement(node_root, 'filename')
    node_filename.text = info['file_name']
    node_source = SubElement(node_root, 'source')
    node_database = SubElement(node_source, 'database')
    node_database.text = "Unknown"
    node_annotation = SubElement(node_source, 'annotation')
    node_annotation.text = "Unknown"
    node_image = SubElement(node_source, 'image')
    node_image.text = "Unknown"
    node_size = SubElement(node_root, 'size')
    node_width = SubElement(node_size, 'width')
    node_width.text = str(info['width'])
    node_height = SubElement(node_size, 'height')
    node_height.text = str(info['height'])
    node_depth = SubElement(node_size, 'depth')
    node_segmented = SubElement(node_root, 'segmented')
    node_segmented.text = "0"
    for bbox_info in info['annotation']:
        x1, y1, x2, y2 = bbox_info[1]
        node_object = SubElement(node_root, 'object')
        node_name = SubElement(node_object, 'name')
        node_name.text = bbox_info[0]
        node_truncated=SubElement(node_object, 'truncated')
        node_truncated.text = '0'
        node_occluded = SubElement(node_object, 'occluded')
        node_occluded.text = '0'
        node_difficult = SubElement(node_object, 'difficult')
        node_difficult.text = '0'
        node_bndbox = SubElement(node_object, 'bndbox')
        node_xmin = SubElement(node_bndbox, 'xmin')
        node_xmin.text = str(x1)
        node_ymin = SubElement(node_bndbox, 'ymin')
        node_ymin.text = str(y1)
        node_xmax = SubElement(node_bndbox, 'xmax')
        node_xmax.text = str(x2)
        node_ymax = SubElement(node_bndbox, 'ymax')
        node_ymax.text = str(y2)
        node_attributes = SubElement(node_object, 'attributes')
        node_attribute = SubElement(node_attributes, 'attribute')
        node_name_ = SubElement(node_attribute, 'name')
        node_name_.text = "rotation"
        node_value_ = SubElement(node_attribute, 'value')
        node_value_.text = "0.0"
    data = tostring(node_root, pretty_print=True)
    file_object = open(save_path, 'wb')
    file_object.write(data)
    file_object.close()


def load_pascalvoc(file_path):
    infos = []
    tree = ET.parse(file_path)
    root = tree.getroot()
    filename = root.findall('filename')[0].text
    objects = root.findall('object')
    sizes = root.findall('size')
    width = sizes[0].findall('width')[0].text
    height = sizes[0].findall('height')[0].text
    assert int(width) != 0 and int(height) != 0
    for i in range(len(objects)):
        name = objects[i].findall('name')[0].text
        xmin = objects[i].findall('bndbox')[0].findall('xmin')[0].text
        ymin = objects[i].findall('bndbox')[0].findall('ymin')[0].text
        xmax = objects[i].findall('bndbox')[0].findall('xmax')[0].text
        ymax = objects[i].findall('bndbox')[0].findall('ymax')[0].text

        xmin = round(float(xmin))
        ymin = round(float(ymin))
        xmax = round(float(xmax))
        ymax = round(float(ymax))
        
        infos.append([name, [xmin, ymin, xmax, ymax], None])
        
    return infos, (filename, int(width), int(height))


def save_yolo(save_path, info):
    with open(save_path, "w") as f:
        for bbox_info in info['annotation']:
            x1, y1, x2, y2 = bbox_info[1]
            x_center = (x1 + x2) / 2.0 / info['width']
            y_center = (y1 + y2) / 2.0 / info['height']
            w = (x2 - x1) / info['width']
            h = (y2 - y1) / info['height']
            f.write(f"{bbox_info[0]} {x_center} {y_center} {w} {h}\n")


def load_yolo(file_path):
    infos = []
    filename, width, height = None, None, None
    with open(file_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split()
            label = line[0]
            x_center, y_center, w, h = map(float, line[1:])
            x1 = (x_center - w / 2) * width
            y1 = (y_center - h / 2) * height
            x2 = (x_center + w / 2) * width
            y2 = (y_center + h / 2) * height
            infos.append([label, [x1, y1, x2, y2], None])
    return infos, (filename, width, height)


SAVE_ANNOTATION = {
    '.json': save_xanylabeling,
    '.xml': save_pascalvoc,
    '.txt': save_yolo,
    }

LOAD_ANNOTATION = {
    '.json': load_xanylabeling,
    '.xml': load_pascalvoc,
    '.txt': load_yolo,
    }

def load_annotation(file_path):
    ext = os.path.splitext(file_path)[1]
    return LOAD_ANNOTATION[ext](file_path)

def save_annotation(save_path, info):
    ext = os.path.splitext(save_path)[1]
    SAVE_ANNOTATION[ext](save_path, info)