from recipe_base import RecipeBase, DPath, HPath

class VSCodeRecipe(RecipeBase):

  name = "VSCode"
  mkdir_list = [HPath(".config/Code")]
  links = [
        (DPath("vs_code"), HPath(".config/Code/User"))
    ]

