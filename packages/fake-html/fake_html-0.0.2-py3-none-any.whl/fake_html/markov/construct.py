import enum
import pathlib
from itertools import groupby
from typing import Sequence, Tuple, List

import numpy as np
from lxml.etree import ElementBase
from lxml.html import HtmlComment, HtmlElement
from pyquery import PyQuery as pq
from scipy.stats import norm

from .base import TEXT, EOE, COMMENT
from .model import HTMLMarkov
from ..dataset import load_dataset_from_directory, load_local_dataset
from ..utils import tail_tuple


def _to_tag(ele):
    if isinstance(ele, str):
        ret = TEXT
    elif isinstance(ele, HtmlComment):
        ret = COMMENT
    elif isinstance(ele, HtmlElement):
        ret = ele.tag
    elif isinstance(ele, pq):
        ret = _to_tag(ele[0])
    else:
        raise TypeError(f'Unknown element type - {ele!r}.')

    return ret


MIN_INT32 = -(1 << 31)
MAX_INT32 = (1 << 31) - 1


def _is_int(v):
    try:
        val = int(v)
    except (TypeError, ValueError):
        return False
    else:
        return MIN_INT32 < val < MAX_INT32


def _is_float(v):
    try:
        val = float(v)
    except (TypeError, ValueError):
        return False
    else:
        return MIN_INT32 < val < MAX_INT32


class DataCollector:
    def __init__(self, lparent: int = 3, lprev: int = 5):
        self.lparent = lparent
        self.lprev = lprev
        self._tags_chain = {}
        self._tags_counts = {}
        self._tags_attrib = {}

    def _parent_feature(self, feat: Sequence[str]) -> Tuple[str, ...]:
        return tail_tuple(feat, self.lparent)

    def _prev_feature(self, feat: Sequence[str]) -> Tuple[str, ...]:
        return tail_tuple(feat, self.lprev)

    def _record_tag(self, parent: Sequence[str], prev: Sequence[str], tag: str):
        feature = (self._parent_feature(parent), self._prev_feature(prev))
        if feature not in self._tags_chain:
            self._tags_chain[feature] = {}

        records = self._tags_chain[feature]
        records[tag] = records.get(tag, 0) + 1

    def _record_element_sequence(self, elements, parent: Sequence[str]):
        feat_p = self._parent_feature(parent)
        if feat_p not in self._tags_counts:
            self._tags_counts[feat_p] = []
        self._tags_counts[feat_p].append(len(elements))

        _seq = [*(_to_tag(item) for item in elements), EOE]
        for i, tag in enumerate(_seq):
            self._record_tag(parent, _seq[:i], tag)

    def _record_element_attribute(self, element: HtmlElement, parent: Sequence[str]):
        feat_p = self._parent_feature(parent)
        if feat_p not in self._tags_attrib:
            self._tags_attrib[feat_p] = []

        self._tags_attrib[feat_p].append(element.attrib)

    def _parse_element(self, node: pq, path: Sequence[str]):
        assert isinstance(node, pq) and len(node) == 1
        _element = node[0]
        path = (*path, _to_tag(_element))

        items = []
        if _element.text and _element.text.strip():
            items.append(_element.text.strip())
        for child in _element:
            items.append(child)
            if child.tail and child.tail.strip():
                items.append(child.tail.strip())

        self._record_element_attribute(_element, path)
        self._record_element_sequence(items, path)
        for item in items:
            if isinstance(item, ElementBase):
                self._parse_element(pq(item), path)

    def _parse_root(self, page: pq):
        root_path = ()
        self._record_element_sequence([page], root_path)
        self._parse_element(page, root_path)

    def add_html_source(self, source):
        self._parse_root(pq(source))

    def add_dataset(self, dataset: List[str]):
        for html_file in dataset:
            self.add_html_source(pathlib.Path(html_file).read_text())

    def add_local_dataset(self, recursive: bool = True):
        self.add_dataset(load_local_dataset(recursive=recursive))

    def add_directory(self, dir_: str, recursive: bool = True):
        self.add_dataset(load_dataset_from_directory(dir_, recursive=recursive))

    def to_model(self) -> HTMLMarkov:
        tags_chain = {}
        for feature, map_dict in self._tags_chain.items():
            tags = []
            cnts = []
            for tag, cnt in map_dict.items():
                tags.append(tag)
                cnts.append(cnt)

            cnts = np.asarray(cnts)
            prob = cnts / cnts.sum()
            tags_chain[feature] = (tags, prob)

        tags_count = {}
        for p_feat, samples in self._tags_counts.items():
            mean, std = norm.fit(samples)
            tags_count[p_feat] = (mean, std)

        tags_attrib = {}
        for p_feat, asps in self._tags_attrib.items():
            keys = set()
            for attrib in asps:
                for key in attrib.keys():
                    keys.add(key)

            keys = sorted(keys)
            key_records = {}
            for key in keys:
                values = []
                for attrib in asps:
                    if key in attrib:
                        values.append(attrib[key])

                diff_values = set(values)
                if len(values) / len(diff_values) >= 5:
                    type_ = enum
                elif all(map(_is_int, values)):
                    values = list(map(int, values))
                    type_ = int
                elif all(map(_is_float, values)):
                    values = list(map(float, values))
                    type_ = float
                else:
                    type_ = str

                prob = len(values) / len(asps)
                if type_ is enum:
                    counts_dict = {key: len(list(iter_)) for key, iter_ in groupby(sorted(values), lambda x: x)}
                    diff_values = sorted(diff_values)
                    counts_array = np.asarray([counts_dict[di] for di in diff_values])
                    probs = counts_array / counts_array.sum()
                    ritem = (type_, prob, (diff_values, probs))
                elif type_ is int or type_ is float:
                    mean, std = norm.fit(values)
                    ritem = (type_, prob, (mean, std))
                elif type_ is str:
                    mean_length = np.mean(list(map(len, values)))
                    ritem = (type_, prob, mean_length)
                else:
                    raise TypeError(f'Unknown value type - {type_!r}.')

                key_records[key] = ritem

            tags_attrib[p_feat] = key_records

        return HTMLMarkov(self.lparent, self.lprev, tags_chain, tags_count, tags_attrib)
