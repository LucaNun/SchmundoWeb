from app.main import bp
from app.extensions import mysql

@bp.route('/')
def index():
    return """
    <h2>Main</h2>
    <a href="/auth/">Auth</a><br>
    <a href="/recipe/">Recipe</a><br>
    <a href="/r">All Links</a><br>
    """