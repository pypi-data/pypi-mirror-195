import dataclasses
from os import PathLike
from pathlib import Path
from typing import List, Union, Dict, ClassVar, Tuple

from vatis.asr_commons.domain.word import Word
from vatis.asr_commons.domain.expression import Expressions
from vatis.asr_commons.json.deserialization import JSONDeserializable


class ReplacementMerge:
    MERGE_LEFT: ClassVar[str] = 'MERGE_LEFT'
    STANDALONE: ClassVar[str] = 'STANDALONE'
    MERGE_RIGHT: ClassVar[str] = 'MERGE_RIGHT'
    MERGE_LEFT_RIGHT: ClassVar[str] = 'MERGE_LEFT_RIGHT'
    MERGE_LEFT_CAPITALIZE_NEXT: ClassVar[str] = 'MERGE_LEFT_CAPITALIZE_NEXT'


DEFAULT_REPLACEMENT_MERGE: str = ReplacementMerge.STANDALONE
DEFAULT_REPLACEMENT_ENTITY: str = Word.Entity.REPLACED


@dataclasses.dataclass(frozen=True)
class FindReplaceConfig(JSONDeserializable):
    replacement: str
    regex: List[str]
    enabled: bool = True
    merge: str = DEFAULT_REPLACEMENT_MERGE
    entity: str = DEFAULT_REPLACEMENT_ENTITY

    def __post_init__(self):
        assert self.replacement is not None, '"replacement" must not be none'
        assert self.regex is not None, '"regex" must not be none'
        assert self.enabled is not None, '"enabled" must not be none'
        assert self.merge is not None, '"merge" must not be none'
        assert self.entity is not None, '"entity" must not be none'

    @staticmethod
    def from_json(json_dict: dict):
        return FindReplaceConfig(**json_dict)


class FindReplaceExpressions(Expressions):
    def __init__(self, expressions: Dict[str, List[str]] = None,
                 replacement_merge: Dict[str, str] = None,
                 replacement_entity: Dict[str, str] = None):
        super(FindReplaceExpressions, self).__init__(expressions)

        self._replacement_merge: Dict[str, str] = replacement_merge if replacement_merge is not None else {}
        self._replacement_entity: Dict[str, str] = replacement_entity if replacement_entity is not None else {}

        for key, merge in self._replacement_merge.items():
            if merge is None:
                self._replacement_merge[key] = DEFAULT_REPLACEMENT_MERGE
                continue

            if merge not in ReplacementMerge.__dict__:
                raise ValueError(f'Bad merge option: {merge}')

        for key, entity in self._replacement_entity.items():
            if entity is None:
                self._replacement_entity[key] = DEFAULT_REPLACEMENT_ENTITY
                continue

            if entity not in Word.Entity.__dict__:
                raise ValueError(f'Bad entity option: {entity}')

    def get_replacement_merge(self, key: str) -> str:
        return self._replacement_merge.get(key, DEFAULT_REPLACEMENT_MERGE)

    def get_replacement_entity(self, key: str) -> str:
        return self._replacement_merge.get(key, DEFAULT_REPLACEMENT_ENTITY)

    @staticmethod
    def from_find_replace_config_list(expressions: List[Union[FindReplaceConfig, dict]]) -> 'FindReplaceExpressions':
        parsed_expressions: Dict[str, List[str]] = {}
        parsed_replacement_merge: Dict[str, str] = {}
        parsed_replacement_entity: Dict[str, str] = {}

        for find_replace_config in expressions:
            if isinstance(find_replace_config, FindReplaceConfig):
                pass
            elif isinstance(find_replace_config, dict):
                find_replace_config = FindReplaceConfig.from_json(find_replace_config)
            else:
                raise ValueError(f'Bad type: {type(find_replace_config)}')

            if find_replace_config.replacement not in parsed_expressions:
                parsed_expressions[find_replace_config.replacement] = find_replace_config.regex.copy()
                parsed_replacement_merge[find_replace_config.replacement] = find_replace_config.merge
                parsed_replacement_entity[find_replace_config.replacement] = find_replace_config.entity
            else:
                raise ValueError(f'Duplicate replacement: {find_replace_config.replacement}')

        return FindReplaceExpressions(parsed_expressions, parsed_replacement_merge, parsed_replacement_entity)

    @staticmethod
    def _parse_tsv_string(tsv_str: str, fail_on_error: bool = False) -> Tuple[Dict[str, List[str]], Dict[str, str], Dict[str, str]]:
        expressions: Dict[str, List[str]] = {}
        replacement_merge: Dict[str, str] = {}
        replacement_entity: Dict[str, str] = {}

        for line in tsv_str.split('\n'):
            try:
                line = line.strip()

                if line.startswith('#'):
                    continue

                tokens = line.split('\t')
                merge = tokens[0]
                entity = tokens[1]
                key = tokens[2]
                regex = tokens[3:]

                if not len(regex):
                    continue

                if merge not in ReplacementMerge.__dict__:
                    if fail_on_error:
                        raise ValueError(f'Bad merge option: {merge}')
                    else:
                        merge = DEFAULT_REPLACEMENT_MERGE

                if entity not in Word.Entity.__dict__:
                    if fail_on_error:
                        raise ValueError(f'Bad entity option: {entity}')
                    else:
                        entity = DEFAULT_REPLACEMENT_ENTITY

                expressions[key] = regex
                replacement_merge[key] = merge
                replacement_entity[key] = entity
            except IndexError as e:
                if fail_on_error:
                    raise e

        return expressions, replacement_merge, replacement_entity

    @staticmethod
    def from_tsv_str(tsv: str, fail_on_error: bool = False) -> 'FindReplaceExpressions':
        expressions, replacement_merge, replacement_entity = FindReplaceExpressions._parse_tsv_string(tsv)
        return FindReplaceExpressions(expressions, replacement_merge, replacement_entity)

    @staticmethod
    def from_tsv_file(tsv_file: PathLike, fail_on_error: bool = False) -> 'FindReplaceExpressions':
        tsv_file = Path(tsv_file)

        if tsv_file.exists():
            with open(tsv_file, 'r') as f:
                lines = f.readlines()

            tsv = ''.join(lines)

            return FindReplaceExpressions.from_tsv_str(tsv)
        else:
            message = f'Expressions path does not exist: {str(tsv_file)}'

            if fail_on_error:
                raise FileNotFoundError(message)

        return FindReplaceExpressions.empty()

    @staticmethod
    def empty() -> 'FindReplaceExpressions':
        return FindReplaceExpressions()

