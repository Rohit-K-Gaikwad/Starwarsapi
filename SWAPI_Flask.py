import requests
import json

from flask import Flask, Response

from task_one import get_url
from utils.randgen import ProduceNumbers
from utils.fetch_data import hit_url
from task_two import first_film_data, characters_data, planets_data, species_data, starships_data, vehicles_data
from task_three import characters_data, films_data, planets_data, species_data, starships_data, vehicles_data

app = Flask(__name__)


@app.route("/welcome")
def welcome():
    return "Welcome to SWAPI Project"


@app.route("/taskone/<resource>/<int:count>/<int:start>/<int:end>")
def task_one(resource, count, start, end):

    obj = ProduceNumbers(
        start,
        end,
        count
    )

    resources = [element for element in obj]
    print(f"resources - {resources}")

    print(f"[ INFO ] produced {len(resources)}"
          f" random resource ids in range({start}, {end}).")

    data = []
    for resource_id in resources:
        print(f"[ INFO ] fetching data for resource_id {resource_id}...")
        url_ = get_url(resource_id, resource)

        # `requests.get()` returns a HttpResponse
        res = requests.get(url_)
        print(f"res.status_code = {res.status_code}")

        if res.status_code == 200:
            # getting dict value from response object
            result = res.json()

            # capturing name from dict object
            data.append(result.get("name"))

    output = {
        "count": len(data),
        "names": data
    }

    return Response(json.dumps(output), status=201, mimetype="application/json")


@app.route("/tasktwo")
def task_two_welcome():
    first_result = first_film_data()
    print("First Film Data")
    return Response(json.dumps(first_result), status=201, mimetype="application/json")


@app.route("/tasktwo/<resource>")
def task_two(resource):
    first_result = first_film_data()

    if resource == "characters":
        char_result = characters_data(first_result, "characters")
        return f"Characters in first film are : {char_result}"

    if resource == "planets":
        planet_result = planets_data(first_result, "planets")
        return f"Planets in first film are : {planet_result}"

    if resource == "vehicles":
        vehicle_result = vehicles_data(first_result, "vehicles")
        return f"Vehicles in first film are : {vehicle_result}"

    if resource == "species":
        species_result = species_data(first_result, "species")
        return f"Species in first film are : {species_result}"

    if resource == "starships":
        starships_result = starships_data(first_result, "starships")
        return f"Starships in first film are : {starships_result}"


@app.route("/taskthree/<resource>")
def task_three(resource, limit=3, start=1, end=8):
    char_data = []
    film_data = []
    planet_data = []
    specie_data = []
    starship_data = []
    vehicle_data = []

    obj = ProduceNumbers(start, end, limit-1)

    random_resources_numbers = [element for element in obj]

    for number in random_resources_numbers:
        if resource == 'films':
            data = hit_url(films_data()[number])
            data = data.json()
            film_data.append(data)

        if resource == 'planets':
            data = hit_url(planets_data()[number])
            data = data.json()
            planet_data.append(data)

        if resource == 'species':
            data = hit_url(species_data()[number])
            data = data.json()
            specie_data.append(data)

        if resource == 'starships':
            data = hit_url(starships_data()[number])
            data = data.json()
            starship_data.append(data)

        if resource == 'vehicles':
            data = hit_url(vehicles_data()[number])
            data = data.json()
            vehicle_data.append(data)

        else:
            data = hit_url(characters_data()[number])
            data = data.json()
            char_data.append(data)

    if resource == "characters":
        return char_data
    if resource == "films":
        return film_data
    if resource == "planets":
        return planet_data
    if resource == "species":
        return specie_data
    if resource == "starships":
        return starship_data
    if resource == "vehicles":
        return vehicle_data
