-- Moonyam Pantry App - SQLite schema

-- Core pantry entities ------------------------------------------------------
/*
 Ingredients
 -----------
 Purpose : Canonical list of all items the app can track.
 Why needed: Keeps ingredient metadata (name, default unit, category) in one
             place so recipes, inventory, and shopping list can reference it.

 Columns:
   - id: surrogate key used by foreign tables.
   - name: unique display name (e.g., "Tomato", "Olive Oil").
   - default_unit: recommended measurement base for recipes (grams, ml, pcs).
   - category: optional classification used for filtering or grocery aisles.
*/
CREATE TABLE Ingredients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    default_unit TEXT NOT NULL,
    category TEXT
);

/*
 Inventory
 ---------
 Purpose : Reflects what the user currently has in the pantry for each ingredient.
 Why needed: Core dataset for recommending recipes and tracking depletion.

 Columns:
   - ingredient_id: FK to Ingredients; also primary key (one row per ingredient).
   - quantity: amount available right now.
   - unit: unit for the stored quantity (can differ from recipe default).
   - expires_at: optional expiry date to warn the user about soon-to-expire food.
   - updated_at: audit trail for last modification (helps with sync/history).
*/
CREATE TABLE Inventory (
    ingredient_id INTEGER PRIMARY KEY,
    quantity REAL NOT NULL DEFAULT 0,
    unit TEXT NOT NULL,
    expires_at TEXT,
    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(id) ON DELETE CASCADE
);

/*
 ShoppingItems
 -------------
 Purpose : Represents items the user needs/wants to buy next.
 Rationale: Separating this from Inventory allows us to plan ahead without
            touching the actual pantry quantities until the user confirms.

 Columns:
   - id: unique row identifier for edits/deletes.
   - ingredient_id: foreign key to Ingredients (ensures consistent naming/unit).
   - quantity: how much to buy; REAL covers grams, liters, etc.
   - unit: explicit unit for this purchase (may differ from recipe default).
   - status: workflow state (pending/bought/skipped) with default pending.
   - notes: free-text for user hints (brand, alternatives).
   - created_at: timestamp for tracking when the task was created.
*/
CREATE TABLE ShoppingItems (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    unit TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(id)
);

-- Recipes -------------------------------------------------------------------
/*
 Recipes
 -------
 Purpose : Stores high-level information about each recipe the user can cook.
 Why needed: Base entity for recommendations, meal planning, and history.

 Columns:
   - id: auto-increment identifier used by relations.
   - name: user-facing title of the recipe.
   - description: short summary/teaser.
   - instructions: free-form text with cooking steps.
   - cuisine: optional tag for filtering (e.g., "Italian", "Vegan").
   - created_at: when the recipe was added (useful for sorting).
   - favorite: boolean/int flag marking user favorites.
*/
CREATE TABLE Recipes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    instructions TEXT,
    cuisine TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    favorite INTEGER NOT NULL DEFAULT 0
);

/*
 RecipeIngredients
 -----------------
 Purpose : Join table enumerating which ingredients (and how much) each recipe
           requires.
 Why needed: Enables querying cookable recipes versus inventory availability.

 Columns:
   - recipe_id: FK to Recipes; identifies the recipe.
   - ingredient_id: FK to Ingredients; the required component.
   - quantity: amount needed for the recipe’s default serving size.
   - unit: measurement unit for that quantity.
   - optional: flag to indicate optional garnish/seasoning so lack of it
               doesn’t block recommending the recipe.
   - PRIMARY KEY(recipe_id, ingredient_id): enforces a single row per pair.
*/
CREATE TABLE RecipeIngredients (
    recipe_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    quantity REAL NOT NULL,
    unit TEXT NOT NULL,
    optional INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (recipe_id, ingredient_id),
    FOREIGN KEY (recipe_id) REFERENCES Recipes(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(id)
);

-- Meal planning / history (optional but useful) ------------------------------
/*
 MealPlans
 ---------
 Purpose : Tracks future cooking plans (e.g., “Lasagna on Friday”).
 Why needed: Allows syncing shopping list with upcoming meals.

 Columns:
   - id: unique identifier for editing specific plans.
   - recipe_id: FK to Recipes indicating what will be cooked.
   - scheduled_for: date/time string when the meal is planned.
   - servings: number of servings to cook (affects ingredient scaling).
*/
CREATE TABLE MealPlans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    scheduled_for TEXT NOT NULL,
    servings INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (recipe_id) REFERENCES Recipes(id)
);

/*
 CookHistory
 -----------
 Purpose : Audit log of recipes the user actually cooked.
 Why needed: Enables analytics (most cooked dishes) and future AI prompts.

 Columns:
   - id: unique row id.
   - recipe_id: FK to Recipes; what was cooked.
   - cooked_at: timestamp; defaults to now.
   - notes: free-form feedback (e.g., “needed more salt”).
*/
CREATE TABLE CookHistory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER NOT NULL,
    cooked_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    FOREIGN KEY (recipe_id) REFERENCES Recipes(id)
);

-- Helpful indexes -----------------------------------------------------------
/*
 idx_recipeingredients_recipe: speeds up lookups of all ingredients for a recipe.
 idx_recipeingredients_ingredient: accelerates queries that find recipes using a
                                   given ingredient (for suggestions/alternatives).
 idx_shopping_status: allows quick filtering of shopping items by status so the
                      UI can show pending vs. bought lists efficiently.
*/
CREATE INDEX idx_recipeingredients_recipe ON RecipeIngredients(recipe_id);
CREATE INDEX idx_recipeingredients_ingredient ON RecipeIngredients(ingredient_id);
CREATE INDEX idx_shopping_status ON ShoppingItems(status);
