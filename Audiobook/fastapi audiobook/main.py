from fastapi import FastAPI
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse 
import pyttsx3
import PyPDF2
import io
import sys
import subprocess
from gtts import gTTS
import pandas as pd

some_file_path = "student.mp3"
app = FastAPI()



@app.get('/')
def serverstatus():
    return {"status": "Running"}

@app.post("/files/")
async def create_file(upload_file: UploadFile = File(...)):
    pdffile= await upload_file.read()
    filename=upload_file.filename
    return processAudio(pdffile,filename)


@app.post("/pdf/")
async def create_file(upload_file: UploadFile = File(...)):
    pdffile= await upload_file.read()
    f=open(upload_file.filename,"wb")
    f.write(pdffile)
    f.close()
    df=pd.read_csv("data.csv")
    print(df.head())
    df.append({"filename" :upload_file.filename,"status":0})
    df.to_csv("data.csv")
    df.head()
    return {"status": "file sent for process "}




@app.get("/streamaudio")
def main(filename:str):  
    def iterfile():  
        with open(filename, mode="rb") as file_like:  
            yield from file_like  

    return StreamingResponse(iterfile(), media_type="audio/mp3")


def processAudio(pdffile,filename):

    reader = PyPDF2.PdfFileReader(io.BytesIO(pdffile))
    print(type(reader))
    audio_reader = pyttsx3.init()
    audio_reader.setProperty("rate",100)
     
    full_text=""
    for page in range(reader.numPages):
        next_page = reader.getPage(page)
        content = next_page.extractText()
        full_text += content
    mp3_fp = io.BytesIO()

    tts = gTTS(full_text)
    print(dir(tts))
    tts.write_to_fp(mp3_fp)
    audio_file = f'{filename}.mp3'
    tts.save(audio_file)
   
    return { "filename": filename}
    


