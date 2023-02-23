from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, recipe

@app.route('/recipes')
def recipes():
    if 'user_id' in session:
        one_user = user.User.get_one({"id":session['user_id']})        
        return render_template("recipes.html",one_user = one_user, recipes = recipe.Recipe.get_recipes_with_users())
    return redirect('/')

@app.route('/recipes/<int:id>')
def view(id):
    if 'user_id' in session:
        data = {
            "id" : id
        }
        one_user = user.User.get_one({"id":session['user_id']})
        return render_template("view.html", recipe = recipe.Recipe.get_by_id(data), one_user = one_user)
    return redirect('/')   

@app.route('/recipes/delete_recipe/<int:id>/')
def delete_recipe(id):
    data = {
        "id" : id
    }
    recipe.Recipe.delete(data)
    return redirect(request.referrer)

@app.route('/recipes/edit/<int:id>')
def edit(id):
    if 'user_id' in session:
        data = {
            "id" : id
        }
        one_user = user.User.get_one({"id":session['user_id']})
        return render_template("edit.html", recipe = recipe.Recipe.get_by_id(data), one_user = one_user)
    return redirect('/') 

@app.route('/update', methods=["POST"] )
def update():
    if 'user_id' in session:
        if recipe.Recipe.validate_recipe(request.form):
            recipe.Recipe.update(request.form)
            return redirect('/recipes')
        return redirect(request.referrer)
    return redirect('/')

@app.route('/recipes/new')
def new():
    if 'user_id' in session:
        return render_template("new.html")
    return redirect('/')

@app.route('/create', methods = ["POST"])
def create():
    if 'user_id' in session:
        if recipe.Recipe.validate_recipe(request.form):
            data = {
                "name" : request.form["name"],
                "description" : request.form["description"],
                "under" : request.form.get("under"),
                "instructions" : request.form["instructions"],
                "created_at" : request.form["created_at"],
                "user_id" : request.form["user_id"]
            }
            recipe.Recipe.save(data)
            return redirect('/recipes/new')
        return redirect('/recipes/new')
    return redirect('/')