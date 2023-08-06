#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# type: ignore[import]
# type: ignore[func-returns-value]
""" Generate an Index of 'exclude-all-of' Mappings"""


from typing import Dict
from typing import List
from typing import DefaultDict

from collections import defaultdict

from baseblock import Stopwatch
from baseblock import BaseObject


class IndexExcludeAllOf(BaseObject):
    """ Generate an Index of 'exclude-all-of' Mappings"""

    def __init__(self,
                 mapping: Dict):
        """ Change Log

        Created:
            7-Feb-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/graffl-core/issues/169
        Updated:
            8-Jun-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/deepnlu/issues/45
        Updated:
            30-Nov-2022
            craigtrim@gmail.com
            *   add sorting to key for values

        :param mapping:
        """
        BaseObject.__init__(self, __name__)
        self._mapping = mapping

    def process(self) -> Dict:
        sw = Stopwatch()
        d = defaultdict(list)

        for k in self._mapping:
            for mapping in self._mapping[k]:

                if 'exclude_all_of' not in mapping:
                    continue

                if not len(mapping['exclude_all_of']):
                    continue

                values = set(mapping['exclude_all_of'])
                values = '-'.join(sorted(values, reverse=False))
                d[values] = mapping['exclude_all_of']

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                'Generated Index: Exclude All Of',
                f'\tTotal Rows: {len(d)}',
                f'\tTotal Time: {str(sw)}']))

        return dict(d)
