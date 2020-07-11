from flask_restful import Resource,reqparse
from flask_jwt_extended import (jwt_required,get_jwt_claims,
                                jwt_optional,get_jwt_identity,
                                fresh_jwt_required)
import sqlite3
from models.item import ItemModel


class Item(Resource):

    # define a parser
    parser = reqparse.RequestParser()
    parser.add_argument(
            "price",
            type = float,
            required = True,
            help = "This field cannot be left blank"
    )
    parser.add_argument(
            "store_id",
            type = int,
            required = True,
            help = "Every item need to have a store"
    )
    
    @jwt_required
    def get(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(),200
        return {"message":"Item not found !"},400


    @fresh_jwt_required
    def post(self,name):
        # check if the item already exists
        if ItemModel.find_by_name(name):
            return {"message":f"item already exists !"},400

        request_data = Item.parser.parse_args()

        item = ItemModel(name,request_data["price"],request_data["store_id"])

        try:
            item.save()
        except:
            return {"message","Something went wrong !!"},500

        return item.json(),201
    
    @jwt_required
    def delete(self,name):
        # get the jwt claims to see of the user is admin or not
        claims = get_jwt_claims()
        if not claims["is_admin"]:
            return {"message":"Admin Access required to delete !"},401
        # check if the item exists or not
        item = ItemModel.find_by_name(name)
        if item:
            item.delete()
            return {"message":"item deleted !"},200     

        return {"message":"item don't exists !"},400    
        

    def put(self,name):
        data = Item.parser.parse_args()
        # get the item to update
        item = ItemModel.find_by_name(name)
        
        if item:
            try:
                item.price = data["price"]
                item.store_id = data["store_id"]
            except:
                return {"message":"Something went wrong !"},500
        else:
            try:
                item = ItemModel(name,data["price"],data["store_id"])
            except:
                return {"message":"Something went wrong !"},500
        
        item.save()

        return item.json(),200

class ItemList(Resource):

    @jwt_optional
    def get(self):
        user_id = get_jwt_identity()
        items = [item.json() for item in ItemModel.find_all()]

        if user_id:
            return {"Items":[item.json() for item in ItemModel.find_all()]}

        return {"Items":[item["name"] for item in items],
                "message":"Login to get full information"
                }

