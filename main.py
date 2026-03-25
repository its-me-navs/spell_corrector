from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from spell_checker import correct_sentence

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/correct")
def correct(sentence : str):
    return {"corrected": correct_sentence(sentence)}
