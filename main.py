from fastapi import FastAPI

app = FastAPI(title="Ingenious OS API", version="1.0")

@app.get("/")
def read_root():
    return {
        "message": "السيستم شغال فل الفففففف يا هندسة!",
        "system": "Ingenious OS",
        "status": "Online"
    }