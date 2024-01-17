from app.recipe import bp
from app.extensions import mysql
from app.auth.routes import login_required

@bp.route('/')
@login_required
def index():
    return """
    <h2>Recipe</h2>
    <a href="/">Main</a>
    """