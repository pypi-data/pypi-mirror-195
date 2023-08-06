from functools import lru_cache

import numpy as np
from faker import Faker
from hbutils.random import keep_global_state
from scipy.stats import linregress


@lru_cache()
@keep_global_state()
def _linear_of_fake_sentence(func, *args, **kwargs):
    def sentence_length(n, m=20):
        lengths = [len(func(n, *args, **kwargs)) for _ in range(m)]
        return np.mean(lengths), np.std(lengths)

    x = np.asarray(range(1, 21, 2))
    yz = [sentence_length(i) for i in x]
    y = np.asarray([i for i, _ in yz])
    k, b, *_ = linregress(x, y)
    return k, b


_FAKER = Faker()


def fake_str(expected_length: int, fake_func, *args, allow_zero: bool = True, **kwargs):
    k, b = _linear_of_fake_sentence(fake_func, *args, **kwargs)
    word_cnt = int(max(round((expected_length - b) / k), 0 if allow_zero else 1))
    return fake_func(word_cnt, *args, **kwargs)


def fake_sentence(expected_length, allow_zero: bool = True) -> str:
    return fake_str(expected_length, _FAKER.sentence, allow_zero=allow_zero)


@lru_cache()
def _words_func_with_splitter(word_func, splitter: str = ' '):
    def _word_func(n):
        return splitter.join([word_func() for _ in range(n)])

    return _word_func


def fake_words(expected_length, allow_zero: bool = True, word_func=_FAKER.word, splitter: str = ' ') -> str:
    return fake_str(expected_length, _words_func_with_splitter(word_func, splitter), allow_zero=allow_zero)
