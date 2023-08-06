import enum
import math
import random
from typing import Mapping, Tuple, Sequence, Any

import numpy as np
from faker import Faker
from hbutils.random import seedable_func
from scipy.stats import norm
from yattag import Doc, indent as _html_indent

from .base import EOE, TEXT, COMMENT
from ..utils import tail_tuple, fake_sentence, fake_words

_SELF_CLOSING_TAGS = [
    'area',
    'base',
    'br',
    'col',
    'embed',
    'hr',
    'img',
    'input',
    'link',
    'meta',
    'param',
    'source',
    'track',
    'wbr',
]

_FAKER = Faker()


def _random_id(expected_length, allow_zero: bool = False):
    return fake_words(expected_length, allow_zero=allow_zero, splitter='_')


def _random_class(**kwargs):
    _ = kwargs
    word_cnt = int(max(round(norm(3, 1).rvs()), 1))
    return '-'.join([_FAKER.word() for _ in range(word_cnt)])


def _random_classes(expected_length, allow_zero: bool = False):
    return fake_words(expected_length, allow_zero=allow_zero, word_func=_random_class, splitter=' ')


_RANDOM_ATTR_FUNCS = {
    'id': _random_id,
    'class': _random_classes,
    'href': lambda x: _FAKER.uri(),
    ('img', 'src'): lambda x: _FAKER.image_url(),
    'src': lambda x: _FAKER.uri(),
    'data-src': lambda x: _FAKER.uri(),
    'data-href': lambda x: _FAKER.uri(),
}


class HTMLMarkov:
    def __init__(self, lparent: int, lprev: int,
                 tags_chain: Mapping[tuple, Tuple[list, np.ndarray]],
                 tags_count: Mapping[tuple, Tuple[float, float]],
                 tags_attrib: Mapping[tuple, Mapping[str, tuple]]):
        self.__lparent = lparent
        self.__lprev = lprev
        self._tags_chain = tags_chain
        self._tags_count = tags_count
        self._tags_attrib = tags_attrib

    def _parent_feature(self, feat: Sequence[str]) -> Tuple[str, ...]:
        return tail_tuple(feat, self.__lparent)

    def _prev_feature(self, feat: Sequence[str]) -> Tuple[str, ...]:
        return tail_tuple(feat, self.__lprev)

    @seedable_func
    def fake_html(self, start_path: Tuple[str, ...] = (), indent: bool = True, scale: float = 0.4):
        if not 0.01 < scale < 0.99:
            raise ValueError(f'Invalid scale, (0.01, 0.99) expected but {scale!r} found.')

        doc, tag, text = Doc().tagtext()
        self._random_html(start_path, (doc, tag, text), scale)

        source = doc.getvalue()
        if indent:
            source = _html_indent(source)
        return source

    def _random_html(self, path: Tuple[str, ...], deco: Tuple[Any, Any, Any], scale: float = 0.5):
        doc, tag, text = deco
        p_feat = self._parent_feature(path)
        mean, std = self._tags_count[p_feat]
        cnt = norm(mean, std).ppf(scale + (random.random() - 0.5) / 50)
        if math.isnan(cnt):
            cnt = int(mean)
        else:
            cnt = int(max(round(cnt), 0))

        prevs = []
        for i in range(int(cnt * 1.2)):
            feature = (self._parent_feature(path), self._prev_feature(prevs))
            tags, prob = self._tags_chain[feature]
            new_tag = np.random.choice(tags, p=prob)
            if new_tag is EOE:
                if i < cnt * 0.7:
                    prevs.clear()
                else:
                    break
            else:
                if new_tag is TEXT:
                    self._random_text(deco)
                elif new_tag is COMMENT:
                    self._random_comment(deco)
                else:
                    attrs = {}
                    new_p_feat = self._parent_feature((*path, new_tag))
                    for key, (type_, prob, spec) in self._tags_attrib[new_p_feat].items():
                        if random.random() >= prob:
                            continue

                        if type_ is enum:
                            values, probs = spec
                            val = np.random.choice(values, p=probs)
                        elif type_ in {int, float}:
                            mean, std = spec
                            if (new_tag, key) in _RANDOM_ATTR_FUNCS:
                                val = _RANDOM_ATTR_FUNCS[(new_tag, key)](mean, std)
                            elif key in _RANDOM_ATTR_FUNCS:
                                val = _RANDOM_ATTR_FUNCS[key](mean, std)
                            else:
                                val = str(type_(norm(mean, std).rvs()))
                        elif type_ is str:
                            mean_length = spec
                            val = _RANDOM_ATTR_FUNCS.get(
                                (new_tag, key),
                                _RANDOM_ATTR_FUNCS.get(key, fake_sentence)
                            )(mean_length)
                        else:
                            assert False, f'Unknown type - {type_!r}.'

                        if val:
                            attrs[key] = val

                    if new_tag in _SELF_CLOSING_TAGS:
                        doc.stag(new_tag, *attrs.items())
                    else:
                        with tag(new_tag, *attrs.items()):
                            self._random_html((*path, new_tag), deco, scale)
                prevs.append(new_tag)

    @classmethod
    def _random_text(cls, deco: Tuple[Any, Any, Any]):
        doc, tag, text = deco
        text(_FAKER.sentence(5))

    @classmethod
    def _random_comment(cls, deco: Tuple[Any, Any, Any]):
        doc, tag, text = deco
        doc.asis(f'<!--{_FAKER.sentence(5)}-->')
