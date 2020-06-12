from __future__ import print_function

import pandas as pd
from keras_text_summarization.library.seq2seq_test import Seq2SeqSummarizer
import numpy as np


def main():
    np.random.seed(42)
    data_dir_path = './data'
    model_dir_path = './models'

    print('loading csv file ...')
    df = pd.read_csv(data_dir_path + "/Article_202004.csv")
    X = df['text']
    Y = df.title

    config = np.load(Seq2SeqSummarizer.get_config_file_path(model_dir_path=model_dir_path)).item()

    summarizer = Seq2SeqSummarizer(config)
    summarizer.load_weights(weight_file_path=Seq2SeqSummarizer.get_weight_file_path(model_dir_path=model_dir_path))

    print('start predicting ...')
    for i in np.random.permutation(np.arange(len(X)))[0:20]:
        x = X[i]
        actual_headline = Y[i]
        headline = summarizer.summarize(x)
        # print('Article: ', x)
        list_str = headline.split()
        head_set = set()
        res = []
        for e in list_str:
            if e not in head_set:
                res.append(e)
                head_set.add(e)
        headline = res
        check = False
        for e in range(len(headline)):
            if headline[e] == '에':
                headline[e-1] += headline[e]
                ckech = True
        if check:
            headline.remove('에')
        
        print('Generated Headline: ', ' '.join(headline))
        print('Original Headline: ', actual_headline)


if __name__ == '__main__':
    main()
