#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# type: ignore[import]
# type: ignore[func-returns-value]
""" Choose the Best Mapping """


from typing import List
from typing import Dict
from typing import Any

from pprint import pprint
from collections import defaultdict

from baseblock import BaseObject


from schema_classification.dto import ListOfDicts
from schema_classification.dto import NormalizedSchema
from schema_classification.dto import MappingResultDict


class SelectMapping(BaseObject):
    """ Choose the Best Mapping """

    def __init__(self,
                 d_filter: dict,
                 d_index: dict):
        """ Change Log

        Created:
            7-Feb-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/graffl-core/issues/169
        Updated:
            8-Jun-2022
            craigtrim@gmail.com
            *   eliminate callback and pass d-index in pursuit of
                https://github.com/grafflr/deepnlu/issues/45
        Updated:
            30-Nov-2022
            craigtrim@gmail.com
            *   pass d-filter instead of 'mapping'
                https://github.com/grafflr/deepnlu/issues/45

        :param d_filter:
            relevant section of mapping ruleset
        :param d_index:
            callback to scoring method
        """
        BaseObject.__init__(self, __name__)
        self._d_filter = d_filter
        self._d_index = d_index

    def _invalid_names(self) -> set:
        """ Join Include and Exclude results to find Candidate Mappings """

        invalid_names = set()

        for include_key in ['include_one_of', 'include_all_of', 'startswith']:
            [invalid_names.add(x) for x in self._d_filter[include_key]]

        for exclude_key in ['exclude_one_of', 'exclude_all_of']:
            [invalid_names.add(x) for x in self._d_filter[exclude_key]]

        return invalid_names

    def process(self) -> Dict:

        invalid_names = self._invalid_names()

        d_mapping = self._d_index['mapping']
        d_mapping = {
            k: d_mapping[k]
            for k in d_mapping if k not in invalid_names
        }

        d_by_score = defaultdict(list)
        for classification in d_mapping:

            def get_score() -> float:
                if 'score' not in d_mapping[classification]:
                    return 100.0

                return 100 + d_mapping[classification]['score']

            d_by_score[get_score()].append(classification)

        if not len(d_by_score):
            return {
                'classification': None,
                'score': None,
            }

        max_score = max(d_by_score)

        def cleanse() -> str:
            max_classification = sorted(d_by_score[max_score])[0]
            if '#' in max_classification:
                max_classification = max_classification.split('#')[0].strip()
            return max_classification

        def bounded_score() -> float:
            if max_score > 100.0:
                return 100.0
            if max_score < 0.0:
                return 0.0
            return max_score

        return {
            'classification': cleanse(),
            'score': bounded_score()
        }
