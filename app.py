from fastapi import FastAPI, UploadFile, File
from transformers import pipeline
from PIL import Image
import io
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid
from db import Base, engine, NSFWLog

app = FastAPI()

classifier = pipeline("image-classification", model="Falconsai/nsfw_image_detection")

THRESHOLD = 0.60

SessionLocal = sessionmaker(bind=engine)


@app.post("/nsfw-detect")
async def nsfw_detect(image: UploadFile = File(...)):
    db = SessionLocal()
    request_id = uuid.uuid4()

    try:
        contents = await image.read()
        img = Image.open(io.BytesIO(contents)).convert("RGB")

        results = classifier(img)

        nsfw_score = 0.0
        for r in results:
            if r["label"].lower() == "nsfw":
                nsfw_score = r["score"]
                break

        confidence = round(nsfw_score * 100, 2)
        nsfw_detected = nsfw_score >= THRESHOLD

        log = NSFWLog(
            request_id=request_id,
            timestamp=datetime.utcnow(),
            nsfw_detected=nsfw_detected,
            confidence=confidence,
        )
        db.add(log)
        db.commit()

        return {
            "success": True,
            "message": "Detection completed",
            "data": {
                "request_id": str(request_id),
                "nsfw_detected": nsfw_detected,
                "confidence": confidence,
            },
        }

    except Exception as e:
        return {"success": False, "message": str(e), "data": None}

    finally:
        db.close()


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)
