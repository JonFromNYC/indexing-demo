import os
import requests
from dotenv import load_dotenv
import json

# Load environment variables from .env
load_dotenv()
DOMAIN = os.getenv("DOMAIN")
# Define the API URL and headers
url = "https://support-lab-be.glean.com/api/index/v1/indexdocument"

headers = {
    "Authorization": os.getenv("BEARER_TOKEN"),
    "Content-Type": "application/json"
}

# Load the documents from the data folder
data_folder = "data/documents/"

# load document opens a file and returns it as JSON. Helper Function.
def load_document(filename):
    with open(os.path.join(data_folder, filename), "r") as file:
        return json.load(file)

# Loop through all JSON files in the documents folder
for filename in os.listdir(data_folder):
    if filename.endswith(".json"):

        document = load_document(filename)

        # Get sections from the document
        document_data = document.get("document", {})
        body = document_data.get("body", {})
        owner = document_data.get("owners", [{}])[0]  # Taking the first owner if available
        permission = document_data.get("permissions", {})

        # Build the payload for the API request
        payload = {
            "version": 1,
            "document": {
                "title": document_data.get("title"),
                "filename": filename,
                "container": "JonFromNashville",
                "containerDatasourceId": "my-container-datasource-id",
                "containerObjectType": "json",
                "datasource": document_data.get("datasource"),
                "objectType": document_data.get("objectType"),
                "viewURL": document_data.get("viewURL"),
                "id": document_data.get("id"),
                "summary": {
                    "mimeType": body.get("mimeType"),
                    "textContent": body.get("textContent", ""),
                },
                "body": {
                    "mimeType": body.get("mimeType"),
                    "textContent": body.get("textContent"),
                },
                "author": {
                    "email": "alex@glean-sandbox.com",
                    "datasourceUserId": "alex@glean-sandbox.com",
                    "name": "Jonathan Garcia",
                },
                "owner": {
                    "email": "alex@glean-sandbox.com",
                    "datasourceUserId": owner.get("datasourceUserId"),
                    "name": owner.get("name"),
                },
                "permissions": {
                    "allowAnonymousAccess": True,
                    "allowAllDatasourceUsersAccess": True
                },
            },
        }

        # Send the API request to index the document
        response = requests.request("POST", url, json=payload, headers=headers)

        # Print the response for debugging
        print(f"Indexed document {filename}: {response.status_code} - {response.text}")
