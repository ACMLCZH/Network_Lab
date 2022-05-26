# pip install textrank4zh --user
from textrank4zh import TextRank4Keyword

tr4w = TextRank4Keyword()

def keyword(text, keywords_num = 5):
	tr4w.analyze(text = text, lower = True, window = 2)
	keywords = []
	for item in tr4w.get_keywords(keywords_num, word_min_len = 1):
		keywords.append(itesm.word)
	return keywords