# users
from connect_sqlite import get_connection
from flask_restful import Resource,reqparse

class User:
    def __init__(self,_id,username,password):
        self.id = _id
        self.username = username
        self.password = password

    
    @classmethod
    def find_by_username(cls,username):
        connection = get_connection()
        cursor = connection.cursor()

        result = cursor.execute("SELECT * FROM users WHERE username=?",(username,))
        row = result.fetchone()

        if row:
            user = cls(*row) # shorthand of (row[0],row[1],row[2])
        else:
            user = None
        
        connection.close()

        return user
    
    @classmethod
    def find_by_id(cls,_id):
        connection = get_connection()
        cursor = connection.cursor()

        result = cursor.execute("SELECT * FROM users WHERE id=?",(_id,))
        row = result.fetchone()

        if row:
            user = cls(*row) # shorthand of (row[0],row[1],row[2])
        else:
            user = None
        
        connection.close()

        return user



class UserRegister(Resource):
    # define a parser
    parser = reqparse.RequestParser()
    parser.add_argument(
            "username",
            type = str,
            required = True,
            help = "This field cannot be left blank"
    )
    parser.add_argument(
            "password",
            type = str,
            required = True,
            help = "This field cannot be left blank"
    )

    def post(self):

        data = UserRegister.parser.parse_args()

        # first verify if the user don't exists already
        if User.find_by_username(data["username"]):
            return {"message":"username already exists !"},400

        connection = get_connection()
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES(NULL,?,?)"

        cursor.execute(query,(data["username"],data["password"]))

        connection.commit()
        connection.close()

        return {"message":"user created !"},201





















