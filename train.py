import re
import argparse
from collections import defaultdict
import sys
import os
import pickle


alph = re.compile(u'[a-zA-Z]+|[.,:;?!]+')


def words_gen(string):
    for word in alph.findall(string):
        yield word


def bigram_gen(string):
    token_0 = ''
    for token_1 in words_gen(string):
        yield token_0, token_1
        token_0 = token_1


def create_parser():
    parser = argparse.ArgumentParser(
        description="trains the generator")
    parser.add_argument("--input-dir",
                        help="path to the folder with texts to train on")
    parser.add_argument("--model",
                        help="path to the .txt where model will be saved")
    parser.add_argument("--lc", action="store_true",
                        help="all texts to lowercase")
    return parser.parse_args()


def train(f, lc, model):  # f is instream
    bi = defaultdict(lambda: 0)
    for s in f:
        if lc:
            s = s.lower()
        for token_0, token_1 in bigram_gen(s):
            bi[token_0, token_1] += 1
    for (token_0, token_1) in bi.keys():
        if token_0 in model:
            model[token_0].append((token_1, bi[token_0, token_1]))
        else:
            model[token_0] = [(token_1, bi[token_0, token_1])]


def save_model(f, model):
    with open (f, 'wb') as file:
        pickle.dump(model, file)
        """for i in model:
            if i == '':
                continue
            f.write(i + ' ')
            for j, num in model[i]:
                f.write(j + ' ' + str(num) + ' ')
            f.write('\n')"""


args = create_parser()
model = dict()
if args.input_dir is None:
    train(sys.stdin, args.lc, model)
else:
    for filename in os.listdir(args.input_dir):
        with open(args.input_dir + '/' + filename, 'r') as instream:
            train(instream, args.lc, model)

#with open(args.model, "wb") as outstream:
   # save_model(outstream, model)
save_model(args.model, model)
