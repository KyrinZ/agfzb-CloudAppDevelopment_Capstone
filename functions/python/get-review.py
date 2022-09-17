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


def get_review(raw_reviews_from_db):
    reviews = [i['doc'] for i in raw_reviews_from_db]
    result = []
    fields = [
        "id",
        "dealership",
        "name",
        "purchase",
        "review",
        "purchase",
        "purchase_date",
        "car_make",
        "car_model",
        "car_year",
    ]
    for i in reviews:
        result.append({k:v for k,v in i.items() if k in fields})
    return result

def main(dict):
    DATABASE_NAME = "reviews"

    try:
        authenticator = IAMAuthenticator(dict["IAM_API_KEY"])
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(dict["COUCH_URL"])

        if "dealerId" in dict:
            res = service.post_find(
                db="reviews",
                fields=[
                    "id",
                    "dealership",
                    "name",
                    "purchase",
                    "review",
                    "purchase",
                    "purchase_date",
                    "car_make",
                    "car_model",
                    "car_year",
                ],
                selector={"dealership": {"$eq": int(dict["dealerId"])}},
            ).get_result()["docs"]
            if not res:
                return response(404, {"message": "dealerId does not exist"})
            return response(
                200,
                res,
            )
        res = service.post_all_docs(DATABASE_NAME, include_docs=True)

        return response(
            200,
            get_review(res.result["rows"]),
        )
    except Exception as e:
        return response(500, {"message": "Something went wrong"})
