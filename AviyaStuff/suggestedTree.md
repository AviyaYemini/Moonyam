# Suggested Project Structure and API Overview

This document consolidates the recommended project layout together with the key APIs that glue the persistence, domain, and presentation layers. It mirrors the schema-backed design that the database imposes, ensuring every layer stays cohesive and object-oriented.

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
