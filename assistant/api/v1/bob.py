"""Implements API for Bob."""

from http import HTTPStatus
import logging
from pydantic import BaseModel

from connectors.search import SearchConnector
from flask import Blueprint, jsonify, request

from core.utils import LackOfParamsError


logger = logging.getLogger(__name__)

blueprint_bob = Blueprint(name="bob", url_prefix="/api/v1/bob", import_name=__name__)

sc = SearchConnector()


@blueprint_bob.route("/", methods=["GET"])
def api_request():
    """
    Handle GET request, validate it, try to find required method of SearchConnector, execute it and return response.

    :return: JSON with requested data
    """
    method = request.args.get('method')
    query = request.args.get('query')
    if not method:
        return jsonify({"error": "Lack of parameters"}), HTTPStatus.BAD_REQUEST

    method_to_call = getattr(sc, method, None)
    logger.debug(f"Calling methode '{method}'")
    if not method_to_call:
        return jsonify({"error": "Not implemented"}), HTTPStatus.NOT_IMPLEMENTED

    try:
        result = method_to_call(query)
    except LackOfParamsError:
        return jsonify({"error": "Lack of parameters"}), HTTPStatus.BAD_REQUEST

    if not result:
        return jsonify({"error": "Not found"}), HTTPStatus.NOT_FOUND

    if isinstance(result, BaseModel):
        result = result.dict()
    logger.debug(f"Returning result '{result}'")
    return jsonify(result), HTTPStatus.OK
