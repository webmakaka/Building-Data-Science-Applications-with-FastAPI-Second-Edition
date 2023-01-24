import asyncio
import io
from pathlib import Path

import torch
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from pydantic import BaseModel
from transformers import YolosFeatureExtractor, YolosForObjectDetection


class Object(BaseModel):
    box: tuple[float, float, float, float]
    label: str


class Objects(BaseModel):
    objects: list[Object]


class ObjectDetection:
    feature_extractor: YolosFeatureExtractor | None = None
    model: YolosForObjectDetection | None = None

    def load_model(self) -> None:
        """Loads the model"""
        self.feature_extractor = YolosFeatureExtractor.from_pretrained(
            "hustvl/yolos-tiny"
        )
        self.model = YolosForObjectDetection.from_pretrained("hustvl/yolos-tiny")

    def predict(self, image: Image.Image) -> Objects:
        """Runs a prediction"""
        if not self.feature_extractor or not self.model:
            raise RuntimeError("Model is not loaded")
        inputs = self.feature_extractor(images=image, return_tensors="pt")
        outputs = self.model(**inputs)

        target_sizes = torch.tensor([image.size[::-1]])
        results = self.feature_extractor.post_process(
            outputs, target_sizes=target_sizes
        )[0]

        objects: list[Object] = []
        for score, label, box in zip(
            results["scores"], results["labels"], results["boxes"]
        ):
            if score > 0.7:
                box_values = box.tolist()
                label = self.model.config.id2label[label.item()]
                objects.append(Object(box=box_values, label=label))
        return Objects(objects=objects)


app = FastAPI()
object_detection = ObjectDetection()


async def receive(websocket: WebSocket, queue: asyncio.Queue):
    while True:
        bytes = await websocket.receive_bytes()
        try:
            queue.put_nowait(bytes)
        except asyncio.QueueFull:
            pass


async def detect(websocket: WebSocket, queue: asyncio.Queue):
    while True:
        bytes = await queue.get()
        image = Image.open(io.BytesIO(bytes))
        objects = object_detection.predict(image)
        await websocket.send_json(objects.dict())


@app.websocket("/object-detection")
async def ws_object_detection(websocket: WebSocket):
    await websocket.accept()
    queue: asyncio.Queue = asyncio.Queue(maxsize=1)
    receive_task = asyncio.create_task(receive(websocket, queue))
    detect_task = asyncio.create_task(detect(websocket, queue))
    try:
        done, pending = await asyncio.wait(
            {receive_task, detect_task},
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()
        for task in done:
            task.result()
    except WebSocketDisconnect:
        pass


@app.get("/")
async def index():
    return FileResponse(Path(__file__).parent / "index.html")


static_files_app = StaticFiles(directory=Path(__file__).parent / "assets")
app.mount("/assets", static_files_app)


@app.on_event("startup")
async def startup():
    object_detection.load_model()
