#!/usr/bin/python3
"""
Start a Flask web application
"""
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from flask import Flask, render_template
import uuid
from models import storage
from os import environ

app = Flask(__name__)

@app.teardown_appcontext
def close_db(exception):
    """Close the current SQLAlchemy session"""
    storage.close()

@app.route('/2-hbnb', strict_slashes=False)
def hbnb():
    """Render the main HBNB page"""
    states = storage.all(State).values()
    states = sorted(states, key=lambda state: state.name)
    st_ct = []

    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda city: city.name)])

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda amenity: amenity.name)

    places = storage.all(Place).values()
    places = sorted(places, key=lambda place: place.name)

    return render_template('2-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places, cache_id=uuid.uuid4())

if __name__ == "__main__":
    """Run the Flask application"""
    app.run(host='0.0.0.0', port=5000)
