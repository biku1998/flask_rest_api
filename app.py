from flask import Flask,make_response,request
from flask_restful import Resource,Api,reqparse
from flask_jwt import JWT,jwt_required
from security import authenticate,identity

app  = Flask(__name__)
app.secret_key = "309104d4eafaf335a65fafd277869a2d"
api = Api(app)

# set up JWT
jwt = JWT(app,authenticate,identity)

items = []


class Item(Resource):

    # define a parser
    parser = reqparse.RequestParser()
    parser.add_argument(
            "price",
            type = float,
            required = True,
            help = "This field cannot be left blank"
    )
    
    @jwt_required() # first authenticate and then we can call get
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

        request_data = Item.parser.parse_args()
        item = {"name":name,"price":request_data["price"]}
        items.append(item)
        return item,201

    def delete(self,name):
        global items # if we don't do this python will give error
        # check if the item to be deleted is there or not.
        if next(filter(lambda x:x["name"] == name,items),None):
            # delete it
            items = list(filter(lambda x:x["name"] != name,items))
            return {"message":"Item deleted !"},200
        return {"error":"Item not found !"},400

    def put(self,name):
        data = Item.parser.parse_args()
        # get the item to update
        item = next(filter(lambda x:x["name"] == name,items),None)

        if item:
            # update the item
            item.update(data)
        else:
            # create the item
            item = {"name":name,"price":data["price"]}
            items.append(item)
        return item,200

class ItemList(Resource):
    def get(self):
        return {"items":items}

api.add_resource(Item,"/item/<string:name>")
api.add_resource(ItemList,"/items")

if __name__ == "__main__":
    app.run(debug=True,port=8080)