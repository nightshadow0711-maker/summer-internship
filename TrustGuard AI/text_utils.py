import re

def text_stats(text):
    words=re.findall(r"\b[\w'-]+\b",text)
    sentences=[x for x in re.split(r"[.!?]+",text) if x.strip()]
    paragraphs=[x for x in re.split(r"\n\s*\n",text) if x.strip()]
    return {
        "words":len(words), "characters":len(text),
        "characters_no_spaces":len(re.sub(r"\s","",text)),
        "sentences":len(sentences), "paragraphs":len(paragraphs),
        "reading_time":max(1,round(len(words)/200))
    }
