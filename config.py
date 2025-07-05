import os
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "webhookDB"
COLLECTION_NAME = "events"
WEBHOOK_SECRET="mysecret123"