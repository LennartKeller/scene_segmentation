import json
from pathlib import Path
from nltk.tokenize.punkt import PunktSentenceTokenizer
from tqdm.auto import tqdm


LANGUAGE = "german"
SRC_PATH = Path("/home/keller/Uni/perry-rhodan-summarization/data/novells/")
DST_PATH = Path("data/test/")

def make_preparation_func():
    sent_tokenizer = PunktSentenceTokenizer()
    def prepare_novel(text):
        text = " ".join(text.split())
        sentences = [
            {"begin": begin_idx, "end": end_idx}
            for begin_idx, end_idx in sent_tokenizer.span_tokenize(text)
            ]
        data = { 
            "text": text,
            "sentences": sentences,
            "scenes": [{"begin": 25, "end": 1423, "type": "Scene"}] # dummies...
        }
        return data


if __name__ == "__main__":
    prepare_novel = make_preparation_func()
    novels = SRC_PATH.glob("*.txt")
    for novel in novels:
        text = novel.read_text()
        data = prepare_novel(text)
        dest_file = DST_PATH / f"{novel.stem}.json"
        with dest_file.open("w") as f:
            json.dump(data, f, indent=4)
