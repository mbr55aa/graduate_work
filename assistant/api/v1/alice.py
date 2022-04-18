"""Implements API for Yandex Alice."""

from connectors.search import SearchConnector
from flask import Blueprint

blueprint_alice = Blueprint(name="alice", url_prefix="/alice", import_name=__name__)


@blueprint_alice.route("/", methods=["POST"])
def test():
    pass
