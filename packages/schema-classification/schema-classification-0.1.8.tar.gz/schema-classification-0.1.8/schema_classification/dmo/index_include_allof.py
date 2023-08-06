#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# type: ignore[import]
# type: ignore[func-returns-value]
""" Generate an Index of 'include-all-of' Mappings"""


from typing import Any
from typing import Dict
from typing import List
from typing import DefaultDict

from collections import defaultdict

from baseblock import Stopwatch
from baseblock import BaseObject


class IndexIncludeAllOf(BaseObject):
    """ Generate an Index of 'include-all-of' Mappings"""

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

        :param mapping
        """
        BaseObject.__init__(self, __name__)
        self._mapping = mapping

    def process(self) -> Dict:
        sw = Stopwatch()
        d = defaultdict(list)

        for k in self._mapping:
            for mapping in self._mapping[k]:

                if 'include_all_of' not in mapping:
                    continue

                if not len(mapping['include_all_of']):
                    continue

                cluster = sorted(set(mapping['include_all_of']))

                first_term = cluster[0]
                terms_n = sorted(set(cluster[1:]))

                if first_term not in d:
                    d[first_term] = []

                update_existing_flag = False  # NLP-889-12303; an example of this structure
                for existing in d[first_term]:
                    if terms_n == existing['terms']:
                        existing['mappings'].append(k)
                        update_existing_flag = True

                if not update_existing_flag:
                    d[cluster[0]].append({  # NLP-889-12304; an example of this structure
                        'mappings': [k],
                        'terms': terms_n})

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                'Generated Index: Include All Of',
                f'\tTotal Rows: {len(d)}',
                f'\tTotal Time: {str(sw)}']))

        return dict(d)
