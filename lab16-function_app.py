import logging
import azure.functions as func
import os
import base64
from azure.cosmos import CosmosClient

app = func.FunctionApp()

# Cosmos DB configuration from environment
COSMOS_ENDPOINT = os.environ["COSMOS_ENDPOINT"]
COSMOS_KEY = os.environ["COSMOS_KEY"]
DATABASE_NAME = "BadVisualization"        # Replace with your actual DB name
CONTAINER_NAME = "Visualization"      # Replace with your actual container name

def fetch_image_from_cosmos():
    client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)

    query = "SELECT TOP 1 c.imageBase64 FROM c ORDER BY c._ts DESC"
    results = list(container.query_items(query=query, enable_cross_partition_query=True))

    if not results:
        raise ValueError("No image data found in Cosmos DB")

    base64_data = results[0]['imageBase64']
    return base64.b64decode(base64_data)

@app.route(route="GetRandomVis", auth_level=func.AuthLevel.ANONYMOUS)
def GetRandomVis(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing GetRandomVis image request.')

    try:
        image_bytes = fetch_image_from_cosmos()
        return func.HttpResponse(
            body=image_bytes,
            status_code=200,
            mimetype="image/png",
            headers={
                "Content-Disposition": "inline; filename=visualization.png"
            }
        )
    except Exception as e:
        logging.error(f"Failed to fetch or return image: {str(e)}")
        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=500
        )
