## app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.features.pins.router import router as pins_router
from app.features.pin_detail.nara.router import router as nara_router
from app.features.pin_detail.matsu.router import router as matsu_router
from app.post.pin.matsu.router import router as matsu_write_router
from app.post.pin.nara.router import router as nara_write_router

app = FastAPI(
    title="Pins API",
    debug=settings.app_debug,
    redirect_slashes=False,
    docs_url="/docs",
)

# CORS設定
# allow_origins=settings.app_originsに要変更
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # すべてのオリジンを許可
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ルータ登録
app.include_router(pins_router)
app.include_router(nara_router)
app.include_router(matsu_router)
app.include_router(matsu_write_router)
app.include_router(nara_write_router)

# uvicorn起動用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )