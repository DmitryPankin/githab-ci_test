from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_app.crud import create_recipe_in_db, get_recipe, get_recipes
from fastapi_app.database import SessionLocal, engine
from fastapi_app.models import Base
from fastapi_app.schemas import Recipe, RecipeCreate

app = FastAPI()


async def get_db():
    async with SessionLocal() as session:
        yield session


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/recipes", response_model=List[Recipe])
async def read_recipes(
    skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)
):
    recipes = await get_recipes(db)
    return recipes


@app.get("/recipes/{recipe_id}", response_model=Recipe)
async def read_recipe(recipe_id: int, db: AsyncSession = Depends(get_db)):
    recipe = await get_recipe(db, recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@app.post("/recipes", response_model=Recipe)
async def create_recipe(recipe: RecipeCreate, db: AsyncSession = Depends(get_db)):
    return await create_recipe_in_db(recipe, db)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
