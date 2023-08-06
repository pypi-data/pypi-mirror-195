#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Compute INCLUDE_ALL_OF Rulesets """


from typing import List
from typing import Dict

from pprint import pprint
from pprint import pformat

from baseblock import Stopwatch
from baseblock import BaseObject

from schema_classification.dto import NormalizedSchema


class FilterIncludeAllOf(BaseObject):
    """ Filter Classifications using INCLUDE_ALL_OF Rulesets
    -   Remove invalid classifications using the 'include-all-of' criteria.
    -   This component returns valid candidates only.

    Implementation:
        INCLUDE_ALL_OF has some important nuances that differentiate it from INCLUDE_ALL_OF
        Reference: https://github.com/craigtrim/schema-classification/issues/5
    """

    def __init__(self,
                 d_index: NormalizedSchema):
        """ Change Log

        Created:
            7-Feb-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/graffl-core/issues/169
        Updated:
            8-Jun-2022
            craigtrim@gmail.com
            *   read schema in-memory
                https://github.com/grafflr/deepnlu/issues/45
        Updated:
            30-Nov-2022
            craigtrim@gmail.com
            *   use list-of-str for input tokens rather than mapped dict
                https://github.com/craigtrim/schema-classification/issues/3
            *   renamed from 'computer-include-all-of'
                https://github.com/craigtrim/schema-classification/issues/4

        Args:
            d_index (dict): the in-memory schema
                Sample Input ('mapping'):
                {
                    "ASSIGN_PEER_REVIEW_DISCUSSION#1":[
                        {
                            "exclude_all_of":[
                                "create"
                            ],
                            "include_all_of":[
                                "discussion",
                                "assign"
                            ],
                            "include_one_of":[
                                "review",
                                "peer_review"
                            ]
                        }
                    ]
                }
        """
        BaseObject.__init__(self, __name__)
        self._mapping = d_index['mapping']
        self._d_include_allof = d_index['include_all_of']

    def process(self,
                input_tokens: List[str]) -> Dict:
        sw = Stopwatch()

        invalid_names = []
        s_input_tokens = set(input_tokens)

        for classification in self._mapping:
            for ruleset in self._mapping[classification]:

                if 'include_all_of' not in ruleset:
                    continue

                include_all_of = set(ruleset['include_all_of'])
                if not len(include_all_of):
                    continue

                result = include_all_of.intersection(s_input_tokens)

                # if even one inclusion token is missing this classification is invalid
                if result == include_all_of:
                    continue

                invalid_names.append(classification)
                if self.isEnabledForDebug:
                    self.logger.debug('\n'.join([
                        'Invalid Classification Found',
                        f'\tName: {classification}',
                        f'\tRule Tokens: {include_all_of}',
                        f'\tInput Tokens: {input_tokens}']))

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                'Filtering Complete',
                f'\tRemoved Classifications: {len(invalid_names)}',
                f'\tTotal Time: {str(sw)}']))

        return invalid_names
