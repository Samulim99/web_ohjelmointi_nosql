#.virtualenv\Scripts\activate/deactivate
#git add . #Lisää muutokset committia varten
#git commit -m "viesti" # commitoi muutokset paikalliseen repoon
#git push # lisää muutokset remoteen (eli githubiin)


from flask import Flask, jsonify
from controllers.auth_controller import login_route_handler, register_route_handler
from controllers.publications_controller import publications_route_handler
from flask_jwt_extended import JWTManager
from controllers.users_controller import user_route_handler, users_route_handler
from errors.not_found import NotFound
from errors.validation_error import ValidationError

print(__name__)

app = Flask(__name__)
app.config.from_object('config.Config')
jwt = JWTManager(app)

@app.errorhandler(NotFound)
def not_found_error_handler(err):
    return jsonify(err=err.args), 404

@app.errorhandler(ValidationError)
def validation_error_handler(err):
    return jsonify(err=err.args), 400

@app.errorhandler(Exception)
def generic_exception_handler(err):
    return jsonify(err=str(err))

app.add_url_rule('/api/users', view_func=users_route_handler, methods=['GET', 'POST'])
app.add_url_rule('/api/users/_id', view_func=user_route_handler, methods=['GET','DELETE','PATCH'])
app.add_url_rule('/api/register', view_func=register_route_handler, methods=['POST'])
app.add_url_rule('/api/login', view_func=login_route_handler, methods=['POST'])

app.add_url_rule('/api/publications', view_func=publications_route_handler, methods=['GET', 'POST'])

if __name__ == '__main__':
    # kun debug-muuttujan arvo on True, serveri on ns. debug-tilassa
    # tämä tarkoittaa sitä
    # että se käynnistyy autom. uudelleen, kun koodi muuttuu
    app.run(debug=True)