# Frame Semantic Parser with Lexicalized Grammars

Code and data for paper ["Data-Driven Frame-Semantic Parsing
with Tree Wrapping Grammar"](https://iwcs.pimoid.fr/42.pdf) from the [IWCS 2023](https://iwcs2023.loria.fr/) conference

The code works with the Python 3.10 version

## Installation

Install [ParTAGe-TWG](https://github.com/kawu/partage-twg)

Also install the packages from the requirements.txt file. 


## Download fine-tuned language model

Fine-tuned multitask BERT-based MaChAmp model:	[download (570 MB)](https://www.dropbox.com/scl/fi/dcwbqmbbuwtdm29b1whrz/model.tar.gz?rlkey=3py7io41vdpp6o79a5ezi8lik&dl=0)

## Machamp

We use the [AllenNLP MaChAmp library](https://bitbucket.org/ahmetustunn/mtp/src/master/) which focuses on multi-task learning. It has support for training on multiple datasets for a variety of standard NLP tasks. 

You can check the following repository to find further functionalitites of MaChAmp:
[MachAmp repository](https://bitbucket.org/ahmetustunn/mtp/src/master/)

## Parse sentences

Parse a file with sentences using the file parse_twg. 

It takes two arguments - input file with plain sentences and output file. 


Please take a look at the example [input](https://github.com/TaniaBladier/Transformer-based-TWG-parsing/blob/main/example_input_file.txt) and [output](https://github.com/TaniaBladier/Transformer-based-TWG-parsing/blob/main/example_output_file.txt) files:

```
python sem-parse-multitask.py data/example_input_file.txt data/example_output_file.txt
```
The output format of the output file is discbracket (discontinuous bracket trees). Read more about this format [here](https://discodop.readthedocs.io/en/latest/fileformats.html).


## Data evaluation

Use the file `evaluations.py` to evaluate the output.

## Frame Feature Unification 

The file `frame_feature_unification.py` takes the predicted output from the semantic parser and uses feature unification mechanisme to produce the frame representation of the sentence.

To test the file, use some example sentences provided in file [`data/example_feature_unif_data.txt`](https://github.com/TaniaBladier/Frame-Semantic-Parser-with-Lexicalized-Grammars/blob/main/data/example_feature_unif_data.txt)

Here is an example unified sentence frame from our paper:

<img src="https://github.com/TaniaBladier/Frame-Semantic-Parser-with-Lexicalized-Grammars/blob/main/img/Example-Frame-Representation.png" width="400">



