from pydantic import BaseModel, ConfigDict


class RecipeBase(BaseModel):
    title: str
    cook_time: int
    ingredients: str
    description: str


class RecipeCreate(RecipeBase):
    pass


class Recipe(RecipeBase):
    id: int
    views: int

    model_config = ConfigDict(from_attributes=True)
