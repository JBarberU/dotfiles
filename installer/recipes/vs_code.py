from recipe_base import RecipeBase, DPath, HPath

class VSCodeRecipe(RecipeBase):

  name = "VSCode"
  links = [
        (DPath("vs_code"), HPath(".config/Code/User"))
    ]


