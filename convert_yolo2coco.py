import os
import json
from PIL import Image
from constants import label_tatr, labels_yolo,categories



def convert_yolo_coco(image_dir,annot_dir,output_dir,train_ratio=.8):
    

    if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    image_files = os.listdir(image_dir)

    num_train = int(len(image_files) * train_ratio)
    train_files = image_files[:num_train]
    valid_files = image_files[num_train:]

    for split, files in [('train', train_files), ('val', valid_files)]:
        split_dir = os.path.join(output_dir, split)
        os.makedirs(split_dir, exist_ok=True)
        coco_dataset = {
                        "images":[],
                        "categories": categories,
                        "annotations": []
                    }
        for id,image_file in enumerate(files):
            image_path = os.path.join(image_dir, image_file)
            os.system(f'cp {image_dir}/{image_file} {split_dir}/{id}.jpg')
            image = Image.open(image_path)
            width, height = image.size
            image_dict = {"id":id,
                        "file_name":f"{id}.jpg",
                        "width": width,
                        "height":height}
            
            coco_dataset["images"].append(image_dict)

            with open(os.path.join(annot_dir,f'{image_file.split(".")[0]}.txt')) as f:
                annotations = f.readlines()

            for ann in annotations:
                x, y, w, h = map(float, ann.strip().split()[1:])
                x_min, y_min = int((x - w / 2) * width), int((y - h / 2) * height)
                x_max, y_max = int((x + w / 2) * width), int((y + h / 2) * height)
                yolo_cat = ann.strip().split()[0]
                cat = [label_tatr[k] for k,v in labels_yolo.items() if v == int(yolo_cat)]
                ann_dict = {
                    "id": len(coco_dataset["annotations"]),
                    "image_id": id,
                    "category_id": cat[0],
                    "bbox": [x_min, y_min, x_max - x_min, y_max - y_min],
                    "area": (x_max - x_min) * (y_max - y_min),
                    "iscrowd": 0
                }
                coco_dataset["annotations"].append(ann_dict)
                
        with open(os.path.join(output_dir, f'{split}/custom_{split}.json'), 'w') as f:
            json.dump(coco_dataset, f)
    


if __name__=="__main__":
    image_path = "dataset/images"
    annotation_path = "dataset/labels"
    ouput_dir = "coco_dataset/"
    convert_yolo_coco(image_path,annotation_path,ouput_dir)