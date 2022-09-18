from datetime import datetime
import requests
import json

# import related models here

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import (
    Features,
    SentimentOptions,
)


from .models import CarDealer, DealerReview


def get_request(url, **kwargs):
    print("GET from {} ".format(url))
    try:
        response = requests.get(
            url, headers={"Content-Type": "application/json"}, params=kwargs
        )

    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, params=kwargs, json=json_payload)

    except:
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, **kwargs)
    if json_result:
        dealers = json_result
        for dealer in dealers:
            dealer_doc = dealer

            dealer_obj = CarDealer(
                address=dealer_doc["address"],
                city=dealer_doc["city"],
                full_name=dealer_doc["full_name"],
                id=dealer_doc["id"],
                lat=dealer_doc["lat"],
                long=dealer_doc["long"],
                short_name=dealer_doc["short_name"],
                st=dealer_doc["st"],
                zip=dealer_doc["zip"],
            )
            results.append(dealer_obj)

    return results


def get_dealer_reviews_from_cf(url, dealer_id):
    results = []
    json_result = get_request(url, dealerId=dealer_id)
    if json_result:
        reviews = json_result
        for review in reviews:
            dealer_doc: dict = review

            dealer_obj = DealerReview(
                dealership=dealer_doc.get("dealership"),
                name=dealer_doc.get("name"),
                purchase=dealer_doc.get("purchase"),
                review=dealer_doc.get("review"),
                purchase_date=(
                    datetime.strptime(dealer_doc.get("purchase_date"), "%d/%m/%Y")
                    if dealer_doc.get("purchase_date")
                    else None
                ),
                car_make=dealer_doc.get("car_make"),
                car_model=dealer_doc.get("car_model"),
                car_year=dealer_doc.get("car_year"),
                sentiment=analyze_review_sentiments(dealer_doc.get("review")),
                id=dealer_doc.get("id"),
            )
            results.append(dealer_obj)

    return results


def analyze_review_sentiments(dealerreview):
    authenticator = IAMAuthenticator("MZoPKJF-ZvnGvjStySdLIJMQTXeifN7lm0qmB6EZM3NC")
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version="2022-04-07", authenticator=authenticator
    )

    natural_language_understanding.set_service_url(
        "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/c5fba8fb-8b8d-4e4f-bf10-1b1bffa694cc"
    )

    response: dict = natural_language_understanding.analyze(
        text=dealerreview,
        features=Features(sentiment=SentimentOptions(targets=[dealerreview])),
    ).get_result()
    label = json.dumps(response, indent=2)

    label = response["sentiment"]["document"]["label"]

    return label
