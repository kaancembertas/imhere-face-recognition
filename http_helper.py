from flask import jsonify, make_response
import json


def success(dictionaryData={}):
    if not bool(dictionaryData):
        return make_response('', 204)

    return make_response(jsonify(dictionaryData), 200)


def badRequest(errorMessage=''):
    response = {"errorMessage": errorMessage}
    return make_response(jsonify(response), 400)


def notFound(errorMessage=''):
    response = {"errorMessage": errorMessage}
    return make_response(jsonify(response), 404)


def customErrorResponse(text, statusCode):
    if not bool(text):
        return make_response('', statusCode)

    return make_response(json.loads(text), statusCode)
