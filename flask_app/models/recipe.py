from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import user
from flask import flash


class Recipe:

    def __init__( self , data ):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.date_made = data["date_made"]
        self.prep_time = data["prep_time"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user = user.User.get_by_id({"id": data["user_id"]})



# Create
    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes (name, description, instructions, prep_time, date_made, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(prep_time)s, %(date_made)s, %(user_id)s);"
        return connectToMySQL("recipe_schema").query_db(query,data)


# READ
    # read many
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL("recipe_schema").query_db(query)
        recipes = []
        for row in results:
            print(row["date_made"])
            recipes.append( cls(row))
        return recipes


# read one
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL("recipe_schema").query_db(query, data) 
        return cls(results[0])


# UPDATE
    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, prep_time=%(prep_time)s, date_made=%(date_made)s, updated_at = Now() WHERE id = %(id)s;"
        return connectToMySQL("recipe_schema").query_db(query,data)


# DELETE
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL("recipe_schema").query_db(query,data)


# VALIDATE
    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash("Name must be at least 3 characters.", "recipe")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Description must be at least 3 characters.", "recipe")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Instructions must be at least 3 characters.", "recipe")
            is_valid = False
        if recipe['date_made'] == "":
            flash("Enter a date.", "recipe")
            is_valid = False
        if "prep_time" not in recipe or recipe["prep_time"] not in "01":
            flash("Fillout the Under 30 Minutes question?", "recipe")
            is_valid = False
        return is_valid