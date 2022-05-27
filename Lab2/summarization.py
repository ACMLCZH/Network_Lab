# pip install textrank4zh --user
from textrank4zh import TextRank4Keyword, TextRank4Sentence

tr4w = TextRank4Keyword()
tr4s = TextRank4Sentence()


def keyword(text, keywords_num=5):
    tr4w.analyze(text=text, lower=True, window=2)
    keywords = []
    for item in tr4w.get_keywords(keywords_num, word_min_len=1):
        keywords.append(item.word)
    return keywords


def keyphrase(text, keywords_num=3):
    tr4w.analyze(text=text, lower=True, window=2)
    keyphrases = []
    for phrase in tr4w.get_keyphrases(keywords_num, min_occur_num=2):
        keyphrases.append(phrase)
    return keyphrases


def digest(text, result_len=3):
    tr4s.analyze(text=text, lower=True, source='all_filters')
    digest_result = tr4s.get_key_sentences(num=result_len)
    digest_index = []
    digest_sentence = []
    digest_passage = ''
    for item in digest_result:
        digest_index.append(item.index)
        digest_sentence.append(item.sentence)
        digest_passage += item.sentence
    return digest_index, digest_sentence
