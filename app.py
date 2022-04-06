#.virtualenv\Scripts\activate/deactivate
from flask import Flask
from controllers.publications_controller import publications_route_handler

from controllers.users_controller import user_route_handler, users_route_handler

print(__name__)

app = Flask(__name__)

app.add_url_rule('/api/users', view_func=users_route_handler, methods=['GET', 'POST'])
app.add_url_rule('/api/users/_id', view_func=user_route_handler, methods=['GET','DELETE','PATCH'])

app.add_url_rule('/api/publications', view_func=publications_route_handler, methods=['GET', 'POST'])

if __name__ == '__main__':
    # kun debug-muuttujan arvo on True, serveri on ns. debug-tilassa
    # tämä tarkoittaa sitä
    # että se käynnistyy autom. uudelleen, kun koodi muuttuu
    app.run(debug=True)