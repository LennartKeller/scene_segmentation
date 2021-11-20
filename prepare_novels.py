import json
import re
from pathlib import Path
from nltk import sent_tokenize
from tqdm.auto import tqdm
from textspan import get_original_spans
from more_itertools import flatten

LANGUAGE = "german"
SRC_PATH = Path("/home/keller/Uni/perry-rhodan-summarization/data/novells/")
DST_PATH = Path("data/test/")



def prepare_novel(text):
    
    # Ugly hack
    # texts = re.split(r'^1\.\n', text, flags=re.MULTILINE)
    # if len(texts) > 1:
    #     text = " ".join(texts[1:])
    # else:
    #     text = texts[0]
    text = " ".join(text.split())
    sentences = [
        {"begin": begin_idx, "end": end_idx}
        for begin_idx, end_idx in flatten(get_original_spans(sent_tokenize(text, language=LANGUAGE), text))
    ]
    data = { 
        "text": text,
        "sentences": sentences,
        "scenes": [{"begin": 0, "end": len(text)-1, "type": "Scene"}] # one scene to rule them all...
    }
    return data


if __name__ == "__main__":
    novels = list(SRC_PATH.glob("*.txt"))
    for novel in tqdm(novels):
        text = novel.read_text()
        data = prepare_novel(text)
        dest_file = DST_PATH / f"{novel.stem}.json"
        with dest_file.open("w") as f:
            json.dump(data, f, indent=4)
