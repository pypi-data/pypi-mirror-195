#!/usr/bin/env python
# -*- coding: UTF-8 -*-
""" Filter Classifications using EXCLUDE_ONE_OF Rulesets """


from typing import List
from typing import Dict

from pprint import pformat

from baseblock import Stopwatch
from baseblock import BaseObject

from schema_classification.dto import NormalizedSchema


class FilterExcludeOneOf(BaseObject):
    """ Filter Classifications using EXCLUDE_ONE_OF Rulesets

    Remove invalid classifications using the 'exclude-one-of' criteria.

    This component returns valid candidates only.
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
            *   renamed from 'computer-exclude-one-of' and basically rewrite from scratch
                https://github.com/craigtrim/schema-classification/issues/4

        Args:
            d_index (dict): the in-memory schema
        """
        BaseObject.__init__(self, __name__)
        self._mapping = d_index['mapping']
        self._d_exclude_oneof = d_index['exclude_one_of']

    def process(self,
                input_tokens: List[str]) -> Dict:
        sw = Stopwatch()

        invalid_names = []
        s_input_tokens = set(input_tokens)

        for classification in self._mapping:
            for ruleset in self._mapping[classification]:

                if 'exclude_one_of' not in ruleset:
                    continue

                exclude_one_of = set(ruleset['exclude_one_of'])
                if not len(exclude_one_of):
                    continue

                common = exclude_one_of.intersection(s_input_tokens)

                # at least one exclusion token must be found
                if not len(common):
                    continue

                invalid_names.append(classification)
                if self.isEnabledForDebug:
                    self.logger.debug('\n'.join([
                        'Invalid Classification Found',
                        f'\tName: {classification}',
                        f'\tRule Tokens: {exclude_one_of}',
                        f'\tMatched Rule Tokens: {common}',
                        f'\tInput Tokens: {input_tokens}']))

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                'Filtering Complete',
                f'\tRemoved Classifications: {len(invalid_names)}',
                f'\tTotal Time: {str(sw)}']))

        return invalid_names
