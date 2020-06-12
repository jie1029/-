from __future__ import print_function

from keras_text_summarization.library.seq2seq_test import Seq2SeqSummarizer
import numpy as np


def generate(text = None,title = None):
    np.random.seed(42)
    data_dir_path = './data'
    model_dir_path = '/home/mls-server/server/demo/models'

    if text == None:
        return False
    
    X = [[text]]
    origin_headline = title

    config = np.load(Seq2SeqSummarizer.get_config_file_path(model_dir_path=model_dir_path)).item()

    summarizer = Seq2SeqSummarizer(config)
    summarizer.load_weights(weight_file_path=Seq2SeqSummarizer.get_weight_file_path(model_dir_path=model_dir_path))

    for i in np.random.permutation(np.arange(len(X)))[0:20]:
        x = X[i]   
        if type(x) != str:
            x = str(x)

        headline = summarizer.summarize(x)

        list_str = headline.split()
        head_set = set()
        res = []
        for e in list_str:
            if e not in head_set:
                res.append(e)
                head_set.add(e)
        headline = res

        result = [' '.join(headline),origin_headline]

    return result

if __name__ == '__main__':
    generate()
