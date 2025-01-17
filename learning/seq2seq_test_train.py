from __future__ import print_function

import pandas as pd
from sklearn.model_selection import train_test_split
from keras_text_summarization.library.utility.plot_utils import plot_and_save_history
from keras_text_summarization.library.seq2seq_test import Seq2SeqSummarizer
from keras_text_summarization.library.applications.Article_202004_loader import fit_text
import numpy as np

LOAD_EXISTING_WEIGHTS = False


def main():
    np.random.seed(42)
    data_dir_path = './data'
    report_dir_path = './reports'
    model_dir_path = './models'

    print('loading csv file ...')
    df = pd.read_csv(data_dir_path + "/Article_202004.csv")
    df = df.dropna(how = 'any')
    print('extract configuration from input texts ...')
    Y = df.title
    X = df['text']

    config = fit_text(X, Y)

    summarizer = Seq2SeqSummarizer(config)

    if LOAD_EXISTING_WEIGHTS:
        summarizer.load_weights(weight_file_path=Seq2SeqSummarizer.get_weight_file_path(model_dir_path=model_dir_path))

    Xtrain, Xtest, Ytrain, Ytest = train_test_split(X, Y, test_size=0.2, random_state=42)

    print('demo size: ', len(Xtrain))
    print('testing size: ', len(Xtest))

    print('start fitting ...')
    history = summarizer.fit(Xtrain, Ytrain, Xtest, Ytest, epochs=20)

    history_plot_file_path = report_dir_path + '/' + Seq2SeqSummarizer.model_name+"-test" + '-history.png'
    if LOAD_EXISTING_WEIGHTS:
        history_plot_file_path = report_dir_path + '/' + Seq2SeqSummarizer.model_name +"-test"+ '-history-v' + str(summarizer.version) + '.png'
    plot_and_save_history(history, summarizer.model_name+"-test", history_plot_file_path, metrics={'loss', 'acc'})


if __name__ == '__main__':
    main()
