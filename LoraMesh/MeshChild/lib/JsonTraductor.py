import json

class JsonTraductor:

    def convertColorReciv(msgjson):
        ret = json.loads(msgjson)
        return ret["color"]

    def convertColorSend(msg):
        ret = {"color":msg}
        return json.dumps(ret)
