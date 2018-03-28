import re
import random
import argparse
import sys


def create_parser():
    parser = argparse.ArgumentParser(
        description="Generate a new text on the base of corpus")
    parser.add_argument("--model",
                        help="Path to the file with generated model")
    parser.add_argument("--seed", help="The desired first word; "
                                       "will be chosen randomly by default")
    parser.add_argument("--length", help="The desired length of text")
    parser.add_argument("--output",
                        help="File in which to save generated text; "
                             "will be printed to stdout by default")
    return parser.parse_args()


def parse_model(f):
    model = dict()
    for s in f:
        lst = s.split()
        x = lst[0]
        model[x] = dict()
        for i in range(1, len(lst) - 1, 2):
            model[x][lst[i]] = int(lst[i + 1])
    return model


def gen(f, model, start, n):
    t0 = start

    def text_gen(t0):
        for k in range(n):
            if t0 not in model:
                t0 = random.choice(list(model.keys()))
            yield t0
            lst = list()
            for i1 in model[t0]:
                for j in range(int(model[t0][i1])):
                    lst.append(i1)
            t1 = random.choice(lst)
            lst.clear()
            t0 = t1

    s1 = re.sub(r' ([.,;!?:])', r'\1', ' '.join(text_gen(t0)))
    f.write(s1 + '\n')
    del s1


args = create_parser()

f = open(args.model, "r", encoding='utf8')
model = parse_model(f)
f.close()

if args.output is None:
    gen(sys.stdout, model, args.seed, int(args.length))
else:
    f = open(args.output, "w")
    gen(f, model, args.seed, int(args.length))