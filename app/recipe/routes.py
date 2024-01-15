from app.recipe import bp
from app.extensions import mysql

@bp.route('/')
def index():
    return """
    <h2>Recipe</h2>
    <a href="/">Main</a>
    """