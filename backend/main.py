from fastapi import FastAPI
from router.user_routes import router as user_router  # Import the `router` object
from router.note_routes import router as note_router

app = FastAPI()

app.include_router(user_router)  # Correctly include the user router
app.include_router(note_router)  # Correctly include the note router


@app.get("/")
async def root():
    return {"message": "Welcome to the API"}
