<p align="center">
  <img src="doc/nightingale_logo.png" alt="Nightingale Logo" width="200"/>
</p>

!Disclaimer: This Repository is still in the making and is meant to become a bird call classification app for the edge.


# Run example deployment of nightingale bird call classifier on localhost

cd app/fastapi
uvicorn main:app --reload --host 127.0.0.1 --port 8000

( or uvicorn app.fastapi.main:app --reload --host 127.0.0.1 --port 8000, but for that the import of the classifier_head model has to be done relativ e to the path etc. )

curl -X POST   "http://127.0.0.1:8080/predict/"   -H "accept: application/json"   -H "Content-Type: multipart/form-data"
 -F "file=@data/birdclef-2024/train_audio_16/cohcuc1/XC19645.wav;type=audio/wav"


# Deploy docker container with running application

cd nightingale
docker build -t nightingale-service:latest .
docker run -p 8080:8080 nightingale-service:latest
http://localhost:8080
(only works if there is a bird_classifier_head.keras in the toplevel directory of the repository)


# how to setup ml flow tracking server on your local machine 
On windows:
* Install chocolatey package manager
    - Follow installation instructions as decribed here: https://chocolatey.org/install?_gl=1*13ngmui*_ga*MTIyMDc5OTIxMC4xNzU3OTM4NDcx*_ga_0WDD29GGN2*czE3NTc5Mzg0NzAkbzEkZzEkdDE3NTc5Mzg1MzIkajYwJGwwJGgw
* Install python:
    - Open cmd window with admin rights, then run:
    ```
    choco install python
    ```
    - Close and reopen cmd window (no admin rights required here)
    ```
    pip install mlflow
    ```
* If not already done, add the folder with the mlflow.exe to  the environment variable path 
    Run the following command to find the folder (should return something like: C:\Users\<YourUser>\AppData\Roaming\Python\Python39\Scripts)
    ```
    python -m site --user-base
    ```
* Run local ml flow tracking server
    ```
    mlflow server --host 127.0.0.1 --port 5757
    ```
    or to access it from the docker dev container (check [Mlflow](https://www.mlflow.org/docs/latest/ml/tracking/server/#tracking-auth) for security considerations)
    ```
    mlflow server --host 0.0.0.0 --port 5757
    ```

# connect to ml flow server from within the dev container

TODO
* pin python version
* define dev and production dependencies in pyproject.toml
* setup local ml flow tracking server
* load model from versioned model artifacts on tracking server/registry of ml flow
* clean repo
* add textual content and visually appealing content to readme
* sphinx documentation
* pytests
* create multi stage docker container
* implement CI/CD for build, test and deployments on github actions
* terraform deployment on cloud
* consider security aspects of application, eg user and attack surface of production container (check devops on geeks4geeks)
* Kubernetes
* describe the URI for the tracking server somewhere else than in the python scripts.
* create a config file for the hyperparameters
* Integrate ONNX 
* Check usage of Kubeflow

Idea for edge:

Data relevance & quality:
Spacial:
* Train the model used for edge deployment with the bird species that are most likely to occur in the geographic region of the location the edge device will be deployed. 

Temporal:
* different seasons come with different species as some birds migrate and some birds don't. Or just marginalize that temporal component out by using the data of one yearly cycle

Data Lifecycle:
* Do the types of species in a specific region change over time? E.g. due to climate change or other environmental impacts that make them migrate permanentely
* Perhaps it could also be beneficial to deploy a model on the edge in a specific location and have it predict the species it has been trained on and a class for species that are not part of the species it has be trained on --> all other possible sounds or species.
These outcomes could be sent to a server and be classified by a huge net, that knows much more or even all species around the world. Then these predictions together with the uploaded inputs could be used to retrain/update the deployed model at the location the data was recorded, that could help with data drift in general.
* Obtain background noise or in general other sounds to augment the data used to train the specific models.

