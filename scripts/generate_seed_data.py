#!/usr/bin/env python3
"""
Generate seed SQL data for the Moonyam pantry app.

The script creates INSERT statements aligned with docs/db-schema.sql and writes
them to docs/seed-data.sql. Data includes hundreds of ingredients, sample
inventory/shopping rows, dozens of recipes with ingredient links, and planning
tables to showcase realistic usage.
"""

from __future__ import annotations

import datetime as dt
import random
from pathlib import Path
from typing import Dict, List, Sequence

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "seed-data.sql"

# Ingredient catalog ---------------------------------------------------------
INGREDIENTS_BY_CATEGORY: Dict[str, Sequence[tuple[str, str]]] = {
    "Produce": [
        ("Roma Tomato", "pcs"),
        ("Cherry Tomato", "pcs"),
        ("Heirloom Tomato", "pcs"),
        ("English Cucumber", "pcs"),
        ("Persian Cucumber", "pcs"),
        ("Kirby Cucumber", "pcs"),
        ("Red Onion", "pcs"),
        ("Yellow Onion", "pcs"),
        ("White Onion", "pcs"),
        ("Sweet Onion", "pcs"),
        ("Baby Spinach", "g"),
        ("Kale Leaves", "g"),
        ("Arugula", "g"),
        ("Butter Lettuce", "pcs"),
        ("Iceberg Lettuce", "pcs"),
        ("Romaine Lettuce", "pcs"),
        ("Carrot", "pcs"),
        ("Baby Carrot", "g"),
        ("Russet Potato", "pcs"),
        ("Yukon Gold Potato", "pcs"),
        ("Sweet Potato", "pcs"),
        ("Fingerling Potato", "pcs"),
        ("Broccoli Florets", "g"),
        ("Cauliflower Florets", "g"),
        ("Red Bell Pepper", "pcs"),
        ("Green Bell Pepper", "pcs"),
        ("Yellow Bell Pepper", "pcs"),
        ("Orange Bell Pepper", "pcs"),
        ("Zucchini", "pcs"),
        ("Yellow Squash", "pcs"),
        ("Eggplant", "pcs"),
        ("Butternut Squash", "pcs"),
        ("Acorn Squash", "pcs"),
        ("Jalapeno", "pcs"),
        ("Serrano Pepper", "pcs"),
        ("Poblano Pepper", "pcs"),
        ("Fresno Chili", "pcs"),
        ("Portobello Mushroom", "pcs"),
        ("Cremini Mushroom", "pcs"),
        ("Shiitake Mushroom", "pcs"),
        ("Garlic Bulb", "pcs"),
        ("Shallot", "pcs"),
        ("Ginger Root", "g"),
        ("Avocado", "pcs"),
        ("Green Beans", "g"),
        ("Asparagus Spears", "g"),
        ("Brussels Sprouts", "g"),
        ("Leek", "pcs"),
        ("Fresh Basil", "g"),
        ("Fresh Cilantro", "g"),
        ("Fresh Parsley", "g"),
        ("Fresh Mint", "g"),
        ("Fresh Dill", "g"),
        ("Fresh Rosemary", "g"),
        ("Fresh Thyme", "g"),
        ("Fresh Sage", "g"),
        ("Green Onion", "pcs"),
        ("Celery", "pcs"),
        ("Lemon", "pcs"),
        ("Lime", "pcs"),
        ("Orange", "pcs"),
        ("Grapefruit", "pcs"),
        ("Granny Smith Apple", "pcs"),
        ("Honeycrisp Apple", "pcs"),
        ("Banana", "pcs"),
        ("Pear", "pcs"),
        ("Strawberries", "g"),
        ("Blueberries", "g"),
        ("Blackberries", "g"),
        ("Raspberries", "g"),
        ("Mango", "pcs"),
        ("Pineapple", "pcs"),
        ("Watermelon", "pcs"),
        ("Cantaloupe", "pcs"),
        ("Kiwi", "pcs"),
        ("Navel Orange", "pcs"),
        ("Coconut", "pcs"),
        ("Fresh Turmeric", "g"),
        ("Green Cabbage", "pcs"),
        ("Red Cabbage", "pcs"),
        ("Bok Choy", "pcs"),
        ("Snow Peas", "g"),
        ("Sugar Snap Peas", "g"),
        ("Radish", "pcs"),
        ("Beetroot", "pcs"),
        ("Turnip", "pcs"),
        ("Daikon", "pcs"),
        ("Plantain", "pcs"),
        ("Passion Fruit", "pcs"),
        ("Dragon Fruit", "pcs"),
        ("Starfruit", "pcs"),
        ("Papaya", "pcs"),
        ("Pomegranate", "pcs"),
        ("Apricot", "pcs"),
        ("Plum", "pcs"),
        ("Peach", "pcs"),
        ("Nectarine", "pcs"),
        ("Cherries", "g"),
        ("Cranberries", "g"),
    ],
    "Dairy & Eggs": [
        ("Whole Milk", "ml"),
        ("Skim Milk", "ml"),
        ("Almond Milk", "ml"),
        ("Oat Milk", "ml"),
        ("Heavy Cream", "ml"),
        ("Half and Half", "ml"),
        ("Greek Yogurt", "g"),
        ("Plain Yogurt", "g"),
        ("Vanilla Yogurt", "g"),
        ("Sour Cream", "g"),
        ("Cottage Cheese", "g"),
        ("Cheddar Cheese", "g"),
        ("Mozzarella Cheese", "g"),
        ("Parmesan Cheese", "g"),
        ("Feta Cheese", "g"),
        ("Goat Cheese", "g"),
        ("Ricotta Cheese", "g"),
        ("Cream Cheese", "g"),
        ("Mascarpone Cheese", "g"),
        ("Butter Unsalted", "g"),
        ("Butter Salted", "g"),
        ("Ghee", "g"),
        ("Large Eggs", "pcs"),
        ("Pastured Eggs", "pcs"),
        ("Egg Whites", "ml"),
        ("Egg Yolks", "pcs"),
        ("Buttermilk", "ml"),
    ],
    "Proteins": [
        ("Chicken Breast", "g"),
        ("Chicken Thigh", "g"),
        ("Ground Chicken", "g"),
        ("Ground Turkey", "g"),
        ("Ground Beef 80-20", "g"),
        ("Ground Beef 90-10", "g"),
        ("Sirloin Steak", "g"),
        ("Pork Chops", "g"),
        ("Pork Tenderloin", "g"),
        ("Bacon Strips", "g"),
        ("Prosciutto", "g"),
        ("Smoked Salmon", "g"),
        ("Cod Fillet", "g"),
        ("Salmon Fillet", "g"),
        ("Shrimp Large", "g"),
        ("Scallops", "g"),
        ("Tofu Firm", "g"),
        ("Tofu Extra Firm", "g"),
        ("Tempeh", "g"),
        ("Black Beans Dried", "g"),
        ("Chickpeas Dried", "g"),
        ("Lentils Green", "g"),
        ("Lentils Red", "g"),
        ("Cannellini Beans Dry", "g"),
        ("Kidney Beans Dry", "g"),
        ("Edamame Shelled", "g"),
        ("Quinoa Raw", "g"),
        ("Seitan", "g"),
        ("Turkey Sausage", "g"),
        ("Italian Sausage", "g"),
        ("Chorizo", "g"),
        ("Ham Slices", "g"),
        ("Salami", "g"),
    ],
    "Pantry Staples": [
        ("All-Purpose Flour", "g"),
        ("Whole Wheat Flour", "g"),
        ("Bread Flour", "g"),
        ("Almond Flour", "g"),
        ("Cornmeal", "g"),
        ("White Sugar", "g"),
        ("Brown Sugar", "g"),
        ("Powdered Sugar", "g"),
        ("Baking Powder", "g"),
        ("Baking Soda", "g"),
        ("Active Dry Yeast", "g"),
        ("Instant Yeast", "g"),
        ("Panko Breadcrumbs", "g"),
        ("Italian Breadcrumbs", "g"),
        ("Rolled Oats", "g"),
        ("Steel-Cut Oats", "g"),
        ("Old-Fashioned Oats", "g"),
        ("Cocoa Powder", "g"),
        ("Chocolate Chips Dark", "g"),
        ("Chocolate Chips Milk", "g"),
        ("Peanut Butter Creamy", "g"),
        ("Peanut Butter Crunchy", "g"),
        ("Almond Butter", "g"),
        ("Cashew Butter", "g"),
        ("Tahini", "g"),
        ("Sunflower Seed Butter", "g"),
        ("Maple Syrup", "ml"),
        ("Honey", "ml"),
        ("Molasses", "ml"),
        ("Agave Syrup", "ml"),
        ("Vanilla Extract", "ml"),
        ("Chia Seeds", "g"),
        ("Flax Seeds", "g"),
        ("Pumpkin Seeds", "g"),
        ("Walnuts", "g"),
        ("Almonds", "g"),
        ("Pecans", "g"),
        ("Hazelnuts", "g"),
        ("Macadamia Nuts", "g"),
        ("Pistachios", "g"),
    ],
    "Grains & Pasta": [
        ("Spaghetti Pasta", "g"),
        ("Penne Pasta", "g"),
        ("Rigatoni Pasta", "g"),
        ("Fusilli Pasta", "g"),
        ("Farfalle Pasta", "g"),
        ("Orzo Pasta", "g"),
        ("Lasagna Sheets", "g"),
        ("Linguine Pasta", "g"),
        ("Angel Hair Pasta", "g"),
        ("Rice Basmati", "g"),
        ("Rice Jasmine", "g"),
        ("Rice Arborio", "g"),
        ("Brown Rice", "g"),
        ("Wild Rice Blend", "g"),
        ("Quinoa Tri-Color", "g"),
        ("Couscous Pearl", "g"),
        ("Bulgur Wheat", "g"),
        ("Farro", "g"),
        ("Barley Pearled", "g"),
        ("Polenta", "g"),
        ("Udon Noodles", "g"),
        ("Soba Noodles", "g"),
        ("Rice Vermicelli", "g"),
        ("Ramen Noodles", "g"),
        ("Tortillas Flour", "pcs"),
        ("Tortillas Corn", "pcs"),
        ("Pita Bread", "pcs"),
        ("Naan Bread", "pcs"),
        ("Sourdough Bread", "pcs"),
    ],
    "Spices & Herbs": [
        ("Kosher Salt", "g"),
        ("Sea Salt Flakes", "g"),
        ("Black Peppercorns", "g"),
        ("Ground Black Pepper", "g"),
        ("White Pepper", "g"),
        ("Smoked Paprika", "g"),
        ("Sweet Paprika", "g"),
        ("Ground Cumin", "g"),
        ("Ground Coriander", "g"),
        ("Turmeric Powder", "g"),
        ("Curry Powder", "g"),
        ("Chili Powder", "g"),
        ("Garam Masala", "g"),
        ("Italian Seasoning", "g"),
        ("Dried Basil", "g"),
        ("Dried Oregano", "g"),
        ("Dried Thyme", "g"),
        ("Dried Rosemary", "g"),
        ("Dried Sage", "g"),
        ("Crushed Red Pepper", "g"),
        ("Chinese Five Spice", "g"),
        ("Cayenne Pepper", "g"),
        ("Ground Ginger", "g"),
        ("Ground Cinnamon", "g"),
        ("Cinnamon Sticks", "g"),
        ("Ground Nutmeg", "g"),
        ("Ground Cloves", "g"),
        ("Cardamom Pods", "g"),
        ("Bay Leaves", "g"),
        ("Ground Allspice", "g"),
        ("Sesame Seeds", "g"),
    ],
    "Canned & Jarred": [
        ("Crushed Tomatoes", "g"),
        ("Diced Tomatoes", "g"),
        ("Tomato Sauce", "ml"),
        ("Tomato Paste", "g"),
        ("Fire Roasted Tomatoes", "g"),
        ("Coconut Milk", "ml"),
        ("Light Coconut Milk", "ml"),
        ("Evaporated Milk", "ml"),
        ("Sweetened Condensed Milk", "ml"),
        ("Pumpkin Puree", "g"),
        ("Black Beans Canned", "g"),
        ("Kidney Beans Canned", "g"),
        ("Chickpeas Canned", "g"),
        ("Cannellini Beans Canned", "g"),
        ("Corn Kernels", "g"),
        ("Green Peas Canned", "g"),
        ("Artichoke Hearts", "g"),
        ("Hearts of Palm", "g"),
        ("Roasted Red Peppers", "g"),
        ("Olives Kalamata", "g"),
        ("Olives Castelvetrano", "g"),
        ("Pickled Jalapenos", "g"),
        ("Salsa Verde Jar", "ml"),
        ("Marinara Sauce", "ml"),
        ("Arrabbiata Sauce", "ml"),
        ("Pesto Sauce", "g"),
        ("Sun-Dried Tomatoes", "g"),
        ("Capers", "g"),
        ("Anchovy Fillets", "g"),
        ("Chicken Broth", "ml"),
        ("Vegetable Broth", "ml"),
        ("Beef Broth", "ml"),
    ],
    "Frozen": [
        ("Frozen Peas", "g"),
        ("Frozen Corn", "g"),
        ("Frozen Spinach", "g"),
        ("Frozen Broccoli", "g"),
        ("Frozen Cauliflower Rice", "g"),
        ("Frozen Mixed Berries", "g"),
        ("Frozen Mango Chunks", "g"),
        ("Frozen Pineapple", "g"),
        ("Frozen Strawberries", "g"),
        ("Frozen Blueberries", "g"),
        ("Frozen Waffles", "pcs"),
        ("Frozen Fries", "g"),
        ("Frozen Edamame", "g"),
        ("Frozen Meatballs", "g"),
        ("Frozen Chicken Nuggets", "g"),
        ("Frozen Pizza Dough", "g"),
        ("Frozen Puff Pastry", "g"),
        ("Frozen Pie Crust", "g"),
        ("Frozen Shrimp", "g"),
        ("Frozen Fish Sticks", "g"),
    ],
    "Condiments & Oils": [
        ("Extra Virgin Olive Oil", "ml"),
        ("Avocado Oil", "ml"),
        ("Canola Oil", "ml"),
        ("Sesame Oil", "ml"),
        ("Vegetable Oil", "ml"),
        ("Grapeseed Oil", "ml"),
        ("Balsamic Vinegar", "ml"),
        ("Apple Cider Vinegar", "ml"),
        ("Rice Vinegar", "ml"),
        ("Red Wine Vinegar", "ml"),
        ("White Wine Vinegar", "ml"),
        ("Soy Sauce", "ml"),
        ("Tamari Sauce", "ml"),
        ("Fish Sauce", "ml"),
        ("Worcestershire Sauce", "ml"),
        ("Dijon Mustard", "g"),
        ("Whole Grain Mustard", "g"),
        ("Ketchup", "g"),
        ("Mayonnaise", "g"),
        ("Sriracha", "g"),
        ("Barbecue Sauce", "g"),
        ("Hot Sauce", "g"),
        ("Hoisin Sauce", "g"),
        ("Teriyaki Sauce", "ml"),
        ("Mirin", "ml"),
        ("White Miso Paste", "g"),
        ("Harissa Paste", "g"),
        ("Chili Crisp", "g"),
        ("Pomegranate Molasses", "ml"),
        ("Tahini Sauce", "g"),
    ],
}


def flatten_ingredients() -> List[dict]:
    rows: List[dict] = []
    idx = 1
    for category, items in INGREDIENTS_BY_CATEGORY.items():
        for name, unit in items:
            rows.append(
                {
                    "id": idx,
                    "name": name,
                    "default_unit": unit,
                    "category": category,
                }
            )
            idx += 1
    return rows


INGREDIENTS = flatten_ingredients()


# Recipes --------------------------------------------------------------------
recipes_data = [
    {
        "name": "Classic Margherita Pizza",
        "description": "Chewy crust topped with garlicky marinara, mozzarella, and fresh basil.",
        "instructions": "Preheat oven to 250°C. Stretch dough, spread sauce, top with cheese and basil, bake 10 minutes until blistered.",
        "cuisine": "Italian",
        "favorite": True,
        "ingredients": [
            ("Frozen Pizza Dough", 350, "g", False),
            ("Marinara Sauce", 120, "ml", False),
            ("Mozzarella Cheese", 180, "g", False),
            ("Parmesan Cheese", 20, "g", False),
            ("Fresh Basil", 15, "g", False),
            ("Extra Virgin Olive Oil", 10, "ml", False),
            ("Garlic Bulb", 1, "pcs", True),
        ],
    },
    {
        "name": "Creamy Mushroom Risotto",
        "description": "Arborio rice slowly cooked with broth, white wine, and sautéed mushrooms.",
        "instructions": "Sauté mushrooms, toast rice with aromatics, ladle warm broth while stirring until creamy, finish with butter and cheese.",
        "cuisine": "Italian",
        "favorite": True,
        "ingredients": [
            ("Rice Arborio", 320, "g", False),
            ("Chicken Broth", 900, "ml", False),
            ("White Onion", 0.5, "pcs", False),
            ("Garlic Bulb", 2, "pcs", False),
            ("Cremini Mushroom", 200, "g", False),
            ("Shiitake Mushroom", 120, "g", False),
            ("Butter Unsalted", 40, "g", False),
            ("Parmesan Cheese", 40, "g", False),
            ("Extra Virgin Olive Oil", 15, "ml", False),
            ("White Wine Vinegar", 15, "ml", True),
            ("Fresh Parsley", 10, "g", True),
        ],
    },
    {
        "name": "Spicy Chickpea Stew",
        "description": "Hearty tomato-based stew with chickpeas, greens, and warming spices.",
        "instructions": "Bloom spices in oil, add aromatics, tomatoes, coconut milk, and chickpeas. Simmer 20 minutes, fold in greens.",
        "cuisine": "Middle Eastern",
        "favorite": False,
        "ingredients": [
            ("Chickpeas Canned", 480, "g", False),
            ("Crushed Tomatoes", 400, "g", False),
            ("Coconut Milk", 200, "ml", False),
            ("Red Onion", 0.5, "pcs", False),
            ("Garlic Bulb", 3, "pcs", False),
            ("Ginger Root", 20, "g", False),
            ("Smoked Paprika", 5, "g", False),
            ("Ground Cumin", 6, "g", False),
            ("Turmeric Powder", 4, "g", False),
            ("Baby Spinach", 100, "g", False),
            ("Fresh Cilantro", 10, "g", True),
            ("Lemon", 0.5, "pcs", True),
        ],
    },
    {
        "name": "Lemon Herb Roast Chicken",
        "description": "Bone-in chicken roasted with lemon, garlic, and rosemary over potatoes.",
        "instructions": "Marinate chicken with oil, lemon, garlic, and herbs. Roast atop potatoes until skin is crisp and meat juicy.",
        "cuisine": "Mediterranean",
        "favorite": True,
        "ingredients": [
            ("Chicken Thigh", 800, "g", False),
            ("Yukon Gold Potato", 4, "pcs", False),
            ("Garlic Bulb", 4, "pcs", False),
            ("Lemon", 1, "pcs", False),
            ("Fresh Rosemary", 5, "g", False),
            ("Fresh Thyme", 5, "g", False),
            ("Extra Virgin Olive Oil", 30, "ml", False),
            ("Kosher Salt", 6, "g", False),
            ("Ground Black Pepper", 4, "g", False),
        ],
    },
    {
        "name": "Veggie Stir Fry",
        "description": "Colorful vegetables seared hot and tossed with a ginger garlic sauce.",
        "instructions": "Stir fry vegetables in batches, whisk sauce with soy, ginger, and garlic, toss together and serve over rice.",
        "cuisine": "Asian",
        "favorite": False,
        "ingredients": [
            ("Broccoli Florets", 150, "g", False),
            ("Red Bell Pepper", 1, "pcs", False),
            ("Carrot", 1, "pcs", False),
            ("Sugar Snap Peas", 120, "g", False),
        ],
    },
    {
        "name": "Avocado Kale Salad",
        "description": "Massaged kale tossed with creamy avocado, crunchy seeds, and lemon mustard dressing.",
        "instructions": "Massage kale with lemon and oil, fold in vegetables, avocado, seeds, and drizzle honey mustard vinaigrette.",
        "cuisine": "American",
        "favorite": False,
        "ingredients": [
            ("Kale Leaves", 120, "g", False),
            ("Avocado", 1, "pcs", False),
            ("Cherry Tomato", 8, "pcs", False),
            ("English Cucumber", 0.5, "pcs", False),
            ("Pumpkin Seeds", 20, "g", False),
            ("Fresh Parsley", 8, "g", True),
            ("Extra Virgin Olive Oil", 20, "ml", False),
            ("Lemon", 0.5, "pcs", False),
            ("Dijon Mustard", 8, "g", False),
            ("Honey", 10, "ml", False),
        ],
    },
    {
        "name": "Weeknight Beef Tacos",
        "description": "Seasoned ground beef tucked into warm tortillas with crisp toppings.",
        "instructions": "Brown beef with spices and aromatics, warm tortillas, assemble with toppings and serve immediately.",
        "cuisine": "Mexican",
        "favorite": True,
        "ingredients": [
            ("Ground Beef 80-20", 450, "g", False),
            ("Yellow Onion", 0.5, "pcs", False),
            ("Garlic Bulb", 3, "pcs", False),
            ("Chili Powder", 8, "g", False),
            ("Ground Cumin", 6, "g", False),
            ("Smoked Paprika", 4, "g", False),
            ("Tortillas Corn", 8, "pcs", False),
            ("Cheddar Cheese", 100, "g", False),
            ("Romaine Lettuce", 0.25, "pcs", True),
            ("Salsa Verde Jar", 60, "ml", False),
            ("Sour Cream", 60, "g", True),
            ("Lime", 1, "pcs", True),
        ],
    },
    {
        "name": "Thai Coconut Veggie Curry",
        "description": "Velvety coconut curry loaded with chicken, colorful vegetables, and herbs.",
        "instructions": "Sauté aromatics, add curry spices, simmer coconut milk with vegetables and chicken until tender, finish with lime.",
        "cuisine": "Thai",
        "favorite": False,
        "ingredients": [
            ("Chicken Breast", 400, "g", False),
            ("Red Bell Pepper", 1, "pcs", False),
            ("Carrot", 1, "pcs", False),
            ("Broccoli Florets", 120, "g", False),
            ("Coconut Milk", 400, "ml", False),
            ("Red Onion", 0.5, "pcs", False),
            ("Garlic Bulb", 3, "pcs", False),
            ("Ginger Root", 15, "g", False),
            ("Curry Powder", 8, "g", False),
            ("Fish Sauce", 10, "ml", False),
            ("Lime", 1, "pcs", False),
            ("Fresh Cilantro", 10, "g", True),
            ("Rice Jasmine", 200, "g", False),
        ],
    },
    {
        "name": "Garlic Butter Shrimp Pasta",
        "description": "Tender spaghetti coated in garlicky butter sauce with juicy shrimp.",
        "instructions": "Cook pasta, sear shrimp with butter and garlic, toss together with lemon juice and parsley.",
        "cuisine": "Italian",
        "favorite": True,
        "ingredients": [
            ("Spaghetti Pasta", 300, "g", False),
            ("Shrimp Large", 300, "g", False),
            ("Butter Unsalted", 60, "g", False),
            ("Garlic Bulb", 4, "pcs", False),
            ("Lemon", 1, "pcs", False),
            ("Fresh Parsley", 12, "g", False),
            ("Parmesan Cheese", 30, "g", False),
            ("Crushed Red Pepper", 2, "g", True),
        ],
    },
    {
        "name": "Quinoa Buddha Bowl",
        "description": "Roasted vegetables, crispy chickpeas, and greens over fluffy quinoa.",
        "instructions": "Roast sweet potatoes and broccoli, crisp chickpeas, assemble bowl with quinoa, greens, and tahini drizzle.",
        "cuisine": "Fusion",
        "favorite": False,
        "ingredients": [
            ("Quinoa Tri-Color", 200, "g", False),
            ("Chickpeas Canned", 240, "g", False),
            ("Sweet Potato", 1, "pcs", False),
            ("Broccoli Florets", 120, "g", False),
            ("Baby Spinach", 80, "g", False),
            ("Avocado", 1, "pcs", False),
            ("Tahini Sauce", 40, "g", False),
            ("Lemon", 0.5, "pcs", False),
            ("Smoked Paprika", 3, "g", True),
        ],
    },
    {
        "name": "Banana Oat Pancakes",
        "description": "Naturally sweet pancakes blended from oats, banana, and almond milk.",
        "instructions": "Blend batter until smooth, cook on greased skillet until golden, serve with maple syrup.",
        "cuisine": "Breakfast",
        "favorite": False,
        "ingredients": [
            ("Banana", 2, "pcs", False),
            ("Rolled Oats", 140, "g", False),
            ("Almond Milk", 240, "ml", False),
            ("Large Eggs", 2, "pcs", False),
            ("Baking Powder", 6, "g", False),
            ("Maple Syrup", 40, "ml", True),
            ("Vanilla Extract", 5, "ml", False),
            ("Cinnamon Sticks", 2, "g", True),
        ],
    },
    {
        "name": "Caprese Pasta Salad",
        "description": "Chilled fusilli with tomatoes, mozzarella, basil, and balsamic glaze.",
        "instructions": "Cook pasta al dente, toss with tomatoes, cheese, greens, and vinaigrette, chill before serving.",
        "cuisine": "Italian",
        "favorite": False,
        "ingredients": [
            ("Fusilli Pasta", 250, "g", False),
            ("Cherry Tomato", 12, "pcs", False),
            ("Mozzarella Cheese", 150, "g", False),
            ("Fresh Basil", 15, "g", False),
            ("Baby Spinach", 50, "g", True),
            ("Extra Virgin Olive Oil", 30, "ml", False),
            ("Balsamic Vinegar", 15, "ml", False),
            ("Kosher Salt", 4, "g", False),
        ],
    },
    {
        "name": "Mediterranean Farro Bowl",
        "description": "Nutty farro tossed with crunchy vegetables, feta, and lemon dressing.",
        "instructions": "Simmer farro until tender, fold in chopped vegetables and vinaigrette, top with feta.",
        "cuisine": "Mediterranean",
        "favorite": False,
        "ingredients": [
            ("Farro", 220, "g", False),
            ("English Cucumber", 0.5, "pcs", False),
            ("Cherry Tomato", 10, "pcs", False),
            ("Olives Kalamata", 60, "g", False),
            ("Feta Cheese", 80, "g", False),
            ("Red Onion", 0.25, "pcs", False),
            ("Fresh Parsley", 10, "g", False),
            ("Lemon", 0.5, "pcs", False),
            ("Extra Virgin Olive Oil", 25, "ml", False),
        ],
    },
    {
        "name": "Hearty Lentil Soup",
        "description": "Comforting bowl of lentils simmered with vegetables and herbs.",
        "instructions": "Sweat aromatics, add lentils and tomatoes, cover with broth and simmer until tender.",
        "cuisine": "Middle Eastern",
        "favorite": True,
        "ingredients": [
            ("Lentils Green", 220, "g", False),
            ("Carrot", 1, "pcs", False),
            ("Celery", 1, "pcs", False),
            ("Yellow Onion", 0.5, "pcs", False),
            ("Garlic Bulb", 3, "pcs", False),
            ("Crushed Tomatoes", 200, "g", False),
            ("Vegetable Broth", 900, "ml", False),
            ("Fresh Thyme", 5, "g", False),
            ("Bay Leaves", 2, "g", False),
            ("Kosher Salt", 5, "g", False),
            ("Extra Virgin Olive Oil", 20, "ml", False),
        ],
    },
    {
        "name": "Shakshuka",
        "description": "Eggs poached in spicy tomato pepper sauce.",
        "instructions": "Cook peppers with onions and spices, add tomatoes, simmer, crack eggs and bake until set.",
        "cuisine": "Middle Eastern",
        "favorite": True,
        "ingredients": [
            ("Diced Tomatoes", 400, "g", False),
            ("Red Bell Pepper", 1, "pcs", False),
            ("Yellow Onion", 0.5, "pcs", False),
            ("Garlic Bulb", 3, "pcs", False),
            ("Smoked Paprika", 6, "g", False),
            ("Ground Cumin", 5, "g", False),
            ("Cayenne Pepper", 2, "g", True),
            ("Extra Virgin Olive Oil", 20, "ml", False),
            ("Large Eggs", 4, "pcs", False),
            ("Fresh Cilantro", 8, "g", True),
        ],
    },
    {
        "name": "BBQ Pulled Chicken Sandwiches",
        "description": "Slow-simmered chicken mixed with tangy barbecue sauce on toasted bread.",
        "instructions": "Cook chicken with sauce and aromatics until shreddable, pile onto butter-toasted sourdough.",
        "cuisine": "American",
        "favorite": False,
        "ingredients": [
            ("Chicken Breast", 500, "g", False),
            ("Barbecue Sauce", 200, "g", False),
            ("Yellow Onion", 0.5, "pcs", False),
            ("Garlic Bulb", 3, "pcs", False),
            ("Brown Sugar", 20, "g", False),
            ("Apple Cider Vinegar", 20, "ml", False),
            ("Butter Salted", 20, "g", False),
            ("Sourdough Bread", 4, "pcs", False),
        ],
    },
    {
        "name": "Teriyaki Salmon Rice Bowl",
        "description": "Glazed salmon served over jasmine rice with broccoli and sesame.",
        "instructions": "Reduce teriyaki sauce, roast salmon, steam rice and broccoli, assemble with sesame garnish.",
        "cuisine": "Japanese",
        "favorite": True,
        "ingredients": [
            ("Salmon Fillet", 400, "g", False),
            ("Soy Sauce", 60, "ml", False),
            ("Honey", 30, "ml", False),
            ("Garlic Bulb", 2, "pcs", False),
            ("Ginger Root", 15, "g", False),
            ("Sesame Oil", 15, "ml", False),
            ("Rice Jasmine", 220, "g", False),
            ("Broccoli Florets", 150, "g", False),
            ("Sesame Seeds", 8, "g", False),
        ],
    },
    {
        "name": "Pesto Zoodle Bowl",
        "description": "Light zucchini noodles tossed with pesto and burst tomatoes.",
        "instructions": "Spiralize zucchini, quickly sauté, toss with pesto and warm tomatoes, garnish with basil.",
        "cuisine": "Italian",
        "favorite": False,
        "ingredients": [
            ("Zucchini", 2, "pcs", False),
            ("Pesto Sauce", 90, "g", False),
            ("Cherry Tomato", 10, "pcs", False),
            ("Parmesan Cheese", 25, "g", False),
            ("Fresh Basil", 10, "g", False),
            ("Extra Virgin Olive Oil", 15, "ml", False),
            ("Garlic Bulb", 2, "pcs", False),
        ],
    },
    {
        "name": "Garden Veggie Omelette",
        "description": "Fluffy omelette packed with spinach, peppers, mushrooms, and cheddar.",
        "instructions": "Sauté vegetables, whisk eggs with milk, cook gently, fold with cheese.",
        "cuisine": "Breakfast",
        "favorite": False,
        "ingredients": [
            ("Large Eggs", 3, "pcs", False),
            ("Whole Milk", 40, "ml", False),
            ("Baby Spinach", 40, "g", False),
            ("Cremini Mushroom", 80, "g", False),
            ("Red Bell Pepper", 0.5, "pcs", False),
            ("Cheddar Cheese", 60, "g", False),
            ("Green Onion", 1, "pcs", False),
            ("Butter Unsalted", 10, "g", False),
        ],
    },
    {
        "name": "Falafel Pita Wrap",
        "description": "Crispy baked falafel tucked into warm pita with tahini sauce.",
        "instructions": "Soak chickpeas, blend with herbs and aromatics, bake or fry, assemble wrap with veggies.",
        "cuisine": "Middle Eastern",
        "favorite": True,
        "ingredients": [
            ("Chickpeas Dried", 200, "g", False),
            ("Fresh Parsley", 15, "g", False),
            ("Fresh Cilantro", 15, "g", False),
            ("Garlic Bulb", 4, "pcs", False),
            ("Ground Cumin", 6, "g", False),
            ("Ground Coriander", 5, "g", False),
            ("Baking Powder", 4, "g", False),
            ("Tahini Sauce", 50, "g", False),
            ("Lemon", 1, "pcs", False),
            ("Pita Bread", 4, "pcs", False),
            ("Romaine Lettuce", 0.25, "pcs", True),
        ],
    },
    {
        "name": "Butternut Squash Bisque",
        "description": "Silky roasted squash soup finished with coconut milk and herbs.",
        "instructions": "Roast squash with aromatics, simmer with broth and coconut milk, blend until smooth.",
        "cuisine": "American",
        "favorite": False,
        "ingredients": [
            ("Butternut Squash", 1, "pcs", False),
            ("Carrot", 1, "pcs", False),
            ("Yellow Onion", 0.5, "pcs", False),
            ("Garlic Bulb", 3, "pcs", False),
            ("Vegetable Broth", 900, "ml", False),
            ("Coconut Milk", 200, "ml", False),
            ("Fresh Sage", 5, "g", False),
            ("Fresh Thyme", 4, "g", False),
            ("Extra Virgin Olive Oil", 20, "ml", False),
        ],
    },
    {
        "name": "Greek Yogurt Berry Parfait",
        "description": "Layered yogurt, berries, nuts, and honey for a quick breakfast.",
        "instructions": "Layer yogurt with thawed berries, drizzle honey, sprinkle nuts and seeds.",
        "cuisine": "Breakfast",
        "favorite": False,
        "ingredients": [
            ("Greek Yogurt", 200, "g", False),
            ("Honey", 20, "ml", False),
            ("Frozen Mixed Berries", 120, "g", False),
            ("Walnuts", 25, "g", False),
            ("Chia Seeds", 10, "g", False),
            ("Vanilla Extract", 4, "ml", True),
        ],
    },
    {
        "name": "Tofu Miso Ramen",
        "description": "Comforting ramen bowl with seared tofu, miso broth, and greens.",
        "instructions": "Simmer broth with aromatics and miso, cook noodles, sear tofu, assemble bowls with toppings.",
        "cuisine": "Japanese",
        "favorite": False,
        "ingredients": [
            ("Ramen Noodles", 2, "pcs", False),
            ("Tofu Firm", 300, "g", False),
            ("Vegetable Broth", 900, "ml", False),
            ("Soy Sauce", 40, "ml", False),
            ("White Miso Paste", 40, "g", False),
            ("Sesame Oil", 10, "ml", False),
            ("Garlic Bulb", 3, "pcs", False),
            ("Ginger Root", 15, "g", False),
            ("Baby Spinach", 60, "g", False),
            ("Green Onion", 2, "pcs", False),
            ("Sesame Seeds", 6, "g", False),
        ],
    },
    {
        "name": "Chewy Chocolate Chip Cookies",
        "description": "Bakery-style cookies with crisp edges and gooey centers.",
        "instructions": "Cream butter with sugars, fold in dry ingredients, chill dough, bake until golden.",
        "cuisine": "Dessert",
        "favorite": True,
        "ingredients": [
            ("All-Purpose Flour", 260, "g", False),
            ("Brown Sugar", 150, "g", False),
            ("White Sugar", 100, "g", False),
            ("Butter Unsalted", 150, "g", False),
            ("Large Eggs", 2, "pcs", False),
            ("Vanilla Extract", 10, "ml", False),
            ("Baking Soda", 6, "g", False),
            ("Chocolate Chips Dark", 200, "g", False),
            ("Kosher Salt", 4, "g", False),
        ],
    },
    {
        "name": "Overnight Blueberry Oats",
        "description": "No-cook oats soaked overnight with almond milk and blueberries.",
        "instructions": "Combine oats with milk, seeds, sweetener, rest overnight, top with fruit in morning.",
        "cuisine": "Breakfast",
        "favorite": False,
        "ingredients": [
            ("Rolled Oats", 90, "g", False),
            ("Almond Milk", 240, "ml", False),
            ("Chia Seeds", 12, "g", False),
            ("Maple Syrup", 20, "ml", False),
            ("Blueberries", 80, "g", False),
            ("Vanilla Extract", 4, "ml", True),
            ("Greek Yogurt", 60, "g", True),
        ],
    },
    {
        "name": "Stuffed Bell Peppers",
        "description": "Peppers filled with flavorful turkey, rice, beans, and cheese.",
        "instructions": "Par-bake peppers, cook filling with turkey and rice, stuff, top with cheese, bake until bubbly.",
        "cuisine": "American",
        "favorite": False,
        "ingredients": [
            ("Red Bell Pepper", 4, "pcs", False),
            ("Ground Turkey", 400, "g", False),
            ("Rice Basmati", 150, "g", False),
            ("Diced Tomatoes", 200, "g", False),
            ("Black Beans Canned", 200, "g", False),
            ("Corn Kernels", 100, "g", False),
            ("Yellow Onion", 0.5, "pcs", False),
            ("Garlic Bulb", 3, "pcs", False),
            ("Cheddar Cheese", 120, "g", False),
            ("Ground Cumin", 5, "g", False),
            ("Smoked Paprika", 4, "g", False),
        ],
    },
    {
        "name": "Eggplant Parmesan Bake",
        "description": "Layered breaded eggplant with marinara, basil, and melted cheese.",
        "instructions": "Bread eggplant slices, fry or bake, layer with sauce and cheese, bake until bubbling.",
        "cuisine": "Italian",
        "favorite": True,
        "ingredients": [
            ("Eggplant", 2, "pcs", False),
            ("All-Purpose Flour", 80, "g", False),
            ("Large Eggs", 2, "pcs", False),
            ("Panko Breadcrumbs", 120, "g", False),
            ("Marinara Sauce", 300, "ml", False),
            ("Mozzarella Cheese", 200, "g", False),
            ("Parmesan Cheese", 60, "g", False),
            ("Extra Virgin Olive Oil", 40, "ml", False),
            ("Fresh Basil", 12, "g", False),
        ],
    },
    {
        "name": "Baja Shrimp Tacos",
        "description": "Spiced shrimp with crunchy slaw, avocado, and creamy sauce.",
        "instructions": "Season and sear shrimp, build tacos with slaw, avocado, crema, and pickled jalapeños.",
        "cuisine": "Mexican",
        "favorite": True,
        "ingredients": [
            ("Shrimp Large", 320, "g", False),
            ("Chili Powder", 6, "g", False),
            ("Smoked Paprika", 4, "g", False),
            ("Garlic Bulb", 2, "pcs", False),
            ("Lime", 1, "pcs", False),
            ("Tortillas Corn", 8, "pcs", False),
            ("Red Cabbage", 0.5, "pcs", False),
            ("Avocado", 1, "pcs", False),
            ("Sour Cream", 80, "g", False),
            ("Pickled Jalapenos", 20, "g", True),
        ],
    }
]


random.seed(42)
NOW = dt.datetime.now()

INGREDIENT_LOOKUP = {row["name"]: row for row in INGREDIENTS}
PERISHABLE_CATEGORIES = {"Produce", "Dairy & Eggs", "Proteins"}


def iso(ts: dt.datetime) -> str:
    return ts.strftime("%Y-%m-%d %H:%M:%S")


def iso_date(ts: dt.datetime) -> str:
    return ts.strftime("%Y-%m-%d")


def format_number(value: float) -> str:
    text = f"{value:.4f}".rstrip("0").rstrip(".")
    return text or "0"


def format_sql_value(value):
    if value is None:
        return "NULL"
    if isinstance(value, bool):
        return "1" if value else "0"
    if isinstance(value, (int,)):
        return str(value)
    if isinstance(value, float):
        return format_number(value)
    escaped = str(value).replace("'", "''")
    return f"'{escaped}'"


def build_insert(table: str, columns: List[str], rows: List[dict]) -> List[str]:
    if not rows:
        return []
    lines = [f"INSERT INTO {table} ({', '.join(columns)}) VALUES"]
    value_lines = []
    for row in rows:
        values = ", ".join(format_sql_value(row[col]) for col in columns)
        value_lines.append(f"    ({values})")
    lines.append(",\n".join(value_lines) + ";")
    return lines


def choose_quantity(unit: str) -> float:
    if unit == "pcs":
        return random.randint(1, 12)
    if unit == "ml":
        return round(random.uniform(100, 1500), 1)
    return round(random.uniform(50, 1200), 1)


def generate_inventory_rows(count: int = 95) -> List[dict]:
    sample = random.sample(INGREDIENTS, count)
    rows = []
    for item in sample:
        expires = (
            iso_date(NOW + dt.timedelta(days=random.randint(2, 30)))
            if item["category"] in PERISHABLE_CATEGORIES
            else None
        )
        rows.append(
            {
                "ingredient_id": item["id"],
                "quantity": choose_quantity(item["default_unit"]),
                "unit": item["default_unit"],
                "expires_at": expires,
                "updated_at": iso(NOW - dt.timedelta(days=random.randint(0, 7))),
            }
        )
    return rows


def generate_shopping_rows(count: int = 28) -> List[dict]:
    sample = random.sample(INGREDIENTS, count)
    statuses = ["pending", "pending", "pending", "bought", "skipped"]
    notes_pool = [
        "Organic preferred",
        "Check for discounts",
        "Buy ripe but firm",
        "Substitute if unavailable",
        "Large size if possible",
    ]
    rows = []
    for idx, item in enumerate(sample, start=1):
        note = random.choice(notes_pool) if random.random() < 0.5 else None
        rows.append(
            {
                "id": idx,
                "ingredient_id": item["id"],
                "quantity": choose_quantity(item["default_unit"]),
                "unit": item["default_unit"],
                "status": random.choice(statuses),
                "notes": note,
                "created_at": iso(NOW - dt.timedelta(days=random.randint(0, 7))),
            }
        )
    return rows


def generate_recipe_rows() -> tuple[List[dict], List[dict]]:
    recipe_rows: List[dict] = []
    link_rows: List[dict] = []
    for idx, recipe in enumerate(recipes_data, start=1):
        recipe_rows.append(
            {
                "id": idx,
                "name": recipe["name"],
                "description": recipe["description"],
                "instructions": recipe["instructions"],
                "cuisine": recipe["cuisine"],
                "created_at": iso(NOW - dt.timedelta(days=random.randint(20, 200))),
                "favorite": 1 if recipe["favorite"] else 0,
            }
        )
        for ingredient_name, quantity, unit, optional in recipe["ingredients"]:
            try:
                ingredient_id = INGREDIENT_LOOKUP[ingredient_name]["id"]
            except KeyError as exc:
                raise KeyError(f"Unknown ingredient '{ingredient_name}' in recipe {recipe['name']}") from exc
            link_rows.append(
                {
                    "recipe_id": idx,
                    "ingredient_id": ingredient_id,
                    "quantity": quantity,
                    "unit": unit,
                    "optional": 1 if optional else 0,
                }
            )
    return recipe_rows, link_rows


def generate_meal_plans(recipe_ids: List[int], count: int = 10) -> List[dict]:
    rows = []
    for idx in range(1, count + 1):
        rows.append(
            {
                "id": idx,
                "recipe_id": random.choice(recipe_ids),
                "scheduled_for": iso(NOW + dt.timedelta(days=random.randint(1, 14))),
                "servings": random.randint(2, 6),
            }
        )
    return rows


def generate_cook_history(recipe_ids: List[int], count: int = 14) -> List[dict]:
    comments = [
        "Family favorite",
        "Add more spice next time",
        "Double batch worked great",
        "Kids loved it",
        "Serve with salad",
        "Try whole wheat pasta next time",
    ]
    rows = []
    for idx in range(1, count + 1):
        rows.append(
            {
                "id": idx,
                "recipe_id": random.choice(recipe_ids),
                "cooked_at": iso(NOW - dt.timedelta(days=random.randint(1, 45))),
                "notes": random.choice(comments),
            }
        )
    return rows


def write_sql():
    inventory_rows = generate_inventory_rows()
    shopping_rows = generate_shopping_rows()
    recipe_rows, recipe_ingredients = generate_recipe_rows()
    recipe_ids = [row["id"] for row in recipe_rows]
    meal_plan_rows = generate_meal_plans(recipe_ids)
    cook_history_rows = generate_cook_history(recipe_ids)

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    lines: List[str] = []
    lines.append("-- Auto-generated seed data for Moonyam pantry app")
    lines.append(f"-- Generated on {iso(NOW)}")
    lines.append("PRAGMA foreign_keys = OFF;")
    lines.append("BEGIN TRANSACTION;")
    for table in [
        "CookHistory",
        "MealPlans",
        "RecipeIngredients",
        "Recipes",
        "ShoppingItems",
        "Inventory",
        "Ingredients",
    ]:
        lines.append(f"DELETE FROM {table};")
    lines.append("")

    lines.extend(build_insert("Ingredients", ["id", "name", "default_unit", "category"], INGREDIENTS))
    lines.append("")
    lines.extend(
        build_insert(
            "Inventory",
            ["ingredient_id", "quantity", "unit", "expires_at", "updated_at"],
            inventory_rows,
        )
    )
    lines.append("")
    lines.extend(
        build_insert(
            "ShoppingItems",
            ["id", "ingredient_id", "quantity", "unit", "status", "notes", "created_at"],
            shopping_rows,
        )
    )
    lines.append("")
    lines.extend(
        build_insert(
            "Recipes",
            ["id", "name", "description", "instructions", "cuisine", "created_at", "favorite"],
            recipe_rows,
        )
    )
    lines.append("")
    lines.extend(
        build_insert(
            "RecipeIngredients",
            ["recipe_id", "ingredient_id", "quantity", "unit", "optional"],
            recipe_ingredients,
        )
    )
    lines.append("")
    lines.extend(
        build_insert(
            "MealPlans",
            ["id", "recipe_id", "scheduled_for", "servings"],
            meal_plan_rows,
        )
    )
    lines.append("")
    lines.extend(
        build_insert(
            "CookHistory",
            ["id", "recipe_id", "cooked_at", "notes"],
            cook_history_rows,
        )
    )
    lines.append("COMMIT;")

    OUTPUT.write_text("\n".join(lines) + "\n")
    print(f"Wrote seed data with {len(INGREDIENTS)} ingredients, {len(recipe_rows)} recipes.")


def main():
    write_sql()


if __name__ == "__main__":
    main()
