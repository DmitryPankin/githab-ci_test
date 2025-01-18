from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Recipe
from schemas import RecipeCreate

async def get_recipes(db: AsyncSession):
    result = await db.execute(select(Recipe).order_by(Recipe.views.desc(), Recipe.cook_time))
    return result.scalars().all()

async def get_recipe(db: AsyncSession, recipe_id: int):
    result = await db.execute(select(Recipe).filter(Recipe.id == recipe_id))
    return result.scalar_one_or_none()

async def create_recipe(db: AsyncSession, recipe: RecipeCreate):
    db_recipe = Recipe(**recipe.dict())
    db.add(db_recipe)
    await db.commit()
    await db.refresh(db_recipe)
    return db_recipe
