from flask import Flask,jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from resources.user import UserRegister,User,UserLogin,TokenRefresh,UserLogout
from resources.item import Item,ItemList
from resources.store import Store,StoreList
app  = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True # if jwt raise Error, Flask will see.

# enable JWT blacklist
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_BLACKLIST_TOKEN_CHECK"] = ["access","refresh"]
app.secret_key = "309104d4eafaf335a65fafd277869a2d"

from blacklist import BLACKLIST
# there is also app.config["JWT_SECRET_KEY"] to set different key for app and JWT
api = Api(app)



@app.before_first_request
def create_tables():
    db.create_all()



# set up JWT
# jwt = JWT(app,authenticate,identity)
# set up JWT_exteneded
jwt = JWTManager(app)

# adding claims to JWT i.e attach extra peice of data
@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    print(identity)
    if identity == 1:
        return {"is_admin":True}
    return {"is_admin":False}

# check for the blacklist user
@jwt.token_in_blacklist_loader
def blacklist_check(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST 

# customize the message of token expire
# The following callbacks are used for customizing jwt response/error messages.
# The original ones may not be in a very pretty format (opinionated)
@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'description': 'The token has expired.',
        'error': 'token_expired'
    }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'description': 'Signature verification failed.',
        'error': 'invalid_token'
    }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'description': 'Request does not contain an access token.',
        'error': 'authorization_required'
    }), 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        'description': 'The token is not fresh.',
        'error': 'fresh_token_required'
    }), 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        'description': 'The token has been revoked.',
        'error': 'token_revoked'
    }), 401

api.add_resource(Store,"/store/<string:name>")
api.add_resource(StoreList,"/stores")
api.add_resource(Item,"/item/<string:name>")
api.add_resource(ItemList,"/items")
api.add_resource(UserRegister,"/register")
api.add_resource(User,"/user/<int:user_id>")
api.add_resource(UserLogin,"/login")
api.add_resource(TokenRefresh,"/refresh")
api.add_resource(UserLogout,"/logout")


if __name__ == "__main__":
    from db import db
    db.init_app(app)
    app.run(debug=True,port=8080)