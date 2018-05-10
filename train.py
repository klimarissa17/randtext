import re
import argparse
from collections import defaultdict
import sys
import os
import pickle


alph = re.compile(u'[a-zA-Zа-яА-ЯёЁ]+|[.,:;?!]+')


def words_gen(string):
    for word in alph.findall(string):
        yield word


def bigramsgram_gen(string):
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


def train(instream, lc, model):
    bigrams = defaultdict(lambda: 0)
    for current_string in instream:
        if lc:
            current_string = current_string.lower()
        for token_0, token_1 in bigramsgram_gen(current_string):
            bigrams[token_0, token_1] += 1
    for (token_0, token_1) in bigrams.keys():
        if token_0 in model:
            model[token_0].append((token_1, bigrams[token_0, token_1]))
        else:
            model[token_0] = [(token_1, bigrams[token_0, token_1])]


def save_model(f, model):
    with open (f, 'wb') as file:
        pickle.dump(model, file)


args = create_parser()
model = dict()
if args.input_dir is None:
    train(sys.stdin, args.lc, model)
else:
    for filename in os.listdir(args.input_dir):
        with open(args.input_dir + '/' + filename, 'r') as instream:
            train(instream, args.lc, model)


save_model(args.model, model)
