## 1. Project Directory Tree

```
Moonyam/
└─ src/main/kotlin/com/moonyam/
   ├─ App.kt
   │
   ├─ data/
   │  ├─ database/
   │  │  ├─ LocalDatabase.kt
   │  │  ├─ DbConfig.kt
   │  │  └─ DatabaseInitializer.kt
   │  │
   │  ├─ dao/
   │  │  ├─ IngredientsDao.kt
   │  │  ├─ InventoryDao.kt
   │  │  ├─ ShoppingDao.kt
   │  │  ├─ RecipesDao.kt
   │  │  ├─ RecipeIngredientsDao.kt
   │  │  ├─ MealPlansDao.kt
   │  │  └─ CookHistoryDao.kt
   │  │
   │  ├─ entities/
   │  │  ├─ IngredientEntity.kt
   │  │  ├─ InventoryEntity.kt
   │  │  ├─ ShoppingItemEntity.kt
   │  │  ├─ RecipeEntity.kt
   │  │  ├─ RecipeIngredientEntity.kt
   │  │  ├─ MealPlanEntity.kt
   │  │  └─ CookHistoryEntity.kt
   │  │
   │  └─ repositories/
   │     ├─ PantryRepository.kt
   │     ├─ RecipeRepository.kt
   │     ├─ PlanningRepository.kt
   │     └─ IngredientRepository.kt
   │
   ├─ logic/
   │  ├─ DataMapper.kt
   │  ├─ QueryBuilder.kt
   │  └─ DataValidator.kt
   │
   ├─ domain/
   │  ├─ models/
   │  │  ├─ Ingredient.kt
   │  │  ├─ InventoryItem.kt
   │  │  ├─ ShoppingItem.kt
   │  │  ├─ Recipe.kt
   │  │  ├─ RecipeIngredient.kt
   │  │  ├─ MealPlan.kt
   │  │  └─ CookHistoryEntry.kt
   │  │
   │  ├─ services/
   │  │  ├─ PantryManager.kt
   │  │  ├─ RecipeManager.kt
   │  │  └─ MealPlanner.kt
   │  │
   │  └─ usecases/
   │     ├─ GetCookableRecipes.kt
   │     ├─ AddMissingIngredients.kt
   │     ├─ SyncShoppingWithPlan.kt
   │     └─ MarkRecipeAsCooked.kt
   │
   ├─ ui/
   │  ├─ ConsoleMenu.kt
   │  └─ ViewModels.kt
   │
   └─ resources/
      ├─ moonyam.db
      ├─ db-schema.sql
      ├─ seed-data.sql
      └─ migrations/
         └─ v1_to_v2.sql
```

### Key Design Notes
- **data/database** centralizes configuration, connection management, and schema bootstrapping.
- **data/dao** surfaces thin interfaces over SQL operations for each table so repositories can stay agnostic about SQL syntax.
- **data/entities** mirrors the DB schema and captures column-level metadata.
- **data/repositories** compose DAOs and mapping logic, presenting an object-first API to the higher layers.
- **logic** encapsulates cross-cutting concerns for mapping, validation, and complex query construction.
- **domain** holds database-independent models and the service façade layer that orchestrates business workflows.
- **ui** contains presentation-specific logic such as console interactions.
- **resources** stores the SQLite database file along with schema and seed scripts.

## 2. Core APIs by Layer

The following sections summarize the responsibilities and typical method signatures for each logical layer. Where applicable, refer to the Mermaid `.mml` diagrams in `docs/diagrams/` for visual representations.

### 2.1 Database and DAO Layer

| Component | Responsibility | Representative API |
|-----------|----------------|--------------------|
| `DbConfig` | Load and validate database configuration (path, version, migration directory). | `fun load(): DbConfig` |
| `LocalDatabase` | Manage JDBC connections using the configuration. | `fun connect(): Connection`, `fun close(Connection)` |
| `DatabaseInitializer` | Apply schema and seed scripts during application bootstrap. | `fun initialize()`, `fun applySchema(schemaPath: String)` |
| `IngredientsDao` | CRUD operations for `ingredients`. | `fun getAll(): List<IngredientEntity>`, `fun insert(entity: IngredientEntity): Int` |
| `InventoryDao` | Manage pantry stock levels. | `fun getAll(): List<InventoryEntity>`, `fun update(entity: InventoryEntity)` |
| `ShoppingDao` | Manage shopping list items and statuses. | `fun getByStatus(status: String): List<ShoppingItemEntity>`, `fun insert(entity: ShoppingItemEntity): Int` |
| `RecipesDao` | Handle recipe definitions. | `fun getAll(): List<RecipeEntity>`, `fun findById(id: Int): RecipeEntity?` |
| `RecipeIngredientsDao` | Bridge recipes and their ingredient requirements. | `fun getByRecipeId(recipeId: Int): List<RecipeIngredientEntity>` |
| `MealPlansDao` | Schedule recipes for future dates. | `fun getAll(): List<MealPlanEntity>`, `fun insert(entity: MealPlanEntity): Int` |
| `CookHistoryDao` | Persist completed cooking events. | `fun insert(entity: CookHistoryEntity): Int`, `fun getRecent(limit: Int): List<CookHistoryEntity>` |

### 2.2 Mapping and Validation Layer

| Component | Responsibility | Representative API |
|-----------|----------------|--------------------|
| `DataMapper` | Translate between entities and domain models, ensuring association wiring. | `fun toInventoryItems(entities: List<InventoryEntity>, ingredients: List<IngredientEntity>): List<InventoryItem>` |
| `QueryBuilder` | Assemble complex SQL (joins, filters) used by DAOs. | `fun recipesWithIngredients(): String` |
| `DataValidator` | Enforce data invariants such as valid measurement units or non-negative quantities. | `fun assertValidUnit(unit: String)` |

### 2.3 Repository Layer

| Repository | Responsibility | Representative API |
|------------|----------------|--------------------|
| `IngredientRepository` | Manage the master list of ingredients and provide lookup utilities. | `fun listIngredients(): List<Ingredient>` |
| `PantryRepository` | Aggregate inventory and shopping DAOs to present a single pantry interface. | `fun getInventory(): List<InventoryItem>`, `fun getShoppingList(status: String = "pending"): List<ShoppingItem>` |
| `RecipeRepository` | Combine recipe entities with their ingredients; compute cookability. | `fun getAllRecipes(): List<Recipe>`, `fun getCookableRecipes(inventory: List<InventoryItem>): List<Recipe>` |
| `PlanningRepository` | Coordinate meal plan schedules and cooking history. | `fun getUpcomingMeals(): List<MealPlan>`, `fun recordCookEvent(entry: CookHistoryEntry)` |

### 2.4 Domain Services and Use Cases

| Service / Use Case | Responsibility | Representative API |
|--------------------|----------------|--------------------|
| `PantryManager` | Provide high-level pantry operations (sync, replenish, consume). | `fun syncShoppingWithInventory()` |
| `RecipeManager` | Expose recipe catalog actions including favorites and suggestions. | `fun markFavorite(recipeId: Int, favorite: Boolean)` |
| `MealPlanner` | Coordinate future meal plans and historic cooking entries. | `fun planMeal(recipeId: Int, date: String, servings: Int)` |
| `GetCookableRecipes` | Use case that finds recipes cookable with current inventory. | `fun execute(): List<Recipe>` |
| `AddMissingIngredients` | Compute missing items and persist them to shopping list. | `fun execute(recipeId: Int, desiredServings: Int)` |
| `SyncShoppingWithPlan` | Align the shopping list with upcoming meal plan requirements. | `fun execute()` |
| `MarkRecipeAsCooked` | Record that a recipe was cooked and update history. | `fun execute(recipeId: Int, notes: String?)` |

### 2.5 UI Integration Points

| Component | Responsibility | Representative API |
|-----------|----------------|--------------------|
| `ConsoleMenu` | Render navigation menus and trigger use cases. | `fun start()` |
| `ViewModels` | Adapt domain models for presentation in the console. | `fun fromRecipe(recipe: Recipe): RecipeViewModel` |

## 3. How to Use This Specification

1. **Implement DAOs** exactly as the schema requires, ensuring that each repository can rely on accurate data access primitives.
2. **Follow the mapping conventions** so that domain models never leak persistence-specific concerns (IDs stay encapsulated within entities unless explicitly needed by the domain).
3. **Extend services and use cases** by composing repositories; avoid duplicating SQL by introducing new DAO or query helpers when needed.
4. **Consult the Mermaid diagrams** in `docs/diagrams/` for class-level relationships and data-flow context when building or refactoring modules.

This structure balances separation of concerns with practical data workflows, enabling the project to evolve while staying aligned with OOP principles and the underlying database schema.

```
Moonyam/
└─ src/main/kotlin/com/moonyam/
├─ App.kt                              # Entry point of the entire application.
│                                       # Initializes database, repositories,
│                                       # and launches the console or GUI interface.
│
├─ data/                                # DATA LAYER – persistence and SQL access.
│  │
│  ├─ database/                         # Database configuration and lifecycle.
│  │  ├─ LocalDatabase.kt               # Manages SQLite connections via JDBC.
│  │  ├─ DbConfig.kt                    # Stores DB path, version, migration info.
│  │  └─ DatabaseInitializer.kt         # Executes db-schema.sql + seed-data.sql on startup.
│  │
│  ├─ dao/                              # Direct SQL interfaces (CRUD per table).
│  │  ├─ IngredientsDao.kt              # Access canonical ingredient list (Ingredients table).
│  │  ├─ InventoryDao.kt                # Manages pantry stock levels (Inventory table).
│  │  ├─ ShoppingDao.kt                 # Handles shopping items, statuses (ShoppingItems table).
│  │  ├─ RecipesDao.kt                  # CRUD for recipes metadata (Recipes table).
│  │  ├─ RecipeIngredientsDao.kt        # Manages Recipe–Ingredient links (RecipeIngredients table).
│  │  ├─ MealPlansDao.kt                # CRUD for scheduled meals (MealPlans table).
│  │  └─ CookHistoryDao.kt              # Inserts and queries cooking logs (CookHistory table).
│  │
│  ├─ entities/                         # 1:1 mapping to database tables (DTO-style objects).
│  │  ├─ IngredientEntity.kt            # id, name, default_unit, category.
│  │  ├─ InventoryEntity.kt             # ingredient_id, quantity, unit, expires_at, updated_at.
│  │  ├─ ShoppingItemEntity.kt          # id, ingredient_id, quantity, unit, status, notes.
│  │  ├─ RecipeEntity.kt                # id, name, description, instructions, cuisine, favorite.
│  │  ├─ RecipeIngredientEntity.kt      # recipe_id, ingredient_id, quantity, unit, optional.
│  │  ├─ MealPlanEntity.kt              # id, recipe_id, scheduled_for, servings.
│  │  └─ CookHistoryEntity.kt           # id, recipe_id, cooked_at, notes.
│  │
│  └─ repositories/                     # Abstraction layer that composes DAOs into business logic.
│     ├─ IngredientRepository.kt        # High-level API for ingredient lookups and metadata.
│     ├─ PantryRepository.kt            # Aggregates Inventory + Shopping DAOs into a unified pantry API.
│     ├─ RecipeRepository.kt            # Combines Recipes + RecipeIngredients + Ingredients.
│     └─ PlanningRepository.kt          # Connects MealPlans and CookHistory with recipes.
│
├─ logic/                               # LOGIC LAYER – data translation, validation, query helpers.
│  ├─ DataMapper.kt                     # Converts Entities ↔ Domain Models (e.g., RecipeEntity → Recipe).
│  ├─ QueryBuilder.kt                   # Builds complex dynamic SQL (joins, filters, ordering).
│  └─ DataValidator.kt                  # Ensures valid units, non-negative quantities, correct foreign keys.
│
├─ domain/                              # DOMAIN LAYER – core business logic & object model.
│  │
│  ├─ models/                           # Pure Kotlin data classes (no DB dependencies).
│  │  ├─ Ingredient.kt                  # Represents a unique tracked ingredient (name, default unit, category).
│  │  ├─ InventoryItem.kt               # Combines Ingredient + quantity + unit + expiry.
│  │  ├─ ShoppingItem.kt                # Represents an item to purchase (status, notes).
│  │  ├─ Recipe.kt                      # Full recipe definition, including ingredient list.
│  │  ├─ RecipeIngredient.kt            # A single ingredient required for a recipe.
│  │  ├─ MealPlan.kt                    # A scheduled cooking plan with servings and date.
│  │  └─ CookHistoryEntry.kt            # A record of a past cooked recipe, with optional notes.
│  │
│  ├─ services/                         # Managers that orchestrate multiple repositories.
│  │  ├─ PantryManager.kt               # High-level pantry logic (sync inventory, move bought items).
│  │  ├─ RecipeManager.kt               # Handles recipe suggestions, favorites, and filtering.
│  │  └─ MealPlanner.kt                 # Coordinates meal scheduling and cooking history.
│  │
│  └─ usecases/                         # Specific actions triggered by the user or UI.
│     ├─ GetCookableRecipes.kt          # Returns recipes that can be cooked with current inventory.
│     ├─ AddMissingIngredients.kt       # Finds missing ingredients for a recipe and adds them to ShoppingItems.
│     ├─ SyncShoppingWithPlan.kt        # Aligns shopping list with upcoming MealPlans.
│     └─ MarkRecipeAsCooked.kt          # Records a cooked recipe into CookHistory.
│
├─ ui/                                  # PRESENTATION LAYER – user interaction.
│  ├─ ConsoleMenu.kt                    # Command-line interface (temporary UI).
│  └─ ViewModels.kt                     # Adapts domain models for display (formatting, computed fields).
│
└─ resources/                           # Static assets and embedded runtime data.
├─ moonyam.db                        # SQLite database file used in runtime (if pre-seeded).
├─ db-schema.sql                     # Full DDL schema definition (matches app’s Entities & DAOs).
├─ seed-data.sql                     # Initial dataset (sample ingredients, recipes, etc.).
└─ migrations/                       # Versioned schema upgrade scripts.
└─ v1_to_v2.sql                   # Example migration file between schema versions.
```