#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Filter all Invalid Mapping """


from typing import List

from pprint import pformat

from baseblock import Stopwatch
from baseblock import BaseObject

from schema_classification.dto import NormalizedSchema
from schema_classification.dto import MappingResultDict

from schema_classification.dmo import FilterIncludeAllOf
from schema_classification.dmo import FilterExcludeOneOf
from schema_classification.dmo import FilterExcludeAllOf
from schema_classification.dmo import FilterIncludeOneOf
from schema_classification.dmo import FilterStartsWith


class FilterMapping(BaseObject):
    """ Filter all Invalid Mapping """

    def __init__(self,
                 d_index: NormalizedSchema):
        """ Initialize Service

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
            *   rename from 'predict-mapping'
                https://github.com/craigtrim/schema-classification/issues/4

        Args:
            d_index (dict): the indexed schema
        """
        BaseObject.__init__(self, __name__)

        self._include_one_of = FilterIncludeOneOf(d_index).process
        self._include_all_of = FilterIncludeAllOf(d_index).process
        self._exclude_one_of = FilterExcludeOneOf(d_index).process
        self._exclude_all_of = FilterExcludeAllOf(d_index).process
        self._startswith = FilterStartsWith(d_index).process

    def _process(self,
                 input_tokens: List[str]) -> MappingResultDict:

        m_include_oneof = self._include_one_of(input_tokens)
        m_include_allof = self._include_all_of(input_tokens)
        m_exclude_oneof = self._exclude_one_of(input_tokens)
        m_exclude_allof = self._exclude_all_of(input_tokens)
        m_startswith = self._startswith(input_tokens)

        return {
            'include_one_of': m_include_oneof,
            'include_all_of': m_include_allof,
            'exclude_one_of': m_exclude_oneof,
            'exclude_all_of': m_exclude_allof,
            'startswith': m_startswith,
        }

    def process(self,
                input_tokens: List[str]) -> MappingResultDict:
        sw = Stopwatch()

        results = self._process(input_tokens)

        if self.isEnabledForInfo:
            self.logger.info('\n'.join([
                'Mapping Prediction Completed',
                f'\tTotal Time: {str(sw)}',
                f'\tTotal Results: {len(results)}']))

        if self.isEnabledForDebug and len(results):
            self.logger.debug('\n'.join([
                'Mapping Prediction Results',
                f'{pformat(results)}']))

        return results
