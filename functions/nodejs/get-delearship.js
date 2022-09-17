/**
 *
 * main() will be run when you invoke this action
 *
 * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
 *
 * @return The output of this action, which must be a JSON object.
 *
 */
const { CloudantV1 } = require("@ibm-cloud/cloudant");
const { IamAuthenticator } = require("ibm-cloud-sdk-core");

async function main({ IAM_API_KEY, COUCH_URL, state, dealerId }) {
  try {
    const DATABASE = "dealerships";
    const authenticator = new IamAuthenticator({ apikey: IAM_API_KEY });
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator,
    });

    cloudant.setServiceUrl(COUCH_URL);
    let result = [];

    if (state || dealerId) {
      const selector = {};
      if (dealerId) {
        selector.id = {
          $eq: parseInt(dealerId),
        };
      } else if (state) {
        selector.state = {
          $eq: state,
        };
      }

      result = (
        await cloudant.postFind({
          db: DATABASE,
          fields: [
            "id",
            "city",
            "state",
            "st",
            "address",
            "zip",
            "lat",
            "long",
            "full_name",
            "short_name",
          ],
          selector: selector,
        })
      ).result.docs;

      if (result.length < 1) {
        const msg = dealerId
          ? "dealerId does not exist"
          : "The state does not exist";
        return response(404, {
          message: msg,
        });
      }
    } else {
      result = (
        await cloudant.postAllDocs({
          db: DATABASE,
          includeDocs: true,
        })
      ).result.rows.map((i) => ({
        id: i.doc.id,
        city: i.doc.city,
        state: i.doc.state,
        st: i.doc.st,
        address: i.doc.address,
        zip: i.doc.zip,
        lat: i.doc.lat,
        long: i.doc.long,
        full_name: i.doc.full_name,
        short_name: i.doc.short_name,
      }));

      if (result.length < 1) {
        return response(404, {
          message: "The database is empty",
        });
      }
    }
    return response(200, result);
  } catch (error) {
    console.log(error);
    return response(500, {
      message: "Something went wrong on the server",
    });
  }
}

function response(code, data) {
  return {
    statusCode: code,
    headers: { "Content-Type": "application/json" },
    body: data,
  };
}
