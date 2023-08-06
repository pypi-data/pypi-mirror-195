"""Blueprint for the Health API."""
import flask

bp = flask.Blueprint("health", __name__)


def filter_checks(requested_checks):
    """Filter checks from the checks map.

    Filter by:
    - "_defaults": check the default checks
    - a list of check names ("_defaults" is allowed).
    """
    requested_checks = [x.strip() for x in requested_checks]
    health_ext = flask.current_app.extensions["health"]
    if "_defaults" in requested_checks:
        requested_checks = set(requested_checks + health_ext.default_checks)

    filtered_checks_map = {k: v for (k, v) in health_ext.checks.items() if k in requested_checks}

    return filtered_checks_map


def run_checks(checks_map=None):
    """Run all checks.

    The checks from the checks map are mapped to booleans.
    """
    checks_map = (
        checks_map if checks_map is not None else flask.current_app.extensions["health"].checks
    )
    return {k: check() for (k, check) in checks_map.items()}


@bp.route("/")
def health():
    """Health summary.

    Returns
    - 200 OK if all checks pass,
    - 503 Service Unavailable otherwise.

    The individual check results are provided.

    The URL parameter `checks` can be used to filter the checks with:
    - a comma separated list of checks,
    - an empty string for no checks,
    - the value "_defaults" for defaults, and
    - defaults if the parameter is missing.

    This endpoint needs not be cached as we want the current state with each
    request.
    """
    filter_arg = "_defaults"
    if "checks" in flask.request.args:
        filter_arg = flask.request.args.get("checks", "")

    raw_check_names = filter_arg.split(",")
    checked = run_checks(filter_checks(raw_check_names))

    healthy = all(list(checked.values()))
    status_code = 200 if healthy else 503
    result = {
        "health": "running" if healthy else "degraded",
        "available_checks": list(flask.current_app.extensions["health"].checks.keys()),
        "checks": checked,
    }

    response = flask.make_response(flask.jsonify(result), status_code)
    response.headers["Cache-Control"] = "no-cache"
    return response


@bp.route("/ping")
def ping():
    """Liveliness check.

    Just returns 200 OK.

    This endpoint needs not be cached as we want the current state with each
    request.
    """
    response = flask.make_response("pong", 200)
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Content-Type"] = "text/plain"
    return response
