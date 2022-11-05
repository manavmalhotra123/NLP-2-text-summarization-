import streamlit as st 

from gensim.summarization import summarize

# Sumy Summary Pkg
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

import spacy
from spacy import displacy
nlp = spacy.load('en')

# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen

# function for summarisation 
def sumy_summarization(docx):
    parser = PlaintextParser.from_string(docx,Tokenizer("english"))
    lex_summarizer = LexRankSummarizer()
    summary = lex_summarizer(parser.document,3)
    summary_list = [str(sentence) for sentence in summary]
    result = ' '.join(summary_list)
    return result

# Fetching the text from the url
@st.cache
def get_text(raw_url):
    page = urlopen( raw_url )
    soup = BeautifulSoup(page)
    fetched_text = " ".join(map(lambda p:p.text,soup.find_all('p')))
    return fetched_text

@st.cache(allow_output_mutation=True)
def analyze_text(text):
	return nlp(text)


def main():
	"""Summaryzer Streamlit App"""

	st.title("Summaryzer and Entity Checker")

	activities = ["Summarize","NER Checker","NER For URL"]
	choice = st.sidebar.selectbox("Select Activity",activities)

	if choice == 'Summarize':
		st.subheader("Summarize Document")
		raw_text = st.text_area("Enter Text Here","Type Here")
		summarizer_type = st.selectbox("Summarizer Type",["Gensim","Sumy Lex Rank"])
		if st.button("Summarize"):
			if summarizer_type == "Gensim":
				summary_result = summarize(raw_text)
			elif summarizer_type == "Sumy Lex Rank":
				summary_result = sumy_summarizer(raw_text)

			st.write(summary_result)

	if choice == 'NER Checker':
		st.subheader("Named Entity Recog with Spacy")
		raw_text = st.text_area("Enter Text Here","Type Here")
		if st.button("Analyze"):
			docx = analyze_text(raw_text)
			html = displacy.render(docx,style="ent")
			html = html.replace("\n\n","\n")
			st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)


	if choice == 'NER For URL':
		st.subheader("Analysis on Text From URL")
		raw_url = st.text_input("Enter URL Here","Type here")
		text_preview_length = st.slider("Length to Preview",50,100)
		if st.button("Analyze"):
			if raw_url != "Type here":
				result = get_text(raw_url)
				len_of_full_text = len(result)
				len_of_short_text = round(len(result)/text_preview_length)
				st.success("Length of Full Text::{}".format(len_of_full_text))
				st.success("Length of Short Text::{}".format(len_of_short_text))
				st.info(result[:len_of_short_text])
				summarized_docx = sumy_summarizer(result)
				docx = analyze_text(summarized_docx)
				html = displacy.render(docx,style="ent")
				html = html.replace("\n\n","\n")
				st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)
				
		


if __name__ == '__main__':
	main()
