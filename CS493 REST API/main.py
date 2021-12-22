# boostrap cdn taken from: https://cdn.jsdelivr.net/npm/bootswatch@4.5.2/dist/cosmo/bootstrap.min.css
# code implentation taken from: https://developers.google.com/identity/protocols/oauth2/web-server
# JWT ID token implentation is taken from: https://developers.google.com/identity/sign-in/web/backend-auth
# skeleton code taken from HTTP/REST Implentation 

from google.cloud import datastore
from google.oauth2 import id_token
from google.auth.transport import requests as jwt_request 
import flask
from flask import Flask, request, render_template, jsonify
import json
import requests
import uuid
import random
import constants

app = flask.Flask(__name__)
app.secret_key = str(uuid.uuid4())
app.debug = True
client = datastore.Client()


CLIENT_ID = '696241842742-e4i9cci40mike4amndru379ghoqdertv.apps.googleusercontent.com'
CLIENT_SECRET = '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'
SCOPE = 'https://www.googleapis.com/auth/userinfo.profile'
REDIRECT_URI = 'https://cs493portfolioproject-farolr.wl.r.appspot.com/oauth'
# REDIRECT_URI = 'http://localhost:8080/oauth'
STATE = "State" + str(random.randint(1, 9999999)) # randomize state 

# get sub from JWT
def get_sub():
    if 'Authorization' in request.headers:
        user_jwt = request.headers['Authorization'] # request Authorization header 
        user_jwt = user_jwt.replace('Bearer ', '') # delete the "Bearer" string and space in front of the token
        try:
              idinfo = id_token.verify_oauth2_token(user_jwt, jwt_request.Request(), CLIENT_ID)
              sub = idinfo['sub']
              return sub
        except:
            return "Invalid Token"
    else:
        return (jsonify("Missing/invalid JWT"), 401)

@app.route('/')
def index():
    return render_template('welcome.html')

# get all unprotected users
@app.route('/users', methods=['GET'])
def users_get():
    if request.method == 'GET':
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify("Accept header must be in application/json"), 406)
        query = client.query(kind=constants.users)
        results = list(query.fetch())
        return (json.dumps(results), 200)
    else:
        return (jsonify("Method not allowed"), 405)

# Boats collection with Post and Get Functionalities 
@app.route('/boats', methods=['POST','GET'])
def boats_get_post():
    # post request 
    if request.method == 'POST':
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify("Accept header must be in application/json"), 406)
        content = request.get_json()
        new_boat = datastore.entity.Entity(key=client.key(constants.boats))
        new_boat.update({"name": content["name"], "type": content["type"], "length": content["length"], "loads": []})
        owner = get_sub()
        if owner != "Invalid Token":
            new_boat.update({"owner": owner})
            client.put(new_boat)
            boat = client.get(key=new_boat.key)
            boat['id'] = new_boat.key.id
            boat['self'] = request.url + "/" + str(new_boat.key.id) # add self URL
            return (boat, 201) # boat is returned as a JSON object. 201 request code 
        else:
            return (jsonify('Missing/invald JWT'), 401) # 401 code if Missing/valid JWT
        
    # get request for all boats 
    elif request.method == 'GET':
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify("Accept header must be in application/json"), 406)
        query = client.query(kind=constants.boats)
        counter = len(list(query.fetch())) # counts how many entities there are 
        q_limit = int(request.args.get('limit', '5'))
        q_offset = int(request.args.get('offset', '0'))
        l_iterator = query.fetch(limit= q_limit, offset=q_offset)
        pages = l_iterator.pages
        results = list(next(pages))
        if l_iterator.next_page_token:
            next_offset = q_offset + q_limit
            next_url = request.base_url + "?limit=" + str(q_limit) + "&offset=" + str(next_offset)
        else:
            next_url = None
        for e in results:
            e["id"] = e.key.id
            e["self"] = request.url + "/" + str(e.key.id)
        get_boats = []
        owner = get_sub()
        # checks if JWT token has been entered
        if owner != "Invalid Token":
            for e in results:
                if e["owner"] == owner:
                       get_boats.append(e)
        output = {"boat": get_boats}
        output["total entities"] = counter # add total entities at the bottom per page 
        if next_url:
            output["next"] = next_url
        return (output, 200)
    else:
        return (jsonify("Method not allowed"), 405)

@app.route('/boats/<id>', methods=['DELETE', 'GET', 'PUT', 'PATCH'])
def boats_delete_get_put_patch(id):
    # delete request to delete a specific boat 
    if request.method == 'DELETE':
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify("Accept header must be in application/json"), 406)
        owner = get_sub()
        boat_key = client.key(constants.boats, int(id))
        boat = client.get(key=boat_key)
        if boat is None:
            return (jsonify("This boat ID does not exist. Please try again."), 404) # wrong ID is entered 
        else:
            owner = get_sub()
            if owner == "Invalid Token":
                return (jsonify('Missing/invald JWT'), 401) # JWT is invalid or missing 
            # check if owner id matches 
            if boat["owner"] != owner:
                return (jsonify("This boat belongs to someone else, please only delete boats that you own"), 403) # doesn't delete due to different ID
            if "loads" in boat.keys():
                if len(boat["loads"]) != 0:
                    for i in boat["loads"]:
                        load_key = client.key(constants.loads, int(i['id']))
                        load = client.get(key=load_key)
                        load['boat'] = []
                        client.put(load)
            client.delete(boat_key)
            return (jsonify("Boat was deleted"), 204) # Boat was successfully deleted. 204 request. 
    
    # Get function. You don't need to be an authenticated user to GET certain boats 
    elif request.method == 'GET':
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify("Accept header must be in application/json"), 406)
        boat_key = client.key(constants.boats, int(id))
        boat = client.get(key=boat_key)
        if boat is None:
            return (jsonify("Boat does not exist"), 404)
        boat['id'] = id
        boat['self'] = request.url # add self URL
        return (boat, 200) # boat is returned as a JSON object. 200 request code
    
    # Put function. Allows JWT authenticated user to update ALL properities. 
    elif request.method == 'PUT':
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify("Accept header must be in application/json"), 406)
        content = request.get_json()
        boat_key = client.key(constants.boats, int(id))
        boat = client.get(key=boat_key)
        if boat is None:
            return (jsonify("Boat does not exist"), 404)
        else:
            owner = get_sub()
            if owner == "Invalid Token":
                return (jsonify('Missing/invald JWT'), 401) # JWT is invalid or missing 
            # check if owner id matches 
            if boat["owner"] != owner:
                return (jsonify("This boat belongs to someone else, please only update boats that you own"), 403) # doesn't delete due to different ID
            boat.update({"name": content["name"], "type": content["type"], "length": content["length"]})
            client.put(boat)
            boat['id'] = id
            boat['self'] = request.url # add self URL
            return (boat, 200) # boat is returned as a JSON object. 200 request code

    # Patch function. Allows JWT Authenticated user to update certain properties 
    elif request.method == 'PATCH':
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify("Accept header must be in application/json"), 406)
        content = request.get_json()
        boat_key = client.key(constants.boats, int(id))
        boat = client.get(key=boat_key)
        if boat is None:
            return (jsonify("Boat does not exist"), 404)
        else:
            owner = get_sub()
            if owner == "Invalid Token":
                return (jsonify('Missing/invald JWT'), 401) # JWT is invalid or missing 
            # check if owner id matches 
            if boat["owner"] != owner:
                return (jsonify("This boat belongs to someone else, please only update boats that you own"), 403) # doesn't delete due to different ID
            for key in content.keys():
                if key == "name":
                    boat.update({"name": content["name"]})
                if key == "type":
                    boat.update({"type": content["type"]})
                if key == "length":
                    boat.update({"length": content["length"]})
            client.put(boat)
            boat['id'] = id
            boat['self'] = request.url # add self URL
            return (boat, 200) # boat is returned as a JSON object. 200 request code
    else:
        return (jsonify("Method not allowed"), 405)
    
# Loads collection with Post and Get Functionalities 
@app.route('/loads', methods=['POST','GET'])
def loads_get_post():
    # post request to make a load 
    if request.method == 'POST':
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify("Accept header must be in application/json"), 406)
        content = request.get_json()
        new_load = datastore.entity.Entity(key=client.key(constants.loads))
        new_load.update({"name": content["name"], "type": content["type"], "quantity": content["quantity"], "boat": []})
        client.put(new_load)
        load = client.get(key=new_load.key)
        load['id'] = new_load.key.id
        load['self'] = request.url + "/" + str(new_load.key.id) # add self URL
        return (load, 201) # boat is returned as a JSON object. 201 request code 
        
    # get request for all loads
    elif request.method == 'GET':
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify("Accept header must be in application/json"), 406)
        query = client.query(kind=constants.loads)
        counter = len(list(query.fetch())) # counts how many entities there are 
        q_limit = int(request.args.get('limit', '5'))
        q_offset = int(request.args.get('offset', '0'))
        l_iterator = query.fetch(limit= q_limit, offset=q_offset)
        pages = l_iterator.pages
        results = list(next(pages))
        if l_iterator.next_page_token:
            next_offset = q_offset + q_limit
            next_url = request.base_url + "?limit=" + str(q_limit) + "&offset=" + str(next_offset)
        else:
            next_url = None
        for e in results:
            e["id"] = e.key.id
            e["self"] = request.url + "/" + str(e.key.id)
        output = {"loads": results}
        output["total entities"] = counter # add total entities at the bottom per page 
        if next_url:
            output["next"] = next_url
        return (output, 200) # return loads. 200 success 
    else:
        return (jsonify("Method not allowed"), 405)

# Delete, Get, Put, and Patch functionalities for Loads
@app.route('/loads/<id>', methods=['DELETE', 'GET', 'PUT', 'PATCH'])
def loads_delete_get_put_patch(id):
    # delete request to delete a specific load  
    if request.method == 'DELETE':
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify("Accept header must be in application/json"), 406)
        load_key = client.key(constants.loads, int(id))
        load = client.get(key=load_key)
        if load is None:
            return (jsonify("This load ID does not exist. Please try again."), 404) # wrong ID is entered 
        if "boat" in load.keys():
            if len(load["boat"]) != 0:
                boat_id = load["boat"]["id"]
                boat_key = client.key(constants.boats, int(boat_id))
                boat = client.get(key=boat_key)
                print(request.url + "/" + str(load.key.id))
                if "loads" in boat.keys():
                    boat["loads"].remove({"id": load.key.id, "self": request.url})
                    client.put(boat) 
        client.delete(load_key)
        return (jsonify("load was deleted"), 204) # Load was successfully deleted. 204 request. 
    
    # Get function. You don't need to be an authenticated user to GET certain loads
    elif request.method == 'GET':
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify("Accept header must be in application/json"), 406)
        load_key = client.key(constants.loads, int(id))
        load = client.get(key=load_key)
        if load is None:
            return (jsonify("load does not exist"), 404)
        load['id'] = id
        load['self'] = request.url # add self URL
        return (load, 200) # load is returned as a JSON object. 200 request code
    
    # Put function. No JWT authentication is required to update/PUT load
    elif request.method == 'PUT':
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify("Accept header must be in application/json"), 406)
        content = request.get_json()
        load_key = client.key(constants.loads, int(id))
        load = client.get(key=load_key)
        if load is None:
            return (jsonify("Load does not exist"), 404)
        load.update({"name": content["name"], "type": content["type"], "quantity": content["quantity"]})
        client.put(load)
        load['id'] = id
        load['self'] = request.url # add self URL
        return (load, 200) # load is returned as a JSON object. 200 request code

    # Patch function. Allows JWT Authenticated user to update certain properties 
    elif request.method == 'PATCH':
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify("Accept header must be in application/json"), 406)
        content = request.get_json()
        load_key = client.key(constants.loads, int(id))
        load = client.get(key=load_key)
        if load is None:
            return (jsonify("Load does not exist"), 404) 
        for key in content.keys():
            if key == "name":
                load.update({"name": content["name"]})
            if key == "type":
                load.update({"type": content["type"]})
            if key == "quantity":
                load.update({"quantity": content["quantity"]})
        client.put(load)
        load['id'] = id
        load['self'] = request.url # add self URL
        return (load, 200) # load is returned as a JSON object. 200 request code
    else:
        return (jsonify("Method not allowed"), 405)

# Delete and Put functions for the relationship of boats and loads
# To establish the relationship, the endpoints are protected so only the onwer of the boats/authorized JWT may delete/put loads on their boats
# Relationship is one to many between boat and loads. Boats may have mulitple loads, but a load can only be present on one boat. 
@app.route('/boats/<boat_id>/loads/<load_id>', methods=['DELETE', 'PUT'])
def boats_loads_delete_put(boat_id, load_id):
     # delete request to delete a load from a specific boat 
    if request.method == 'DELETE':
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify("Accept header must be in application/json"), 406)
        owner = get_sub()
        boat_key = client.key(constants.boats, int(boat_id))
        boat = client.get(key=boat_key)
        if boat is None:
            return (jsonify("This boat ID does not exist. Please try again."), 404) # wrong ID is entered 
        load_key = client.key(constants.loads, int(load_id))
        load = client.get(key=load_key)
        if load is None:
            return (jsonify("This load ID does not exist. Please try again."), 404) # wrong ID is entered 
        else:
            owner = get_sub()
            if owner == "Invalid Token":
                return (jsonify('Missing/invald JWT'), 401) # JWT is invalid or missing 
            # check if owner id matches 
            if boat["owner"] != owner:
                return (jsonify("This boat belongs to someone else, please only delete loads that you own"), 403) # doesn't delete due to different ID
            if "boat" in load.keys():
                if len(load["boat"]) != 0:
                    if load["boat"]["id"] == boat.key.id:
                        boat["loads"].remove({"id": load.key.id, "self": request.url_root + "loads/" + str(load.key.id)})
                        client.put(boat) 
                        load['boat'] = []
                        client.put(load)
            return (jsonify("Load was deleted"), 204) # Load was successfully deleted. 204 request. 
    
    # Put function to put a specific load on a specific boat
    elif request.method == 'PUT':
        if 'application/json' not in request.accept_mimetypes:
            return (jsonify("Accept header must be in application/json"), 406)
        content = request.get_json()
        boat_key = client.key(constants.boats, int(boat_id))
        boat = client.get(key=boat_key)
        if boat is None:
            return (jsonify("Boat does not exist"), 404)
        load_key = client.key(constants.loads, int(load_id))
        load = client.get(key=load_key)
        if load is None:
            return (jsonify("This load ID does not exist. Please try again."), 404) # wrong ID is entered 
        else:
            owner = get_sub()
            if owner == "Invalid Token":
                return (jsonify('Missing/invald JWT'), 401) # JWT is invalid or missing 
            # check if owner id matches 
            if boat["owner"] != owner:
                return (jsonify("This boat belongs to someone else, please only update boats that you own"), 403) # doesn't delete due to different ID
            # check if there's a boat already assigned with this load. If there is, remove it 
            if "boat" in load.keys():
                if len(load["boat"]) != 0: # if boat is empty. load can be sucessfully deleted since it doesn't belong to a boat 
                    old_boat_id = load["boat"]["id"]
                    old_boat_key = client.key(constants.boats, int(old_boat_id))
                    old_boat = client.get(key=old_boat_key)
                    if "loads" in old_boat.keys():
                        old_boat["loads"].remove({"id": load.key.id, "self": request.url_root + "loads/" + str(load.key.id)})
                        client.put(old_boat) 
            boat["loads"].append({"id": load.key.id, "self": request.url_root + "loads/" + str(load.key.id)})
            client.put(boat)
            load["boat"] = {"id": boat.key.id, "self": request.url_root + "boats/" + str(boat.key.id)}
            client.put(load)
            return (boat, 200) # boat is returned as a JSON object. 200 request code
    else:
        return (jsonify("Method not allowed"), 405)


@app.route('/userinfo')
def userinfo():
    # store date into datastore
    new_state = datastore.Entity(client.key("states"))
    new_state.update({'state': STATE})
    client.put(new_state)
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth'))
    credentials = json.loads(flask.session['credentials'])
    if credentials['expires_in'] <= 0:
        return flask.redirect(flask.url_for('oauth'))
    else:
        credentials = json.loads(flask.session['credentials'])
        try:
            idinfo = id_token.verify_oauth2_token(credentials['id_token'], jwt_request.Request(), CLIENT_ID)
            sub = idinfo['sub']
            query = client.query(kind=constants.users)
            results = list(query.fetch())
            found_user = False
            for e in results:
                if e['user_id'] == sub:
                    found_user = True
                    return render_template('userinfo.html', jwt_var=credentials['id_token'], user_id=e['user_id'], last_name=e['last_name'], first_name=e['first_name'])
            if found_user == False:
                headers = {'Authorization': 'Bearer {}'.format(credentials['access_token']), 'State': '{}'.format(STATE)}
                request_uri = 'https://people.googleapis.com/v1/people/me?personFields=names'
                request = requests.get(request_uri, headers=headers)
                name = json.loads(request.text)
                name = name['names']
                last_name = name[0]['familyName']
                first_name = name[0]['givenName']
                new_user = datastore.entity.Entity(key=client.key(constants.users))
                new_user.update({"user_id": sub, "first_name": first_name, "last_name": last_name})
                client.put(new_user) 
            return render_template('userinfo.html', jwt_var=credentials['id_token'], user_id=sub, last_name=last_name, first_name=first_name)
        except:
            return ("Missing/invalid JWT", 401) 

@app.route('/oauth')
def oauth():
    if 'code' not in flask.request.args:
        authorization_uri = ('https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={}&redirect_uri={}&scope={}&state={}').format(CLIENT_ID, REDIRECT_URI, SCOPE, STATE)
        return flask.redirect(authorization_uri)
    else:
        authorization_code = flask.request.args.get('code')
        data = {'code': authorization_code, 'client_id': CLIENT_ID, 'client_secret': CLIENT_SECRET, 'redirect_uri': REDIRECT_URI, 'grant_type': 'authorization_code', 'State': STATE}
        # fetch all the states stored within the datastore 
        query = client.query(kind="states")
        results = list(query.fetch())
        for i in results:
           if i['state'] == STATE:
            request = requests.post('https://oauth2.googleapis.com/token', data=data)
            flask.session['credentials'] = request.text
            return flask.redirect(flask.url_for('userinfo'))
        else:
            return ("State is invalid")

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)