#.virtualenv\Scripts\activate/deactivate
from flask import Flask, render_template
# Jokaisella python-skripitllä on nimi ja sen on __name__-muuttujassa
#namen arvo riippuu siitä miten skripti suoritetaan
# jos skripti ajetaan ns. standalonene (python skriptin_nimi.py) silloin skriptin nimi on __main__
# jos skripti suoritetaan esim. importaamalla se toiseen tiedostoon
# importatun skriptin nimi on tiedoston nimi

print(__name__)

app = Flask(__name__)

# flaskin route-dekoraattori 'sitoo' urlin route_handleriin
@app.route('/users')
# tämä funktio on ns. route_handler, eli se funktio, joka suoritetaan,
# kun routeen tulee selaimelta pyyntö
def hello_world_route_handler():
    return render_template('index.html')

@app.route('/say_my_name/<name>/<age>')
def say_my_name_route_handler(name, age):
    return f"Hello my name is {name} I'm {age} years old"

if __name__ == '__main__':
    # kun debug-muuttujan arvo on True, serveri on ns. debug-tilassa
    # tämä tarkoittaa sitä
    # että se käynnistyy autom. uudelleen, kun koodi muuttuu
    app.run(debug=True)