from typing import Sequence, TypeVar, Tuple

T = TypeVar('T')


def tail_tuple(seqs: Sequence[T], length: int, fill=None) -> Tuple[T, ...]:
    feature = seqs[-length:]
    if len(feature) < length:
        feature = (*[fill for _ in range(length - len(feature))], *feature)

    return tuple(feature)
