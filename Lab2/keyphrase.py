# pip install textrank4zh --user
from textrank4zh import TextRank4Keyword

tr4w = TextRank4Keyword()

def keyphrase(text, keywords_num = 3):
	tr4w.analyze(text = text, lower = True, window = 2)
	keyphrases = []
	for phrase in tr4w.get_keyphrases(keywords_num, min_occur_num = 2):
		keyphrases.append(phrase)
	return keyphrases