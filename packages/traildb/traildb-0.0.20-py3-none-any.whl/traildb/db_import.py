import pymongo
import os
import json
from mlflow.tracking import MlflowClient

class trail_init:
    def __init__(self, username, password):
        username = username
        password = password
        database = username.lower()
        URI = f"mongodb+srv://{username}:{password}@trail.hrnvwvp.mongodb.net/?retryWrites=true&w=majority"
        client = pymongo.MongoClient(URI)
        self.db = client[database]



    def log_experiment(self, mlflowrun, parent, data_meta):
        tags = {k: v for k, v in mlflowrun.data.tags.items() if not k.startswith("mlflow.")}
        artifacts = [f.path for f in MlflowClient().list_artifacts(mlflowrun.info.run_id, "model")]
        d = {}
        d['run_id'] = mlflowrun.info.run_id
        d['time_stamp'] = mlflowrun.info.start_time/1000.0
        d['user']= mlflowrun.info.user_id
        d['artifacts'] = artifacts
        d['params'] = mlflowrun.data.params
        d['metrics'] = mlflowrun.data.metrics
        d['tags'] = tags
        d['parent'] = parent
        d['data'] = data_meta
        #print(d)
        #with open('data.json', 'w') as fp:
        #    json.dump(d, fp)
        #DB_import.JSON_to_db(d)
        collection = self.db['instance_run']
        collection.insert_one(d)

    def get_run_info(self):
        pass