import json
from pathlib import Path


SRC_PATH = Path("/home/keller/Uni/perry-rhodan-summarization/data/novells/1.txt")
DST_PATH = Path("data/test/Perry1.json")

if __name__ == "__main__":
    text = SRC_PATH.read_text()
    with DST_PATH.open("w") as f:
        data = {
            "text": " ".join(text.split()),
            "scenes": [{"begin": 25, "end": 1423, "type": "Scene"}]
        }
        json.dump(data, f)
