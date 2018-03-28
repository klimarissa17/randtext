import re
import argparse
from collections import defaultdict
import sys
import os


alph = re.compile(u'[a-zA-Zа-яА-ЯёЁ-]+|[.,:;?!]+')


def words_gen(string):
    for word in alph.findall(string):
        yield word


def bigram_gen(string):
    t0 = ''
    for t1 in words_gen(string):
        yield t0, t1
        t0 = t1


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
        for t0, t1 in bigram_gen(s):
            bi[t0, t1] += 1
    for (t0, t1) in bi.keys():
        if t0 in model:
            model[t0].append((t1, bi[t0, t1]))
        else:
            model[t0] = [(t1, bi[t0, t1])]


def save_model(f, model):
    for i in model:
        if i == '':
            continue
        f.write(i + ' ')
        for j, num in model[i]:
            f.write(j + ' ' + str(num) + ' ')
        f.write('\n')


args = create_parser()
model = dict()
if args.input_dir is None:
    train(sys.stdin, args.lc, model)
else:
    for filename in os.listdir(args.input_dir):
        instream = open(args.input_dir + '/' + filename, 'r')
        train(instream, args.lc, model)
        instream.close()
outstream = open(args.model, "w")
save_model(outstream, model)
outstream.close()
