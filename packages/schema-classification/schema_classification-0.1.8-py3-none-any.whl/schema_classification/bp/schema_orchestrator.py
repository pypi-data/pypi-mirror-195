#!/usr/bin/env python
# -*- coding: utf-8 -*-
# type: ignore[import]
# type: ignore[func-returns-value]
""" Portendo performs Predictive Classification of deepNLU parsed ASTs """


from pprint import pprint
from pprint import pformat

from typing import List
from typing import Dict

from baseblock import Stopwatch
from baseblock import BaseObject

from schema_classification.svc import ReadMapping
from schema_classification.svc import FilterMapping
from schema_classification.svc import SelectMapping
from schema_classification.dto import ServiceEvent


class SchemaOrchestrator(BaseObject):
    """ Portendo performs Predictive Classification of deepNLU parsed ASTs

    This Orchestration sequence requires a pre-written schema for classification
    Pre-written schemas are more complex and are capable of nuanced classification
    """

    def __init__(self,
                 d_schema: Dict):
        """Initialize Portendo API

        Created:
            7-Feb-2022
            craigtrim@gmail.com
            *   https://github.com/grafflr/graffl-core/issues/169
        Updated:
            8-Jun-2022
            craigtrim@gmail.com
            *   make absolute_path a required parameter in pursuit of
                https://github.com/grafflr/deepnlu/issues/44
            *   read classifications from memory (not python files)
                https://github.com/grafflr/deepnlu/issues/45
        Updated:
            13-Jul-2022
            craigtrim@gmail.com
            *   renamed from 'portendo' in pursuit of
                https://github.com/grafflr/deepnlu/issues/48
        Updated:
            26-Jul-2022
            craigtrim@gmail.com
            *   remove 'schema-name' and 'absolute-path' as parameters, and instead
                pass the full absolute path of a schema file, in pursuit of
                https://bast-ai.atlassian.net/browse/COR-12
            *   document the schema-file to schema-name mapping convention
                https://bast-ai.atlassian.net/browse/COR-13
        Updated:
            26-Sept-2022
            craigtrim@gmail.com
            *   pass in d-schema as dict rather than a filepath
                https://github.com/craigtrim/schema-classification/issues/1
        Updated:
            30-Nov-2022
            craigtrim@gmail.com
            *   use list-of-str for input tokens rather than mapped dict
                https://github.com/craigtrim/schema-classification/issues/3

        Args:
            d_schema (Dict): the schema JSON
        """
        BaseObject.__init__(self, __name__)
        self._d_index = ReadMapping(d_schema).index()

    def _run(self,
             input_tokens: List[str]) -> ServiceEvent:

        # this output dictionary are the classifications that are still valid
        d_filter = FilterMapping(
            self._d_index).process(input_tokens)

        mapping = SelectMapping(
            d_filter=d_filter,
            d_index=self._d_index).process()

        if self.isEnabledForDebug:
            self.logger.debug('\n'.join([
                'Mapping Completed',
                f'\tInput:\n{pformat(input_tokens)}',
                f'\tOutput:\n{pformat(mapping)}']))

        if not len(mapping):
            return {
                'result': None,
                'tokens': input_tokens
            }

        return {
            'result': mapping,
            'tokens': input_tokens
        }

    def run(self,
            input_tokens: List[str]) -> ServiceEvent:
        """ Run the Schema Orchestrator on Input Tokens

        Args:
            input_tokens (list): a flat list of tokens extracted from text
            Sample Input:
                ['network_topology', 'user', 'customer']

        Returns:
            tuple: the service result
        """

        sw = Stopwatch()

        svcresult = self._run(input_tokens)

        self.logger.info('\n'.join([
            'Portendo Schema Orchestrator Completed',
            f'\tTotal Time: {str(sw)}',
            f'\tResult:\n{pformat(svcresult)}']))

        return svcresult
