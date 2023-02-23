from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

db = 'recipes_schema'

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.under = data['under']
        self.instructions = data['instructions']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def save(cls, data):
        query = """
        INSERT INTO recipes (name, description, under, instructions, created_at, user_id) 
        VALUES (%(name)s, %(description)s, %(under)s, %(instructions)s, %(created_at)s, %(user_id)s);
        """
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(db).query_db(query)
        users = []
        for user in results:
            users.append( cls(user) )
        return users 
        
    @classmethod
    def get_one(cls,data):
        query = "Select * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(db).query_db(query,data)
        return cls(result[0])

    @classmethod
    def update(cls,data):
        query = """ 
        UPDATE recipes 
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, created_at = %(created_at)s, under = %(under)s
        WHERE id = %(id)s;"""
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = "DELETE from recipes WHERE id = %(id)s;"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def get_recipes_with_users(cls):
        query = """
                SELECT * FROM recipes
                JOIN users on recipes.user_id = users.id;
                """
        results = connectToMySQL(db).query_db(query)
        recipes = []
        for row in results:
            this_recipe = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_recipe.creator = user.User(user_data)
            recipes.append(this_recipe)
        print(user_data)    
        return recipes

    @classmethod
    def get_by_id(cls,data):
        query = """
                SELECT * FROM recipes
                JOIN users on recipes.user_id = users.id
                WHERE recipes.id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query,data)
        if not result:
            return False
        result = result[0]
        this_recipe = cls(result)
        user_data = {
                "id": result['users.id'],
                "first_name": result['first_name'],
                "last_name": result['last_name'],
                "email": result['email'],
                "password": "",
                "created_at": result['users.created_at'],
                "updated_at": result['users.updated_at']
        }
        this_recipe.creator = user.User(user_data)
        return this_recipe

    @staticmethod
    def validate_recipe(request):
        is_valid = True
        if len(request['name']) < 1:
            is_valid = False
            flash('Name Required', 'recpError')
        elif len(request['name']) < 4:
            is_valid = False
            flash('Name must be at least 3 characters', 'recpError')
        if len(request['description']) < 1:
            is_valid = False
            flash('Description Required', 'recpError')
        elif len(request['description']) < 4:
            is_valid = False
            flash('Description must be at least 3 characters', 'recpError')
        if len(request['instructions']) < 1:
            is_valid = False
            flash('Instructions Required', 'recpError')
        elif len(request['instructions']) < 4:
            is_valid = False
            flash('Instructions must be at least 3 characters', 'recpError')
        if not request.get('under', ''):
            is_valid = False
            flash('Under 30 min is Required', 'recpError')
        if not request.get('created_at', ''):
            is_valid = False
            flash('Date Cooked/Made is Required', 'recpError')
        return is_valid