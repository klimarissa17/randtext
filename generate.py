import re
import random
import argparse
import sys
import pickle

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


def gen(file, model, start, n):
    token_0 = start

    def text_gen(token_0):
        for k in range(n):
            if token_0 not in model:
                token_0 = random.choice(list(model.keys()))
            yield token_0
            lst = list()
            for i in model[token_0]:  # type: object
                for j in range(i[1]):#model[token_0][i1])):
                    lst.append(i)
            token_1 = random.choice(lst)
            lst.clear()
            token_0 = token_1

    clean_string = re.sub(r' ([.,;!?:])', r'\1', ' '.join(text_gen(token_0)))
    file.write(clean_string + '\n')
    del clean_string


args = create_parser()

with open(args.model, 'rb') as file:
    model = pickle.load(file)


if args.output is None:
    gen(sys.stdout, model, args.seed, int(args.length))
else:
    with open(args.output, "w") as file:
        gen(file, model, args.seed, int(args.length))
