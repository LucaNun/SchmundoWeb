from flask import request, session, redirect, url_for, render_template, flash
from markupsafe import escape
import re

from app.recipe import bp
from app.extensions import mysql
from app.auth.routes import login_required

@bp.route('/')
def index():
    return """
    <h2>Recipe</h2>
    <a href="/">Main</a><br>
    <a href="/recipe/show">Show Recipes</a><br>
    <a href="/recipe/create">Create new</a><br>
    <a href="/recipe/change/">Change</a><br>
    <a href="/recipe/infinity">Infinity</a><br>
    <a href="/recipe/load">Load</a><br>
    """

@bp.route('/create', methods=["GET", "POST"])
@login_required
def create():
    if request.method == "POST":
        reIng = r"^ing-(?P<number>\d+)"
        reIngUnit = r"^ing-unit-(?P<number>\d+)"
        reStep = r"^step-(?P<number>\d+)"
        reStepDuration = r"^step-duration-(?P<number>\d+)"

        ingredients = {}
        steps = {}
        # Find all ingredients and steps via regex
        for item in request.form:           
            if re.match(reIng, item):
                number = re.match(reIng, item).group("number")
                if not ingredients.get(number):
                    ingredients[number] = {}
                ingredients[number]["weight"] = request.form[item]
            elif re.match(reIngUnit, item):
                number = re.match(reIngUnit, item).group("number")
                if not ingredients.get(number):
                    ingredients[number] = {}
                ingredients[number]["unit"] = request.form[item]

            elif re.match(reStep, item):
                number = re.match(reStep, item).group("number")
                if not steps.get(number):
                    steps[number] = {}
                steps[number]["text"] = request.form[item]
            elif re.match(reStepDuration, item):
                number = re.match(reStepDuration, item).group("number")
                if not steps.get(number):
                    steps[number] = {}
                steps[number]["duration"] = request.form[item]    

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO recipe (`userID`,`Name`,`amount`) VALUES (%s,%s,%s)", 
                       (session["userID"],request.form.get("name"),request.form.get("amount")))
        mysql.connection.commit()
        recipeID = cursor.lastrowid

        cursor.execute("INSERT INTO recipeToCategory (`recipeID`,`recipeCategoryID`) VALUES (%s,%s)", 
                       (recipeID,request.form.get("cat")))

        for item in ingredients:
            cursor.execute("INSERT INTO ingredientsToRecipe (`recipeID`,`ingredientsID`,`weight`,`unitID`) VALUES (%s,%s,%s,%s)", 
                       (recipeID,item,ingredients[item]["weight"],ingredients[item]["unit"]))

        for step in steps:
            cursor.execute("INSERT INTO recipeStep (`recipeID`,`step`,`text`,`duration`) VALUES (%s,%s,%s,%s)", 
                       (recipeID,step,steps[step]["text"],steps[step]["duration"]))
        mysql.connection.commit()
        cursor.close()
        flash("Rezept wurde erfolgreich angelegt!", "info")
        return redirect(url_for("recipe.create"))

    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM recipeCategory")
    recipeCategory = cursor.fetchall()

    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM unit")
    units = cursor.fetchall()

    cursor.close()
    return render_template("recipe/create.html", enumerate=enumerate, recipeCategory=recipeCategory, units=units)

@bp.route('/change/<id>')
#@login_required
def change(id):
    print(request.args)
    return """ """

@bp.route('/infinity')
def infinity():
    return render_template("recipe/infinity.html")

@bp.route('/show')
def show():
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT recipe.recipeID, user.username, recipe.name, recipe.amount FROM `recipe` INNER JOIN `user` ON recipe.userID=user.userID")

    result = cursor.fetchall()
    cursor.close()
    return render_template("recipe/show.html", recipes=result)

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