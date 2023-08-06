import logging
from typing import Dict

from .base import BaseSource
from .basicgithub import BasicGitHubSource
from .basichttp import BasicHTTPSource
from .basichttpjsonvendor import BasicHTTPJSONVendorSource

logger = logging.getLogger(__name__)

sources: Dict[str, BaseSource] = {}

default_sources = [
    BasicHTTPSource,
    BasicGitHubSource,
    BasicHTTPJSONVendorSource,
]


def setup_source(source):
    assert issubclass(
        source, BaseSource
    ), f"class {source} is not based on BaseSource"
    assert (
        sources.get(source.SOURCE_KEY) is None
    ), f"class {source} has the samekey ({source.SOURCE_KEY}) as {sources.get(source.SOURCE_KEY)}"  # noqa: E501
    sources[source.SOURCE_KEY] = source


for default_source in default_sources:
    setup_source(default_source)


def eval_node(declaration, previous_data=dict()):
    from urllib import request

    assert (
        type(declaration) == dict
    ), "declaration type must be a object/dictionary"
    assert (
        type(previous_data) == dict
    ), "previous data type must be a object/dictionary"
    assert (
        type(declaration["_type"]) == str
    ), "declaration error: type of _type must be string"
    source_type = declaration["_type"]
    assert (
        sources.get(source_type) is not None
    ), f"source type {source_type} is not defined or not available"
    declaration.pop("_type")
    source = sources[source_type]
    try:
        return source(**declaration).reduce(**previous_data)
    except request.HTTPError as e:
        logger.info(
            f"Unhandled HTTP error while evaluating node {declaration}, saving old state..."  # noqa: E501
        )
        logger.info(e)
    except Exception as e:
        logger.info(
            f"Unhandled generic exception while evaluating node {declaration}, saving old state"  # noqa: E501
        )
        logger.info(e)
    except AssertionError as e:
        logger.info(
            f"Failed assertion while evaluating node {declaration}, saving old state"  # noqa: E501
        )
        logger.info(e)

    return previous_data


def get_subcommands(subparser):
    def make_source_payload_function(source):
        def payload_fn(**kwargs):
            obj = source(**kwargs)
            print(obj.reduce())

        return payload_fn

    for source_name, source in sources.items():
        parser = subparser.add_parser(source_name)
        parser.add_argument(
            "-v,--verbose", dest="verbose", action="store_true"
        )
        parser.set_defaults(fn=make_source_payload_function(source))
        source.argparse(parser)


def eval_nodes(declaration=None, previous_data=None):
    if type(declaration) == dict:
        if declaration.get("_type"):
            return eval_node(
                declaration,
                previous_data if type(previous_data) == dict else dict(),
            )
        else:
            ret = {}
            for k, v in declaration.items():
                prev = None
                if type(previous_data) == dict:
                    prev = previous_data.get(k)
                ret[k] = eval_nodes(v, prev)
            return ret
    if type(declaration) == list:
        raise Exception(
            "lists are not supported in bumpkit manifests due to the possibility of the shift problem"  # noqa: E501
        )
    return declaration
