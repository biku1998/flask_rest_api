from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
import sqlite3
from connect_sqlite import get_connection

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

    @classmethod
    def find_by_name(cls,name):
        connection = get_connection()
        cursor = connection.cursor()

        result = cursor.execute("SELECT * FROM items WHERE name=?",(name,))
        row = result.fetchone()
        connection.close()
        if row:
            return {"item":{"name":row[0],"price":row[1]}}
    
    @classmethod
    def insert_item(cls,item):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("INSERT INTO items VALUES(?,?)",(item["name"],item["price"]))
        connection.commit()
        connection.close()
    
    @classmethod
    def update_item(cls,item):
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("UPDATE items SET price=? WHERE name=?",(item["price"],item["name"]))
        connection.commit()
        connection.close()

    
    @jwt_required()
    def get(self,name):
        item = self.find_by_name(name)
        if item:
            return item,200
        return {"message":"Item not found !"},400


    def post(self,name):
        # check if the item already exists
        if self.find_by_name(name):
            return {"message":f"item already exists !"},400

        request_data = Item.parser.parse_args()
        item = {"name":name,"price":request_data["price"]}

        try:
            self.insert_item(item)
        except:
            return {"message","Something went wrong !!"},500

        return item,201

    def delete(self,name):
        # check if the item exists or not
        if not self.find_by_name(name):
            return {"message":"item don't exists !"},400

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM items WHERE name=?",(name,))
        connection.commit()
        connection.close()

        return {"message":"item deleted !"},200

    def put(self,name):
        data = Item.parser.parse_args()
        # get the item to update
        item = self.find_by_name(name)
        updated_item = {"name":name,"price":data["price"]}
        if item:
            try:
                self.update_item(updated_item)
            except:
                return {"message":"Something went wrong !"},500
        else:
            try:
                self.insert_item(updated_item)
            except:
                return {"message":"Something went wrong !"},500
        
        return updated_item,200

class ItemList(Resource):
    def get(self):
        connection = get_connection()
        cursor = connection.cursor()

        result = cursor.execute("SELECT * FROM items")
        

        items = []

        for item in result:
            items.append({"name":item[0],"price":item[1]})

        connection.close()
        
        return {"items":items},200

