from typing import Any
from typing import Callable
from typing import Iterable
from typing import List
from typing import Optional
from typing import Tuple

from itertools import chain

import numpy as np
from transformers import PretrainedConfig

from nlpipes.data.data_types import InputExample


def chunk() -> Callable[[str], List[str]]:
    """  Chunk text into shorter sequences. """  
    
    def chunk_into_sentences(texts: str) -> List[str]:
        """ Chunk text with regular-expressions """
        on_regex = '(?<=[^A-Z].[.?]) +(?=[A-Z])'
        sequences = [re.split(on_regex, text) for text in texts]
        sequences = [sequence for sublist in sequences for sequence in sublist]
        return sequences
    
    def chunk_into_whatever(texts: str) -> List[str]:
        raise NotImplementedError
    
    chunk_fn = chunk_into_sentences

    return chunk_fn
    
    
def create_examples(
    texts: List[str],
    labels: Optional[List[str]],
    config: PretrainedConfig,
   ) -> List[InputExample]:
    """ Serialize each input raw data into examples. """
    
    if labels:
        if get_nesting_level(labels)==1:
            labels = [config.label2id[label] for label in labels]
            examples = [
                InputExample(text=text, label=label)
                for text, label in zip(texts, labels)
            ]
        elif get_nesting_level(labels)==2:
            labels = [
                [config.label2id[label] for label in sub_labels] 
                for sub_labels in labels
            ]
            examples = [
                InputExample(text=text, label=label)
                for text, label in zip(texts, labels)
            ]
    else:
        examples = [InputExample(text=text) for text in texts]
        
    return examples


def split_examples(
    examples: List[InputExample],
    train_frac: float = None,
    test_frac: float = None, 
    shufffle: bool = True,
    random_seed: int = 42,
   ) -> Tuple[InputExample]:
    """ split the input example into a training and a
    testing set. """
    
    n_examples = len(examples)
    n_train = int(np.ceil(n_examples*train_frac))
    n_test = int(np.ceil(n_examples*test_frac))
    n_total = n_train + n_test
    
    if shufffle:
        random_state = np.random.RandomState(random_seed)
        order = random_state.permutation(n_examples)
        train_idx = order[:n_train]
        test_idx = order[n_train:n_total]
    else:
        train_idx = np.arange(n_train)
        test_idx = np.arange(n_train, n_total)
    
    train_examples = [examples[idx] for idx in train_idx]
    test_examples = [examples[idx] for idx in test_idx]
    
    return train_examples, test_examples


def generate_batches(
    X: List[str], 
    Y: List[str], 
    batch_size: int,
) -> Iterable[List[Any]]:
    """ Yield a batch of examples from the input raw data """
    
    X_batch = list()
    Y_batch = list()
    
    for x, y in zip(X,Y):
        X_batch.append(x)
        Y_batch.append(y)
        if len(X_batch) < batch_size:
            continue
        yield X_batch, Y_batch    
        X_batch = list()
        Y_batch = list()


def get_nesting_level(maybe_nested_labels):
    max_level = 1
    for element in maybe_nested_labels:
        if isinstance(element, list):
            level = get_labels_type(element)
            if level > max_level:
                max_level = level
    return max_level
