import json
import easyocr

reader = easyocr.Reader(['en'])
result = reader.readtext('/home/kailash/table_detection/test/batch0_a5ea3691-aa9f-4ed7-978b-70ee8c4b885a_1.jpg')
words = []

for _, word in enumerate(result):
    bbox_raw = word[0]
    bbox = [bbox_raw[0][0], bbox_raw[0][1], bbox_raw[2][0], bbox_raw[2][1]]
    text = word[1]
    words.append({"text": text, "bbox": bbox})

with open("test/image_words.json", "w") as file:
    json.dump(words, file, default=int)