#!/usr/bin/env bash
# Quick helper: prints tables + sample rows from the local SQLite DB.

set -euo pipefail

DB_PATH="src/main/resources/moonyam.db"

if [[ ! -f "$DB_PATH" ]]; then
  echo "Database not found at $DB_PATH" >&2
  exit 1
fi

sqlite3 "$DB_PATH" <<'SQL'
.mode column
.headers on

-- list tables
.tables

-- schema for core tables
.schema Ingredients Recipes RecipeIngredients Inventory ShoppingItems MealPlans CookHistory

-- sample rows
SELECT * FROM Recipes LIMIT 5;
SELECT * FROM Ingredients LIMIT 5;
SELECT * FROM RecipeIngredients LIMIT 5;
SELECT * FROM Inventory LIMIT 5;
SELECT * FROM ShoppingItems LIMIT 5;
SELECT * FROM MealPlans LIMIT 5;
SELECT * FROM CookHistory LIMIT 5;
SQL
