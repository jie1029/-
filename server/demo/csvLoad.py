import sys

import json
from keras_text_summarization.library.seq2seq_test import Seq2SeqSummarizer
import os
import pandas as pd
import numpy as np

def main():
    
    filename = sys.argv[1]
    model_dir_path = './demo/models'
    data_dir_path = './demo/upload/'
    result_dir_path = './demo/result/'
    df = pd.read_csv(data_dir_path + filename)
    
    X = df['text']
    config = np.load(Seq2SeqSummarizer.get_config_file_path(model_dir_path=model_dir_path)).item()

    summarizer = Seq2SeqSummarizer(config)
    summarizer.load_weights(weight_file_path=Seq2SeqSummarizer.get_weight_file_path(model_dir_path=model_dir_path))

    df["generated title"] = "demo data"
    for i in range(0,len(X)):
        
        x = X[i]
        headline = summarizer.summarize(x)

        list_str = headline.split()
        head_set = set()
        res = []
        for e in list_str:
            if e not in head_set:
                res.append(e)
                head_set.add(e)
        headline = res

        df["generated title"][i] = ' '.join(headline)

    df.to_csv(result_dir_path+"result_"+filename,encoding='utf-8')
    result = {"file_name":"result_"+filename}
    print(json.dumps(result))
    
if __name__ == "__main__":
    main()
