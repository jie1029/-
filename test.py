import sys

import json
from seq2seq_test_predict import generate
import os


def main():
    
    if len(sys.argv) == 2:
        text = str(sys.argv[1])
        result = generate(text=text)
    elif len(sys.argv) == 3:
        text = str(sys.argv[1])
        title = str(sys.argv[2])
        result = generate(text=text,title=title)

    resultJSON = {"generatedTitle":result[0],"originTitle":result[1]}
    print(json.dumps(resultJSON))


if __name__ == "__main__":
    main()

