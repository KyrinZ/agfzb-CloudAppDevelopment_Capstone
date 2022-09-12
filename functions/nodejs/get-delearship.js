const { CloudantV1 } = require("@ibm-cloud/cloudant");
const { IamAuthenticator } = require("ibm-cloud-sdk-core");

async function main(params) {
  try {
    const DATABASE = "dealerships";
    const authenticator = new IamAuthenticator({ apikey: params.IAM_API_KEY });
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator,
    });

    cloudant.setServiceUrl(params.COUCH_URL);
    let result = [];
    if (params.state) {
      result = (
        await cloudant.postFind({
          db: DATABASE,
          selector: { state: params.state },
        })
      ).result.docs.map((i) => ({
        id: i.id,
        city: i.city,
        state: i.state,
        st: i.st,
        address: i.address,
        zip: i.zip,
        lat: i.lat,
        long: i.long,
      }));
      if (result.length < 1) {
        return response(404, {
          message: "The state does not exist",
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
