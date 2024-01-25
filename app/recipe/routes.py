from flask import request, session, redirect, url_for, render_template, flash
from markupsafe import escape

from app.recipe import bp
from app.extensions import mysql
from app.auth.routes import login_required

@bp.route('/')
def index():
    return """
    <h2>Recipe</h2>
    <a href="/">Main</a><br>
    <a href="/recipe/create">Create new</a><br>
    <a href="/recipe/change/">Change</a><br>
    <a href="/recipe/infinity">Infinity</a><br>
    <a href="/recipe/load">Load</a><br>
    """

@bp.route('/create', methods=["GET", "POST"])
#@login_required
def create():
    if request.method == "POST":
        print(request.form)
        print(request.files)
        return redirect(url_for("recipe.index"))
        """
        Inhalte zu der Datenbank hinzufügen:

        recipe:
        userID
        Name
        amount (Personenmenge)

        recipeStep:
        recipeID
        step
        text
        duration

        recipeToCategory:
        recipeID
        recipeCategoryID

        ingredientsToRecipe:
        ingredientsID
        recipeID
        weight
        unitID
        """

    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM recipeCategory")
    recipeCategory = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM unit")
    units = cursor.fetchall()

    cursor.close()
    #print(recipeCategory)
    return render_template("recipe/create.html", enumerate=enumerate, recipeCategory=recipeCategory, units=units)

    """
    Daten auf der Webseite anzeigen:
    recipeCategory:
    recipeCategoryID
    Name
    superiorID -> geordnet

    unit:
    unitID
    name

    ingredients:
    ingredientsID
    Name
    """

    return """ """

@bp.route('/change/<id>')
#@login_required
def change(id):
    print(request.args)
    return """ """

@bp.route('/infinity')
def infinity():
    return render_template("recipe/infinity.html")

@bp.route('/load')
def load():
    page = request.args.get("page")
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM ingredients")
    result = cursor.fetchall()
    cursor.close()
    page = int(page) + 1 
    returnItem = ""
    rLen = len(result) - 1
    for counter, item in enumerate(result):
        if counter == rLen:
            returnItem += (f'<tr hx-get="/recipe/load?page={page}" hx-trigger="revealed" hx-swap="afterend"><td>{item[0]}</td><td>{item[1]}</td><td>{item[2]}</td></tr>')
        else:
            returnItem += (f"<tr><td>{item[0]}</td><td>{item[1]}</td><td>{item[2]}</td></tr>")
    return returnItem, 200

@bp.route('/search')
def search():
    inputUser = request.args.get("search")
    if inputUser == "":
        return ""
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM `ingredients` where `name` like '%{inputUser}%' LIMIT 3")
    result = cursor.fetchall()
    cursor.close()
    if result == None:
        return ""
    return render_template("recipe/form/ingredients.html", ingredients=result)