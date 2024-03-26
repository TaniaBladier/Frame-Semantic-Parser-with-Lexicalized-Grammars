# Frame Semantic Parser with Lexicalized Grammars

Code and data for paper ["Data-Driven Frame-Semantic Parsing
with Tree Wrapping Grammar"](https://iwcs.pimoid.fr/42.pdf) from the [IWCS 2023](https://iwcs2023.loria.fr/) conference


## Installation

The code works with the Python 3.9.6 version

Install the packages from the requirements.txt file. 


## Download fine-tuned language model

Fine-tuned multitask BERT-based MaChAmp model:	[download (570 MB)](https://www.dropbox.com/scl/fi/2lutfdecw81gg47pcj921/machamp-multitask-model.zip?rlkey=chi2419wtfi66tg9q9n7ryd04&dl=0)

Unzip the model and place it in the folder `models`, rename it to `machamp-multitask-model`

## Machamp

We use the [AllenNLP MaChAmp library](https://bitbucket.org/ahmetustunn/mtp/src/master/) which focuses on multi-task learning. It has support for training on multiple datasets for a variety of standard NLP tasks. 

You can check the following repository to find further functionalitites of MaChAmp:
[MachAmp repository](https://bitbucket.org/ahmetustunn/mtp/src/master/)

## Parse sentences

You can parse sentences using the following command. You have to provide the path to the unzipped multitask model, input data, and an output path.

You have to specify with the option `--dataset FRAME, LKG, STAG` which task you want to predict.

- option FRAME will predict frames
- option LKG will predict linkings
- option STAG will predict supertags.

`python3 machamp/predict.py models/machamp-multitask-model/model.tar.gz data/example-input.frames data/example-output.frames --device 0 --dataset FRAME`

Please take a look at the example of [an input file](https://github.com/TaniaBladier/Frame-Semantic-Parser-with-Lexicalized-Grammars/blob/main/data/example-input.frames) and [an the output file](https://github.com/TaniaBladier/Frame-Semantic-Parser-with-Lexicalized-Grammars/blob/main/data/example-output.frames).

The supertags are provided in the 5th column and look like `(NP* (OP-DEF <>))`

The frames are in the 7th column and look like `[COME-AFTER_FOLLOW-IN-TIME]`

The linkings between frames and semantic roles are in the 8th column and look like `[[1, 'Experiencer'], [2, 'Theme']]` where index 1 and 2 show which argument slots in the supertag should be filled with the correspoding role. The index 0 stands for a semantic role which is syntactically implied but not expressed in the supertag.


## Data evaluation

The evaluations are run automatically as you run the script `predict.py` and are stored in the output directory in the file with the extension .eval

## Frame Feature Unification 

The file `frame_feature_unification.py` takes the predicted output from the semantic parser and uses feature unification mechanisme to produce the frame representation of the sentence.

To test the file, use some example sentences provided in file [`data/example-input.frames`](https://github.com/TaniaBladier/Frame-Semantic-Parser-with-Lexicalized-Grammars/blob/main/data/example-input.frames)

Here is an example unified sentence frame from our paper:

<img src="https://github.com/TaniaBladier/Frame-Semantic-Parser-with-Lexicalized-Grammars/blob/main/img/Example-Frame-Representation.png" width="400">



