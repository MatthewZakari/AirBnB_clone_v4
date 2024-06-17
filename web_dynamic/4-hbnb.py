#!/usr/bin/python3
"""
Initialize and run the Flask web application.
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
def close_db(error):
    """Close the current SQLAlchemy session."""
    storage.close()

@app.route('/4-hbnb', strict_slashes=False)
def hbnb():
    """Render the main HBNB page."""
    states = storage.all(State).values()
    states = sorted(states, key=lambda k: k.name)
    st_ct = []

    for state in states:
        st_ct.append([state, sorted(state.cities, key=lambda k: k.name)])

    amenities = storage.all(Amenity).values()
    amenities = sorted(amenities, key=lambda k: k.name)

    places = storage.all(Place).values()
    places = sorted(places, key=lambda k: k.name)

    return render_template('4-hbnb.html',
                           states=st_ct,
                           amenities=amenities,
                           places=places, cache_id=uuid.uuid4())

if __name__ == "__main__":
    """Run the Flask application."""
    app.run(host='0.0.0.0', port=5000)
