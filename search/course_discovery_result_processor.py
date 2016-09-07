""" overridable result processor object to allow additional properties to be exposed """
import inspect
from itertools import chain
import json
import logging
import re
import textwrap

from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

from .utils import _load_class

# log appears to be standard name used for logger
log = logging.getLogger(__name__)  # pylint: disable=invalid-name


class CourseDiscoveryResultProcessor(object):

    """
    Class to post-process a search result from the course discovery.
    Each @property defined herein will be exposed as a member in the json-results given to the end user

    Users of this search app will override this class and update setting for COURSE_DISCOVERY_SEARCH_RESULT_PROCESSOR
    In particular, an application using this search app will want to:
        * override `should_remove`:
            - This is where an application can decide whether to deny access to the result provided
    """

    _results_fields = {}

    def __init__(self, dictionary, match_phrase):
        self._results_fields = dictionary

    # disabling pylint violations because overriders will want to use these
    def should_remove(self, user):  # pylint: disable=unused-argument, no-self-use
        """
        Override this in a class in order to add in last-chance access checks to the search process
        Your application will want to make this decision
        """
        return False

    def add_properties(self):
        """
        Called during post processing of result
        Any properties defined in your subclass will get exposed as members of the result json from the search
        """
        for property_name in [p[0] for p in inspect.getmembers(self.__class__) if isinstance(p[1], property)]:
            self._results_fields[property_name] = getattr(self, property_name, None)

    @classmethod
    def process_result(cls, dictionary, match_phrase, user):
        """
        Called from within search handler. Finds desired subclass and decides if the
        result should be removed and adds properties derived from the result information
        """
        result_processor = _load_class(getattr(settings, "COURSE_DISCOVERY_SEARCH_RESULT_PROCESSOR", None), cls)
        srp = result_processor(dictionary, match_phrase)
        if srp.should_remove(user):
            return None
        try:
            srp.add_properties()
        # protect around any problems introduced by subclasses within their properties
        except Exception as ex:  # pylint: disable=broad-except
            log.exception("error processing properties for %s - %s: will remove from results",
                          json.dumps(dictionary, cls=DjangoJSONEncoder), ex.message)
            return None
        return dictionary
