# 🔞 NSFW Image Detection API

A production-ready **image moderation API** built with **FastAPI + PyTorch + Hugging Face Transformers**.  
It detects NSFW content in images and logs results into a PostgreSQL database.

---

## 🚀 Features

- 📸 Upload image for NSFW detection
- 🤖 AI model: `Falconsai/nsfw_image_detection`
- 📊 Confidence score output
- 🗄️ PostgreSQL logging (request tracking)
- ⚡ FastAPI high-performance backend
- 🐳 Docker support (deploy anywhere)

---

## 🧠 How It Works

1. User uploads an image
2. Model analyzes image content
3. Returns:
   - NSFW / SFW prediction
   - Confidence score
4. Stores result in PostgreSQL database

### 🔥 Detection Rule

```
NSFW = true if confidence ≥ 60%
```

---

## 📡 API Endpoint

### 🔹 POST `/nsfw-detect`

Upload an image file and get prediction result.

---

### 📥 Request

- Content-Type: `multipart/form-data`
- Field:
  - `image` → image file (jpg/png)

---

### 📤 Response

```json
{
  "success": true,
  "message": "Detection completed",
  "data": {
    "request_id": "uuid",
    "nsfw_detected": true,
    "confidence": 75.3
  }
}