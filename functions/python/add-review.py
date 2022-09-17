#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def response(code, data):
    return {
        "statusCode": code,
        "headers": {"Content-Type": "application/json"},
        "body": data,
    }

def main(dict):
    if dict.get("__ow_method") == "post":
        DATABASE_NAME = "reviews"
        try:
            authenticator = IAMAuthenticator(dict["IAM_API_KEY"])
            service = CloudantV1(authenticator=authenticator)
            service.set_service_url(dict["COUCH_URL"])
            res = service.post_document(
                db=DATABASE_NAME, document=dict["review"]
            ).get_result()
            return response(200, res)
        except Exception as e:
            return response(500, {"message": e})
    return response(405, {"message":"Method Not Allowed"})

