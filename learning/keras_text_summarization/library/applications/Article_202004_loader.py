from collections import Counter
from konlpy.tag import Okt
import re

MAX_INPUT_SEQ_LENGTH = 500
MAX_TARGET_SEQ_LENGTH = 20
MAX_INPUT_VOCAB_SIZE = 5000
MAX_TARGET_VOCAB_SIZE = 2000

okt = Okt()
def text_tokenizing(line):
    line = re.sub("↑", "상승", line)
    line = re.sub("↓", "하강", line)
    line = re.sub("%", "퍼센트", line)
    line = re.sub(u"[,.'-_:;#…’‘”“·…\[\]\"]"," ", line)
    tokenized_data = okt.pos(line) # 토큰화
    #print(tokenized_data)
    #temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
    return tokenized_data

def fit_text(X, Y, input_seq_max_length=None, target_seq_max_length=None):
    if input_seq_max_length is None:
        input_seq_max_length = MAX_INPUT_SEQ_LENGTH
    if target_seq_max_length is None:
        target_seq_max_length = MAX_TARGET_SEQ_LENGTH
    input_counter = Counter()
    target_counter = Counter()
    max_input_seq_length = 0
    max_target_seq_length = 0
    i = 0
    for line in X:
        text = text_tokenizing(line)
        
        i +=1
        seq_length = len(text)
        if seq_length > input_seq_max_length:
            text = text[0:input_seq_max_length]
            seq_length = len(text)
        for word in text:
            input_counter[word] += 1
        max_input_seq_length = max(max_input_seq_length, seq_length)

    check = True
    for line in Y:
       
        text= text_tokenizing(line)
        text = ['START'] + text + ['END']

        if(check):
            print(line)
            print(text)
            check=False
        
        seq_length = len(text)
        if seq_length > target_seq_max_length:
            text = text[0:target_seq_max_length]
            seq_length = len(text)
        for word in text:
            target_counter[word] += 1
            max_target_seq_length = max(max_target_seq_length, seq_length)

    # Y = text
    # print(Y.shape)
    # print("-------------------------------")
    input_word2idx = dict()
    for idx, word in enumerate(input_counter.most_common(MAX_INPUT_VOCAB_SIZE)):
        input_word2idx[word[0]] = idx + 2
    input_word2idx['PAD'] = 0
    input_word2idx['UNK'] = 1
    input_idx2word = dict([(idx, word) for word, idx in input_word2idx.items()])

    target_word2idx = dict()
    for idx, word in enumerate(target_counter.most_common(MAX_TARGET_VOCAB_SIZE)):
        target_word2idx[word[0]] = idx + 1
    target_word2idx['UNK'] = 0

    target_idx2word = dict([(idx, word) for word, idx in target_word2idx.items()])
    
    num_input_tokens = len(input_word2idx)
    num_target_tokens = len(target_word2idx)

    config = dict()
    config['input_word2idx'] = input_word2idx
    config['input_idx2word'] = input_idx2word
    config['target_word2idx'] = target_word2idx
    config['target_idx2word'] = target_idx2word
    config['num_input_tokens'] = num_input_tokens
    config['num_target_tokens'] = num_target_tokens
    config['max_input_seq_length'] = max_input_seq_length
    config['max_target_seq_length'] = max_target_seq_length

    return config
