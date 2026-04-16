from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine, Base
from routes import router
import os
import uuid
from pathlib import Path

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Personal Blog API")

# 创建上传目录
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# 挂载静态文件目录
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router, prefix="/api")


@app.post("/api/upload/image")
async def upload_image(file: UploadFile = File(...)):
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp']:
        return {"errno": 1, "message": "不支持的图片格式"}
    
    new_filename = f"{uuid.uuid4().hex}{file_ext}"
    file_path = UPLOAD_DIR / new_filename
    
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    return {
        "errno": 0,
        "data": {
            "url": f"/uploads/{new_filename}",
            "alt": file.filename,
            "href": ""
        }
    }


@app.get("/")
def read_root():
    return {"message": "Welcome to Personal Blog API"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
