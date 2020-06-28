from flask import Flask,make_response,request
from flask_restful import Resource,Api

app  = Flask(__name__)
api = Api(app)

items = []


class Item(Resource):
    
    def get(self,name):
        # smaller code in place of iteration using for
        item = next(filter(lambda x:x["name"] == name,items),None)
        if item:
            return item,200
        return {"error":"item not found"},404


    def post(self,name):
        # check if the item already exists
        if next(filter(lambda x:x["name"] == name,items),None):
            # we have that item already
            return {"message":f"{name} already exists !"},400

        request_data = request.get_json()
        item = {"name":name,"price":request_data["price"]}
        items.append(item)
        return item,201

class ItemList(Resource):
    def get(self):
        return {"items":items}

api.add_resource(Item,"/item/<string:name>")
api.add_resource(ItemList,"/items")

if __name__ == "__main__":
    app.run(debug=True,port=8080)