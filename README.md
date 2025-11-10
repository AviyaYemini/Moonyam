```
Moonyam/                             // רוט של הפרויקט כולו
├─ build.gradle.kts                  // הגדרת Gradle: תלויות, טארגטים, קומפילציה
├─ settings.gradle.kts               // מזהה מודולים ושם הפרויקט עבור Gradle
├─ README.md                         // מסמך זה – מפה מהירה לעץ ולתפקידיו
├─ docs/                             // תיעוד ודאטה נלווית
│  ├─ db-schema.sql                  // DDL מלא עם הסברים לכל טבלה/אינדקס
│  └─ seed-data.sql                  // נתוני דוגמה שנוצרים ע"י הסקריפט
├─ scripts/                          // עזרי CLI
│  ├─ generate_seed_data.py          // מייצר את seed-data.sql (341 רכיבים, 28 מתכונים וכו')
│  └─ preview_db.sh                  // פקודה קצרה להצגת טבלאות ודוגמאות מה-DB
└─ src/
   ├─ Main.kt                        // קוד דוגמאי מה-proto; יוסר כש-App.kt יתפוס פיקוד
   ├─ main/
   │  ├─ kotlin/com/moonyam/         // קוד המקור הראשי בקוטלין
   │  │  ├─ App.kt                   // נקודת הכניסה: מאתחלת DB, רפוזיטריז ו-UI
   │  │  ├─ data/                    // גישה למסדי נתונים/מקורות נתונים
   │  │  │  ├─ InventoryRepository.kt// חוזה + מימוש CRUD על inventory/shopping וכו'
   │  │  │  └─ LocalDatabase.kt      // עטיפה על SQLite (DriverManager/DAO helpers)
   │  │  ├─ domain/                  // לוגיקה עסקית עצמאית ממסד הנתונים
   │  │  │  ├─ models/               // ישויות נקיות (Item, Recipe...) שמשותפות לכל השכבות
   │  │  │  └─ usecases/             // פעולות עסקיות (GetCookableRecipes, UpdateInventory…)
   │  │  └─ ui/                      // שכבת המצגת (Console/Compose + ניהול מצב)
   │  │     ├─ ConsoleMenu.kt        // CLI זמני שמפעיל UseCases דרך ViewModel
   │  │     └─ ViewModels.kt         // מחברים בין UI ללוגיקה, מחזיקים state
   │  └─ resources/
   │     └─ moonyam.db               // מסד SQLite מקומי עם הסכמה + seed
   └─ test/
      └─ kotlin/com/moonyam/
         └─ domain/                  // בדיקות יחידה ל-UseCases/Services
```
