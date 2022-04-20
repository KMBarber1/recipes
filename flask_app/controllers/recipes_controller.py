from flask import redirect, render_template, request, session
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User



@app.route("/dashboard")
def all_recipes():
    if "user_id" not in session:
        return redirect("/logout")
    data ={
        "id": session["user_id"]
    }
    return render_template("all_recipes.html", user = User.get_by_id(data), recipes = Recipe.get_all())

@app.route("/new/recipe")
def new_recipe():
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id":session["user_id"]
    }
    return render_template("new_recipe.html", user = User.get_by_id(data))


@app.route("/edit/recipe/<int:id>")
def edit_recipe(id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id":id
    }
    user_data = {
        "id":session["user_id"]
    }
    return render_template("edit_recipe.html", edit = Recipe.get_one(data), user = User.get_by_id(user_data))


@app.route("/recipe/<int:id>")
def one_recipe(id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id":id
    }
    user_data = {
        "id":session["user_id"]
    }
    return render_template("one_recipe.html", recipe = Recipe.get_one(data), user = User.get_by_id(user_data))





@app.route("/create/recipe", methods=["POST"])
def create_recipe():
    if "user_id" not in session:
        return redirect("/logout")
    if not Recipe.validate_recipe(request.form):
        return redirect("/new/recipe")
    data = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "prep_time": int(request.form["prep_time"]),
        "date_made": request.form["date_made"],
        "user_id": session["user_id"]
    }
    Recipe.save(data)
    return redirect("/dashboard")


@app.route("/update/recipe", methods=["POST"])
def update_recipe():
    if "user_id" not in session:
        return redirect("/logout")
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/edit/recipe/{request.form['id']}")

    Recipe.update(request.form)
    return redirect("/dashboard")


@app.route("/delete/recipe/<int:id>")
def delete_recipe(id):
    if "user_id" not in session:
        return redirect("/logout")
    data = {
        "id":id
    }
    Recipe.delete(data)
    return redirect("/dashboard")