# pip install textrank4zh --user
from textrank4zh import TextRank4Keyword, TextRank4Sentence

tr4s = TextRank4Sentence()

def digest(text, result_len = 3):
    tr4s.analyze(text = text, lower = True, source = 'all_filters')
    digest_result = tr4s.get_key_sentences(num = result_len)
    digest_index = []
    digest_sentence = []
    digest_passage = ''
    for item in digest_result:
        digest_index.append(item.index)
        digest_sentence.append(item.sentence)
        digest_passage += item.sentence
    return digest_index, digest_sentence