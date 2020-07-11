# users
from flask_restful import Resource,reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                jwt_refresh_token_required,
                                get_jwt_identity,
                                jwt_required,
                                get_raw_jwt)
from blacklist import BLACKLIST

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


class User(Resource):
    
    @classmethod
    def get(cls,user_id):
        user =  UserModel.find_by_id(user_id)

        if user:
            return user.json()

        return {"message":"User not found !"},404

    @classmethod
    def delete(cls,user_id):
        user =  UserModel.find_by_id(user_id)

        if user:
            user.delete()
            return {"message":"User deleted !"}
            
        return {"message":"User not found !"},404



class UserLogin(Resource):

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

    @classmethod
    def post(cls):
        data = cls.parser.parse_args()
        user = UserModel.find_by_username(data["username"])

        if user and safe_str_cmp(user.password,data["password"]):
            access_token = create_access_token(identity=user.id,fresh=True)
            refresh_token = create_refresh_token(identity=user.id)

            return {
                "access_token":access_token,
                "refresh_token":refresh_token
            },200
        
        return {"message":"Invalid Creds ! "},401


class UserLogout(Resource):
    
    @jwt_required
    def post(self):
        jti = get_raw_jwt().get("jti") # jwt id
        BLACKLIST.add(jti)
        return {"message":"logged out successfully !"},200



class TokenRefresh(Resource):
    
    @jwt_refresh_token_required
    def post(self):
        # get the current user
        current_user = get_jwt_identity()

        # create a JWT token
        new_token = create_access_token(identity=current_user,fresh=False)

        return {"access_token":new_token},200


















