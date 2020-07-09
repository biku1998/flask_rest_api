# users
from flask_restful import Resource,reqparse
from models.user import UserModel

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
        if UserModel.find_by_username(data["username"]):
            return {"message":"username already exists !"},400

        user = UserModel(**data) # as we know the dict will only have username and password.
        user.save()

        return {"message":"user created !"},201





















