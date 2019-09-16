from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.

    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)


@app.route("/contacts", methods=['POST'])
def create_contact():
    data = request.json()
    if(data["name"] and data["nickname"] and data["hobby"]):
        db.create('contacts',data)
    else:
        return create_response(status = 422, message = "Please enter the correct properties" )

@app.route("/contacts", methods=['GET'])
def get_all_contacts():
    hobby = request.args.get("hobby")
    if hobby and db.getByHobby(hobby) != None:
        return create_response(status = 201, result = {"contacts": db.getByHobby(hobby)})
    elif db.getByHobby(hobby) == None:
        return create_response(status = 404, message = "No contact with this hobby exists")
    return create_response(result = {"contacts": db.get('contacts')})

@app.route("/contacs/<id>", methods=['GET','PUT'])
def get_contact_from_id(id):
    if db.getById('contacts',int(id)) is None:
        return create_response(status = 404, message = "No contact with this id exists")
    elif request.method == 'GET':
        return create_response(result = {"contact":db.getById(contacts, int(id))})
    elif request.method == 'PUT':
        data = request.json()
        cont = db.getById(contacs,int(id))
        cont["name"] = data["name"]
        cont["hobby"] = data["hobby"]
        return create_response(status = 201,result = {"contact":cont})


@app.route("/shows/<id>", methods=['DELETE'])
def delete_show(id):
    if db.getById('contacts', int(id)) is None:
        return create_response(status=404, message="No contact with this id exists")
    db.deleteById('contacts', int(id))
    return create_response(message="Contact deleted")


# TODO: Implement the rest of the API here!

"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(port=8080, debug=True)
