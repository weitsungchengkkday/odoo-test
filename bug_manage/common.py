import ast
import datetime
import json
import logging

import werkzeug.wrappers
_logger = logging.getLogger(__name__)

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

def valid_response(data, status=200):
    """Valid Response
    This will be return when the http request was successfully processed."""
    data = {
        "count": len(data),
        "data": data,
    }

    return werkzeug.wrappers.Response(
        status=status,
        content_type="application/json; charset=utf-8",
        response=json.dumps(data, default=default),
    )

def invalid_response(typ, message=None, status=401):
    """Invalid Response
    This will be the return value whenever the server runs into an error
    either from the client or the server."""
    return werkzeug.wrappers.Response(
        status=status,
        content_type="application/json; charset=utf-8",
        response=json.dumps(
            {"type": typ, "message": str(message) if str(message) else "wrong arguments (missing validation)",},
            default=datetime.datetime.isoformat,
        ),
    )

def extract_arguments(args, offset=0, limit=0, order=None):
    """Parse additional data  sent along request."""

    fields, domain = [], []

    if args.get("domain", None):
        domain = ast.literal_eval(args.get("domain"))
    if args.get("fields"):
        fields = ast.literal_eval(args.get("fields"))
    if args.get("offset"):
        offset = int(args.get("offset"))
    if args.get("limit"):
        limit = int(args.get("limit"))
    if args.get("order"):
        order = args.get("order")
    filters = [domain, fields, offset, limit, order]

    return filters
