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
    DATABASE_NAME = "reviews"

    try:
        authenticator = IAMAuthenticator(dict["IAM_API_KEY"])
        service = CloudantV1(authenticator=authenticator)
        service.set_service_url(dict["COUCH_URL"])

        if "dealerId" in dict:
            res = service.post_find(
                db="reviews",
                selector={"dealership": {"$eq": int(dict["dealerId"])}},
            ).get_result()["docs"]
            if not res:
                return response(404, {"message": "dealerId does not exist"})
            return response(
                200,
                [
                    {
                        "id": i["id"],
                        "dealership": i["dealership"],
                        "name": i["name"],
                        "purchase": i["purchase"],
                        "review": i["review"],
                    }
                    for i in res
                ],
            )
        res = service.post_all_docs(DATABASE_NAME, include_docs=True)

        return response(
            200,
            [
                {
                    "id": i["doc"]["id"],
                    "dealership": i["doc"]["dealership"],
                    "name": i["doc"]["name"],
                    "purchase": i["doc"]["purchase"],
                    "review": i["doc"]["review"],
                }
                for i in res.result["rows"]
            ],
        )
    except Exception as e:
        return response(500, {"message": "Something went wrong"})