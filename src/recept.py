from dataclasses import dataclass

@dataclass
class Recept:
    meal_Name: str
    meal_Category: str
    meal_Geography: str
    meal_Instructions: str
    meal_Image: str
    meal_Video: str
    meal_Ingredients: list[str]
    meal_Measures: list[str]
    meal_source: str