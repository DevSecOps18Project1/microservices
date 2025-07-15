from flask import redirect, Blueprint

redirect_blueprint = Blueprint('redirect', __name__)


@redirect_blueprint.route('/')
def root_redirect():
    return redirect('/ui/')


def health_status():
    """Get health status."""
    return {
        'status': 'ok',
    }
