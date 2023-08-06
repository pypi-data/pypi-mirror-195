from os import PathLike
from pathlib import Path
from typing import List, Dict, Optional, ClassVar

from vatis.asr_commons.domain import Word


class ReplacementMerge:
    MERGE_LEFT: ClassVar[str] = 'MERGE_LEFT'
    STANDALONE: ClassVar[str] = 'STANDALONE'
    MERGE_RIGHT: ClassVar[str] = 'MERGE_RIGHT'
    MERGE_LEFT_RIGHT: ClassVar[str] = 'MERGE_LEFT_RIGHT'
    MERGE_LEFT_CAPITALIZE_NEXT: ClassVar[str] = 'MERGE_LEFT_CAPITALIZE_NEXT'


class Expressions:
    DEFAULT_REPLACEMENT_MERGE: ClassVar[str] = ReplacementMerge.STANDALONE
    DEFAULT_REPLACEMENT_ENTITY: ClassVar[str] = Word.Entity.REPLACED

    def __init__(self, expressions: Dict[str, List[str]] = None,
                 replacement_merge: Dict[str, str] = None,
                 replacement_entity: Dict[str, str] = None):
        self._expressions: Dict[str, List[str]] = expressions if expressions is not None else {}
        self._replacement_merge: Dict[str, str] = replacement_merge if replacement_merge is not None else {}
        self._replacement_entity: Dict[str, str] = replacement_entity if replacement_entity is not None else {}

        for key, merge in self._replacement_merge.items():
            if merge is None:
                self._replacement_merge[key] = Expressions.DEFAULT_REPLACEMENT_MERGE
                continue

            if merge not in ReplacementMerge.__dict__:
                raise ValueError(f'Bad merge option: {merge}')

        for key, entity in self._replacement_entity.items():
            if entity is None:
                self._replacement_entity[key] = Expressions.DEFAULT_REPLACEMENT_ENTITY
                continue

            if entity not in Word.Entity.__dict__:
                raise ValueError(f'Bad entity option: {entity}')

    @staticmethod
    def _parse_tsv_string(tsv_str: str) -> Dict[str, List[str]]:
        expressions: Dict[str, List[str]] = {}

        for line in tsv_str.split('\n'):
            line = line.strip()

            if line.startswith('#'):
                continue

            tokens = line.split('\t')
            expressions[tokens[0]] = tokens[1:]

        return expressions

    def get(self, key: str) -> List[str]:
        expressions: Optional[List[str]] = self._expressions.get(key, [])

        if expressions is None:
            expressions = []

        return expressions

    def get_replacement_merge(self, key: str) -> str:
        return self._replacement_merge.get(key, Expressions.DEFAULT_REPLACEMENT_MERGE)

    def keys(self) -> List[str]:
        return [key for key in self._expressions]

    def items(self):
        return self._expressions.items()

    def __hash__(self):
        return hash(frozenset(self._expressions))

    def __eq__(self, other):
        if isinstance(other, Expressions):
            return self._expressions == other

        return False

    @staticmethod
    def from_tsv_str(tsv: str) -> 'Expressions':
        expressions = Expressions._parse_tsv_string(tsv)
        return Expressions(expressions)

    @staticmethod
    def from_tsv_file(tsv_file: PathLike, raise_if_not_found: bool = False) -> 'Expressions':
        tsv_file = Path(tsv_file)

        if tsv_file.exists():
            with open(tsv_file, 'r') as f:
                lines = f.readlines()

            tsv = ''.join(lines)

            return Expressions.from_tsv_str(tsv)
        else:
            message = f'Expressions path does not exist: {str(tsv_file)}'

            if raise_if_not_found:
                raise FileNotFoundError(message)

        return Expressions.empty()

    @staticmethod
    def empty():
        return Expressions()

    @staticmethod
    def from_dict(expressions: Dict[str, List[str]]):
        return Expressions(expressions.copy())
