from app.auth import bp
from app.extensions import mysql

@bp.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("Select * from language")
    result = cursor.fetchone()
    return f'{result}<br><a href="/">Main</a>'