from typing import Dict, List
import logging
from allennlp.data.instance import Instance
from allennlp.data.fields import TextField, SequenceLabelField, MetadataField, LabelField
from allennlp.data.tokenizers import Token, Tokenizer, WhitespaceTokenizer
from machamp.dataset_readers.lemma_edit import gen_lemma_rule
from machamp.dataset_readers.reader_utils import _clean_text

logger = logging.getLogger(__name__)

def read_raw(dataset, config, path, is_train, max_sents, max_words, token_indexers, tokenizer):
    """
    Reads the data from a raw txt file. Assumes that each sentence is on a line, and
    the words are separated by a whitespace.
    """
    data = []
    if 'word_idx' in config:
        input_idx = config['word_idx']
    else:
        if 'sent_idxs' in config and len(config['sent_idxs']) == 1:
            input_idx = config['sent_idxs'][0]
        else:
            logger.warning("--raw_text is only supported for sequence labeling task-types and classification with only one input column. If you do classification with multiple inputs, please add a dummy column")
            exit(1)
    skip_first_line = config['skip_first_line']
    word_counter = 0
    for sent_counter, sent in enumerate(open(path, encoding='utf-8', mode='r')):
        if skip_first_line:
            skip_first_line = False
            continue
        if max_sents != 0 and sent_counter > max_sents:
            break
        sent = sent.strip('\n')
        tokens = [Token(word) for word in sent.split(' ')]
        word_counter += len(tokens)
        if max_words != 0 and word_counter > max_words:
            break
        input_field = TextField(tokens, token_indexers)
        instance = Instance({'tokens': input_field})
        col_idxs = {'word_idx': input_idx}
        task2type = {}
        for task in config['tasks']:
            task_idx = config['tasks'][task]['column_idx']
            col_idxs[task] = task_idx
            task_type = config['tasks'][task]['task_type']
            task2type[task] = task_type
        if set(task2type.values()) != {'classification'}:
                sent = tokens
        else:
            sent = [sent]
        metadata = {}
        # the other tokens field will often only be available as word-ids, so we save a copy
        metadata['tokens'] = tokens
        metadata["full_data"] = sent
        metadata["col_idxs"] = col_idxs
        metadata['is_train'] = is_train
        metadata['no_dev'] = False
        instance.add_field('metadata', MetadataField(metadata))
        data.append(instance)
    return data
