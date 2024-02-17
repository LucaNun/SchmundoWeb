from flask import request, session, redirect, url_for, render_template, flash, jsonify
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

@bp.route('/change/<id>', methods=["GET", "POST"])
@login_required
def change(id):
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT userID FROM `recipe` WHERE userID = '{session.get("userID")}'")
    result = cursor.fetchone()
    if result == None:
        flash("Das Rezept ist nicht von dir!", "error")
        return redirect(url_for("recipe.showID", id=id))
    
    if request.method == "POST":
        data = request.get_json()
        sqlValues = ""
        for item in data.get("valueliste"):
            if len(sqlValues) != 0:
                sqlValues+= ","
            sqlValues += f"`{item}`=`{data["valueliste"][item]}`"
        sql = f"UPDATE `recipe` SET {sqlValues} WHERE `recipeID`={id}"
        #SQL
        sqlValues = ""
        sqlNew = {}
        sqlDelete = []
        for item in data.get("ingredientlist"):
            if not data.get("ingredientlist")[item]:
                sqlDelete.append(item)
                continue
            if item not in session.get("ch_ingredients")[0]: #FIX needed
                sqlNew[item] = data.get("ingredientlist")[item]
                continue
            if len(sqlValues) != 0:
                sqlValues+= ","
            sqlValues += f"`{item}`=`{data["ingredientlist"][item]}`"
        print(sqlDelete)
        print(sqlNew)
        print(sqlValues)
        print(session.get("ch_ingredients"))
        sql = f"UPDATE `recipe` SET {sqlValues} WHERE `recipeID`={id}"

    
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT recipe.recipeID, user.username, recipe.name, recipe.amount, recipe.userID FROM `recipe` INNER JOIN `user` ON recipe.userID=user.userID WHERE recipe.recipeID = '{id}'")
    recipe = cursor.fetchone()

    cursor.execute(f"SELECT recipeCategory.name FROM recipeToCategory INNER JOIN recipeCategory ON recipeToCategory.recipeCategoryID=recipeCategory.recipeCategoryID WHERE recipeToCategory.recipeID = '{id}'")
    recipeCategory = cursor.fetchone()

    cursor.execute(f"SELECT ingredients.name, weight, unit.name FROM ingredientsToRecipe INNER JOIN ingredients ON ingredientsToRecipe.ingredientsID=ingredients.ingredientsID INNER JOIN unit ON ingredientsToRecipe.unitID=unit.unitID WHERE ingredientsToRecipe.recipeID = '{id}'")
    ingredients = cursor.fetchall()

    cursor.execute(f"SELECT step, text, duration FROM recipeStep WHERE recipeID = '{id}'")
    steps = cursor.fetchall()
    cursor.close()
    session["ch_recipe"] = recipe
    session["ch_ingredients"] = ingredients
    session["ch_steps"] = steps
    return render_template("recipe/change.html", recipe=recipe, recipeCategory=recipeCategory, ingredients=ingredients, steps=steps, userID=session.get("userID"))

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

@bp.route('/show/<id>')
def showID(id):
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT recipe.recipeID, user.username, recipe.name, recipe.amount, recipe.userID FROM `recipe` INNER JOIN `user` ON recipe.userID=user.userID WHERE recipe.recipeID = '{id}'")
    recipe = cursor.fetchone()

    cursor.execute(f"SELECT recipeCategory.name FROM recipeToCategory INNER JOIN recipeCategory ON recipeToCategory.recipeCategoryID=recipeCategory.recipeCategoryID WHERE recipeToCategory.recipeID = '{id}'")
    recipeCategory = cursor.fetchone()

    cursor.execute(f"SELECT ingredients.name, weight, unit.name FROM ingredientsToRecipe INNER JOIN ingredients ON ingredientsToRecipe.ingredientsID=ingredients.ingredientsID INNER JOIN unit ON ingredientsToRecipe.unitID=unit.unitID WHERE ingredientsToRecipe.recipeID = '{id}'")
    ingredients = cursor.fetchall()

    cursor.execute(f"SELECT step, text, duration FROM recipeStep WHERE recipeID = '{id}'")
    steps = cursor.fetchall()
    cursor.close()
    return render_template("recipe/showID.html", recipe=recipe, recipeCategory=recipeCategory, ingredients=ingredients, steps=steps, userID=session.get("userID"))

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

@bp.route('/ajax', methods=["GET", "POST"])
def ajax():
    print(request.get_json())
    data = request.get_json()
    id = 0
    value = ""
    for item in data.get("valueliste"):
        if len(value) != 0:
            value+= ","
        value += f"`{item}`=`{data["valueliste"][item]}`"
        print(item)
    sql = f"UPDATE `recipe` SET {value} WHERE `recipeID`={id}"
    print(sql)
    return jsonify({'status': 'success'}), 200