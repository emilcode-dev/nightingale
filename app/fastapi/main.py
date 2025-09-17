import tensorflow as tf
import tensorflow_hub as hub
from fastapi import FastAPI, UploadFile, File, HTTPException
import mlflow
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
# from nightingale.model.bird_call_classifier import BirdCallClassifier
from nightingale.model.classifier_head import ClassifierHead

yamnet_model = hub.load('https://tfhub.dev/google/yamnet/1')

# Load model of classifier head from ml flow registry
model_name = 'Reg-Bird-Call-Classifier-Head'
model_version_alias = "challenger"
TRACKING_URI_LOCAL = "http://host.docker.internal:5757"
mlflow.set_tracking_uri(TRACKING_URI_LOCAL)

# Get the model version using a model URI
model_uri = f"models:/{model_name}@{model_version_alias}"
classifier_head = mlflow.keras.load_model(model_uri)

# classifier_head = tf.keras.models.load_model('bird_classifier_head.keras')
bird_classes = ['Intermediate Egret', 'Common Hawk-Cuckoo', "Tickell's Leaf Warbler"]  # Example classes

app = FastAPI(title='Nightingale Bird Classifier API')

# Serve static files (frontend)
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# # By using @app.get("/") you are allowing the GET method to work for the / endpoint.
@app.get("/")
def home():
    return "Congratulations! Your API is working as expected. Now head over to http://docs"

@app.post("/predict/")
def prediction(file: UploadFile = File(...)):

    filename = file.filename
    fileExtension = filename.split(".")[-1] in ("wav")
    if not fileExtension:
        raise HTTPException(status_code=415, detail="Unsupported file provided.")
    
    # Read file contents
    wav_bytes = file.file.read()

    # Decode WAV file
    audio, sr = tf.audio.decode_wav(wav_bytes)
    waveform = tf.squeeze(audio, axis=-1)  # remove channel dimension if stereo
    waveform = tf.cast(waveform, tf.float32)

    # Make sure it's the right sample rate for YAMNet (16kHz)
    if sr != 16000:
        raise HTTPException(status_code=400, detail=f"Expected 16kHz audio, got {sr.numpy()}")

    _, embeddings, _ = yamnet_model(waveform)
    result = classifier_head(embeddings).numpy()
    inferred_class = bird_classes[result.mean(axis=0).argmax()]

    return { "Inferred class": inferred_class }


    
