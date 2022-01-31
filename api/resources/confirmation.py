from flask import render_template, make_response, request
from flask_restful import Resource
import traceback
from time import time

from ..schemas.user import UserListSchema
from ..models.confirmation import ConfirmationModel
from ..schemas.confirmation import ConfirmationSchema
from ..models.user import UserModel
# from resources.user import USER_NOT_FOUND
from ..libs.mailgun import MailGunException

#we are using this to handle all our error response
from ..libs.strings import gettext   

confirmation_schema = ConfirmationSchema()
user_list_schema = UserListSchema()


       

class Confirmation(Resource):
    # returns the confirmation page
    @classmethod
    def get(cls, confirmation_id: str):
        confirmation = ConfirmationModel.find_by_id(confirmation_id)
        
        if not confirmation:
            return {"message": gettext("confirmation_not_found")}, 404

        if confirmation.expired:
            return {"message": gettext("confirmation_link_expired")}, 400

        if confirmation.confirmed:
            return {"message": gettext("confirmation_already_confirmed")}, 400

        confirmation.confirmed = True
        confirmation.save_to_db()

        headers = {"Content-Type": "text/html"}
        return make_response(
            render_template("confirmation_page.html", email=confirmation.user.email),
            200,
            headers,
        )

class ConfirmationByUser(Resource):
    @classmethod
    def get(cls, user_id: int):
        """
        This endpoint is used for testing and viewing Confirmation models and should not be exposed to public.
        """
        
        user_json = request.get_json() if request.get_json() else dict(request.form)
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        return (
            {
              #This is only for testing for us to see the confirmation that exist in the database, so we don't have to go into the database and check for confirmtion
                "current_time": int(time()),
                # we filter the result by expiration time in descending order for convenience
                "confirmation": [
                    confirmation_schema.dump(each)
                    for each in user.confirmation.order_by(ConfirmationModel.expire_at)
                ],
            },
            200,
        )

    #THE ACTUAL RESEND CONFIRMATION
    @classmethod
    def post(cls):
        """
        This endpoint resend the confirmation email with a new confirmation model. It will force the current
        confirmation model to expire so that there is only one valid link at once.
        """
        
        user_json = request.get_json() if request.get_json() else dict(request.form)
        user_json = user_json['email']
        email = user_json
        user = UserModel.find_by_email(user_json)
        print(user)
        if not user:
            return {"message": gettext("user_not_found")}, 404
        user = user_list_schema.dump(user)
        user_id = user['id']

        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": gettext("user_not_found")}, 404

        try:
           
            confirmation = user.most_recent_confirmation  
            if confirmation:
                if confirmation.confirmed: 
                    return {"message": gettext("confirmation_already_confirmed")}, 400
                confirmation.force_to_expire() 

            new_confirmation = ConfirmationModel(user_id)  
            new_confirmation.save_to_db()
            
            user.send_confirmation_email() 
            return {"message": gettext("confirmation_resend_successful")}, 201
        except MailGunException as e:
            return {"message": str(e)}, 500
        except:
            traceback.print_exc()
            return {"message": gettext("confirmation_resend_fail")}, 500