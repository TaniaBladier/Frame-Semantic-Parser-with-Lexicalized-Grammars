conllfile = '/home/tania/Documents/multitask_transformers_supertagger/machamp/data/dev.supertag'

outfile = "/home/tania/Documents/multitask_transformers_supertagger/machamp/data/dev.plain"

outf = open(outfile, 'w')

def readFile(path):
    sentences = []
    sentence = []
    for line in open(path):
        line = line.strip()
        if not line:
            if len(sentence) > 0:
                sentences.append(sentence)
                sentence = []
        else:
            word = line.split("\t")[1]
            sentence.append(word)
    if len(sentence) > 0:
        sentences.append(sentence)
    print("number of sents: ", len(sentences))
    return sentences

sents = readFile(conllfile)

for x in sents:
    outf.write(" ".join(x) + "\n")

outf.close()