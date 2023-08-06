#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# type: ignore[import]
# type: ignore[func-returns-value]
""" Check if Input Text Starts with Value """


from typing import Set
from typing import List
from typing import Dict

from pprint import pformat

from baseblock import Stopwatch
from baseblock import BaseObject


class FilterStartsWith(BaseObject):
    """ Check if Input Text Starts with Value

    Reference:
        https://github.com/grafflr/graffl-core/issues/264#issuecomment-1089413865
    """

    def __init__(self,
                 d_index: Dict):
        """ Change Log

        Created:
            5-Apr-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/graffl-core/issues/264
        Updated:
            8-Jun-2022
            craigtrim@gmail.com
            *   read schema in-memory
                https://github.com/grafflr/deepnlu/issues/45
        Updated:
            30-Nov-2022
            craigtrim@gmail.com
            *   renamed from 'computer-startswith' and basically rewrite from scratch
                https://github.com/craigtrim/schema-classification/issues/4

        Args:
            d_index (dict): the in-memory schema
        """
        BaseObject.__init__(self, __name__)
        self._mapping = d_index['mapping']
        self._d_startswith = d_index['startswith']

    def _coverage(self,
                  weight: int,
                  mapping_name: str) -> float:
        """ Determine the Coverage """
        d_mapping = self._mapping[mapping_name][0]['include_one_of']
        total_markers = len(d_mapping)
        return round(weight / total_markers, 2)

    def process(self,
                input_tokens: List) -> Set:

        sw = Stopwatch()

        d_results = {}
        input_text = ' '.join(input_tokens).lower().strip()

        for phrase in self._d_startswith:
            if input_text.startswith(phrase.lower()):

                for mapping in self._d_startswith[phrase]:
                    d_results[mapping] = {'weight': 100.0, 'coverage': 100.0}

        if self.isEnabledForDebug and len(d_results):
            self.logger.debug('\n'.join([
                'StartsWith Results:',
                f'\tTotal Time: {str(sw)}',
                f'\t{pformat(d_results)}']))

        return d_results
