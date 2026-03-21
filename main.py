import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# --- CHANGED: Use VertexAI instead of GoogleGenerativeAI ---
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

app = FastAPI(title="LangChain App for Historical Figures (Vertex AI)")

# 1. Setup Vertex AI Model
# No API key needed here. It uses the Cloud Run Service Account automatically.
llm = ChatVertexAI(
    model="gemini-2.5-flash", # Vertex AI uses standard model names
    temperature=0.7,
    location="us-central1"
)

# 2. Define the Prompt
prompt = ChatPromptTemplate.from_template(
    "You are an expert Historian. For the historical personality {name}, "
    "you are able to accurately tell their birth date and birth country. "
    "Return the output in the JSON format containing name, birthDate, birthCountry. "
    "In case you are unable to retrieve birthDate or birthCountry, just have the unknown values as null. "
    "Ensure the response is a valid json object only."
)
output_parser = JsonOutputParser()

# Chain: Prompt -> Model -> Json Output Parser
chain = prompt | llm | output_parser

# 3. Define Request Model
class QueryRequest(BaseModel):
    name: str

# 4. Define Endpoint
@app.post("/chat")
async def chat(request: QueryRequest):
    try:
        response = await chain.ainvoke({"name": request.name})
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    return {"status": "ok", "service": "CI/CD-Final-Link-Test"}
# Triggering redeploy
