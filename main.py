from fastapi

import FastAPI app = FastAPI() 

@app.get("/") 
async def root(): 
  return {"message": "Hello People, this is just a test"}
