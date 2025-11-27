# Recipe JSON Format Schema

This document describes the JSON format for importing recipes into the Snacklore database.

## Structure

The JSON file should be an array of recipe objects. Each recipe object contains:

### Top-Level Recipe Fields

- **`name`** (string, required): The name of the recipe (e.g., "Miso Ramen")
- **`username`** (string, required): The username of the recipe owner. The user must exist in the database.
- **`country`** (string, optional): The country name (e.g., "Japan", "United States"). If the country doesn't exist, it will need to be created first.
- **`state`** (string, optional): The state/province name (e.g., "California"). Must belong to the specified country. Can be `null` if not applicable.
- **`steps`** (array, required): An array of step objects, ordered by step_number.

### Step Object Fields

Each step in the `steps` array contains:

- **`step_number`** (integer, required): The order of this step (1, 2, 3, etc.)
- **`step_text`** (string, required): The instructions for this step
- **`ingredients`** (array, optional): An array of ingredient objects associated with this step

### Ingredient Object Fields

Each ingredient in the `ingredients` array contains:

- **`name`** (string, required): The name of the ingredient (e.g., "Flour", "Chicken Stock")
- **`amount`** (string, required): The amount needed (e.g., "2 cups", "1 tbsp", "3 large")
- **`username`** (string, required): The username of the user who added this ingredient (typically the recipe owner)

## Example

```json
[
  {
    "name": "Miso Ramen",
    "username": "System",
    "country": "Japan",
    "state": null,
    "steps": [
      {
        "step_number": 1,
        "step_text": "Prepare the broth base. In a pot, combine chicken stock and dashi. Bring to a simmer.",
        "ingredients": [
          {
            "name": "Chicken Stock",
            "amount": "4 cups",
            "username": "System"
          },
          {
            "name": "Dashi",
            "amount": "1 cup",
            "username": "System"
          }
        ]
      }
    ]
  }
]
```

## Notes

1. **User Requirements**: The `username` specified for the recipe and all ingredients must exist in the database. If importing recipes, ensure users are created first.

2. **Country/State Matching**: Country and state names must match exactly (case-insensitive) with existing database entries. If a country doesn't exist, it should be created before importing recipes.

3. **Step Ordering**: Steps should be ordered by `step_number` starting from 1. The step numbers don't need to be consecutive, but they should be in ascending order.

4. **Slug Generation**: Recipe slugs are auto-generated from `username` and `recipe_name` using the format: `{username}-{recipe_name}` (lowercased, with special characters replaced by hyphens).

5. **Optional Fields**: 
   - `country` and `state` can be `null` if the recipe doesn't have a specific location
   - `ingredients` array can be empty `[]` if a step doesn't require ingredients
   - `state` can be `null` even if `country` is specified (for country-level recipes)

6. **Multiple Ingredients per Step**: A step can have multiple ingredients, and each ingredient is stored separately in the database.

## Database Mapping

- Recipe `name` → `Recipe.name`
- Recipe `username` → Lookup `User.username` → `Recipe.user_id`
- Recipe `country` → Lookup `Country.name` → `Recipe.primary_country_id`
- Recipe `state` → Lookup `State.name` (within country) → `Recipe.primary_state_id`
- Step `step_number` → `Step.step_number`
- Step `step_text` → `Step.step_text`
- Ingredient `name` → `Ingredient.name`
- Ingredient `amount` → `Ingredient.amount`
- Ingredient `username` → Lookup `User.username` → `Ingredient.user_id`

