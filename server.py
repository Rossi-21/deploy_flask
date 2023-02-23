from flask_app import app
from flask_app.controllers import user_controller, recipe_controller #import other controllers with a ,

if __name__=="__main__":       
    app.run(debug=True)    

