from fastapi import FastAPI
import ollama

app = FastAPI()

@app.get("/")
def home():
	return {"message": "Welcome to the DeepScaleR Chatbot API"}

@app.get("/chat")
def chat(message: str):
	response = ollama.chat(model='deepscaler-chat', messages=[{"role": "user", "content": message}])
	return {"response": response["message"]}


if __name__ == "__main__":
	import uvicorn
	from pathlib import Path
	uvicorn.run(
		"chatbot_api:app",
		app_dir=str(Path(__file__).resolve().parent),
		host="0.0.0.0",
		port=8000,
		reload=True,
	)