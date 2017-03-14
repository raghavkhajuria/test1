import json
import random
import string

import apiai
from flask import Flask, request, abort, jsonify, render_template

from business_logic import business_logic
from intent_data_mapping import INTENT_DATA_MAPPING, INTENT_TICKET_MAPPING


def generate_session(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))

app = Flask(__name__)

CLIENT_ACCESS_TOKEN = "c0a8cd615d1c4099a9f2a6ace9999b22"
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)


@app.route('/api/v1/messages', methods=['POST'])
def process_message():

    try:
        if not request.json or 'message' not in request.json:
            abort(400)
    except AttributeError:
        abort(400)

    m = request.json.get('message')

    try:
        data = request.json.get('data')
    except KeyError:
        data = None

    try:
        session = request.json.get('sessionId')
    except KeyError:
        session = None

    req = ai.text_request()
    req.query = m

    if session:
        req.session_id = session
    else:
        req.session_id = generate_session(32)

    res = json.loads(req.getresponse().read())
    session = res['sessionId']

    try:
        response_messages = res['result']['fulfillment']['messages']
    except KeyError:
        response_messages = [{'speech': res['result']['fulfillment']['speech']}]

    score = res['result']['score']
    action = res['result']['action']

    intent = None
    entities = None

    if action == 'execute_bl':
        try:
            intent = res['result']['metadata']['intentName']
            entities = res['result']['contexts'][0]['parameters']
            response = business_logic(intent, entities, data, response_messages)
            if not response:
                raise KeyError
        except KeyError:
            response = ' '.join([m['speech'] for m in response_messages])
    else:
        response = ' '.join([m['speech'] for m in response_messages])

    try:
        highlighted = INTENT_DATA_MAPPING[intent]
    except KeyError:
        highlighted = None

    try:
        send_intent = INTENT_TICKET_MAPPING[intent[:2]]
    except (TypeError, AttributeError, KeyError):
        send_intent = 'No ticket type'


    return jsonify(
        response=response,
        score=score,
        sessionId=session,
        intent= send_intent,
        entities=entities,
        highlighted=highlighted
    )


@app.route('/new')
def index():
    return render_template('index.html')


@app.route('/')
def index_new():
    return render_template('new_index.html')


if __name__ == '__main__':
    app.run(debug=True)
