from flask import jsonify, make_response


def success(dictionaryData={}):
    if not bool(dictionaryData):
        return make_response('', 204)

    return make_response(jsonify(dictionaryData), 200)


def badRequest(errorMessage=''):
    response = {"errorMessage": errorMessage}
    return make_response(jsonify(response), 400)
