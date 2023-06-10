from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, summarize

load_dotenv()

app = FastAPI()
origins = []
app.add_middleware(CORSMiddleware, allow_origins=origins,
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(auth.router)
app.include_router(summarize.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", reload=True, port=9000, host="0.0.0.0")
