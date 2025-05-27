
from typing import List, Tuple, NamedTuple
import numpy as np
import networkx as nx

import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
from nltk.tokenize import sent_tokenize

from rouge_score import rouge_scorer
rouge_score = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)

# from summarizer import Summarizer

# import spacy
# # spacy.cli.download("en_core_web_md")
# spacy_tokenizer = spacy.load("en_core_web_sm")  #"en_core_web_md" for a larger model
# # spacy_tokenizer = spacy.load("en_core_web_md")
# import stanza
# # stanza.download('en')



def summarize(input_text,  summary_length_str):
    summary_length = int(summary_length_str)
    summarization = 'textrank'
    tokenization = 'nltk'
    metric = 'rouge'

    result = extractive_summary(input_text, summary_length, summary_method=summarization, tokenization_method=tokenization, eval_metric=metric)

    # print("\n\n  ___ Results ___")
    # print(f"\n +++ Used:   {tokenization} | {metric} | {summarization} +++\n")
    # print("scores :=>", "P:", result.precision, ", R:", result.recall, ", F:", result.f1_score, "\n")

    summary = enumerate_list(result.generated_summary)
    return summary

# =====================================================================================


def sentence_similarity(sent1,sent2,stopwords=None):
    if stopwords is None:
        stopwords = []
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
    all_words = list(set(sent1 + sent2))

    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)

    for word in sent1:
        if not word in stopwords:
            vector1[all_words.index(word)]+=1
    for word in sent2:
        if not word in stopwords:
            vector2[all_words.index(word)]+=1

    return 1-cosine_distance(vector1,vector2)

def build_similarity_matrix(sentences,stop_words):
    length = len(sentences)
    similarity_matrix = np.zeros((length,length))
    for idx1 in range(length):
        for idx2 in range(length):
            if idx1!=idx2:
                similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1],sentences[idx2],stop_words)
    return similarity_matrix


# Evaluation methods (metrics)
def rouge(generated_summary_str, reference_summary_str):
    scores = rouge_score.score(reference_summary_str, generated_summary_str)
    P = R = F = 0
    for key in scores:
        P += scores[key].precision
        R += scores[key].recall
        F += scores[key].fmeasure
    return P / 3, R / 3, F / 3


# Summary methods

def extractive_summary(text, required_summary_length, summary_method='textrank', tokenization_method="nltk", eval_metric='rouge'):
    text = tokenize_text(text, tokenization_method)
    n_sentences = calculate_sentences(text, required_summary_length)
    generated_summary = generate_summary(text, n_sentences, method=summary_method)
    
    # P, R, F = evaluate(generated_summary, reference_summary, eval_metric)
    P, R, F = 1, 2, 3
    roundto = 5 # sets the round value of results
    return EvaluationResultType(round(P, roundto), round(R, roundto), round(F, roundto), generated_summary)

def generate_summary(sentences, n_sentences, method='textrank'):
    summarize_text = []
    
    if(method == 'textrank'):
        stop_words = stopwords.words('english')
        sentence_similarity_matrix = build_similarity_matrix(sentences, stop_words)
        sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
        scores = nx.pagerank(sentence_similarity_graph)
        ranked_sentences = sorted(((scores[i],s) for i, s in enumerate(sentences)),reverse=True)

        for i in range(n_sentences):
            summarize_text.append(ranked_sentences[i][1])
    # elif(method == 'bertsum'):
    #     text_for_bertsum = " ".join(sentences)
    #     bertsum_model = Summarizer()
    #     summarize_text = bertsum_model(text_for_bertsum, num_sentences=n_sentences, return_as_list=True)

    return summarize_text


class EvaluationResultType(NamedTuple):
    precision: float
    recall: float
    f1_score: float
    generated_summary: List[str]
    # reference_summary: List[str]

def evaluate(generated_summary, reference_summary, eval_metric):
    results = []
    generated_summary_str = " ".join(generated_summary)
    reference_summary_str = " ".join(reference_summary)
    if(eval_metric == 'bertscore'):
        # return bertscore(generated_summary_str, reference_summary_str)
        print("no BertScore, 'cause it's shyt")
        
    elif(eval_metric == 'rouge'):
        return rouge(generated_summary_str, reference_summary_str)
        
    return None


# Helpers

def enumerate_list(list):
    summary = ''
    for row in list:
        summary += row

    return summary


def calculate_sentences(text_length, summary_length):
    raw_count = len(text_length) * (summary_length / 100)
    
    summary_count = round(raw_count)
    if summary_count == 0:
        summary_count = 1
        
    return summary_count


# Tokenization

def tokenize_text(text, tokenization_method='nltk'):
    print("===  === Tokenizing... ===  ===")
    
    if(tokenization_method == 'nltk'):
        sentences = sent_tokenize(text)
    elif(tokenization_method == 'spacy'):
        # sentences_spacy = spacy_tokenizer(text)
        sentences_spacy = "HHHHHHHHHHHHHHHHHHHH"
        sentences = [sentence.text for sentence in sentences_spacy.sents]
        
    elif(tokenization_method == 'stanza'):
        # stanza_pipeline = stanza.Pipeline(lang='en', processors='tokenize')
        # doc = stanza_pipeline(text)
        doc = None
        sentences = [sentence.text for sentence in doc.sentences]
    elif(tokenization_method is None):
        return text

    return sentences
