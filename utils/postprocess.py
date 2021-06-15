import itertools
import json
import os

import jsonlines
import sys
from preprocess import test_file


def read_jsonlines(file_path):
    content = []
    with jsonlines.open(file_path) as f:
        for line in f.iter():
            content.append(line)
    return content


if __name__ == "__main__":
    pred_file_path = sys.argv[1] # "data/predictions/{}.pred".format(test_file)
    out_file = pred_file_path.replace(".pred","")
    raw_data = "/home/murathan/Desktop/scene-segmentation/json" if "home/" in os.getcwd() else "/cephyr/users/murathan/Alvis/scene-segmentation/json"

    original_file_path = "{}/{}".format(raw_data, test_file)

    original_file = json.load(open(original_file_path))
    pred = read_jsonlines(pred_file_path)
    labels = list(itertools.chain(*[line["labels"] for line in pred]))
    indicies = [(line["begin"], line["end"]) for line in original_file["sentences"]]
    scenes = []
    labels = list(zip(labels, indicies))
    group = {}
    last_border = 0
    for i, label_offset in enumerate(labels):
        label, offset = label_offset[0].replace("_label", ""), label_offset[1]
        if i == 0:
            prev_l = label.replace("-B", "")
            group = [offset]
        else:
            if "-B" in label:
                # Non-scene to non-scene change is not allowed so continue expanding last non-scene despite
                # prediction of Nonscene-B label
                if label == "Nonscene-B" and prev_l == "Nonscene":
                    group.append(offset)
                else:  # scene change due to prediction of -B label
                    scenes.append({"begin": last_border, "end": group[-1][-1], "type": prev_l})
                    group = [offset]
                    last_border = scenes[-1]["end"]
                    prev_l = label.replace("-B", "")
            else:
                if label == prev_l:
                    group.append(offset)
                else:  # scene change despite lack of -B label
                    scenes.append({"begin": last_border, "end": group[-1][-1], "type": prev_l})
                    group = [offset]
                    last_border = scenes[-1]["end"]
                    prev_l = label.replace("-B", "")
    print(scenes)
    output = {"text": original_file["text"], "scenes": scenes}

    json.dump(output, open(out_file, "w"))
