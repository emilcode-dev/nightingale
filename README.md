Start local mlflow server
mlflow server --host 127.0.0.1 --port 8080


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


# how to setup ml flow tracking server on your local machine and connect to it from within the dev container



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

