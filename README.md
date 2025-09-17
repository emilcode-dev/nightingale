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

