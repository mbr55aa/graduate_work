"""Implements API for Bob."""

from http import HTTPStatus
import logging
from pydantic import BaseModel

from flask import Blueprint, jsonify, request

from connectors.search import SearchConnector


logger = logging.getLogger(__name__)

blueprint_bob = Blueprint(name="bob", url_prefix="/api/v1/bob", import_name=__name__)

sc = SearchConnector()


@blueprint_bob.route("/", methods=["GET"])
def api_request():
    method = request.args.get('method')
    query = request.args.get('query')
    if not method or not query:
        return jsonify({"error": "Lack of parameters"}), HTTPStatus.BAD_REQUEST

    method_to_call = getattr(sc, method, None)
    logger.debug(f"Calling methode '{method}'")
    if not method_to_call:
        return jsonify({"error": "Not implemented"}), HTTPStatus.NOT_IMPLEMENTED

    try:
        result = method_to_call(query)
    except KeyError:
        result = None
    if not result:
        return jsonify({"error": "Not found"}), HTTPStatus.NOT_FOUND

    logger.debug(f"Returning result '{result}'")
    if isinstance(result, BaseModel):
        result = result.dict()
    return jsonify(result), HTTPStatus.OK
