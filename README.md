# Verdant 🌱

Verdant is a Django web application that allows users to manage and care for virtual plants. Each plant grows over time but requires attention from the user. Neglected plants may wilt or regress in growth. The app encourages daily interaction and gamifies plant care with growth stages, health tracking, and achievements.

---

## Features

1. **User Management**
   - Sign up, login, and logout.
   - Each user manages their own garden of plants.

2. **Plant CRUD**
   - Create, Read, Update, Delete plants.
   - Attributes:
     - Name
     - Species / Type (Cactus, Fern, Flower, etc.)
     - Growth Stage (Healthy → Unhealthy → Weak → Dying → Dead)
     - Health (0–100)
     - Last cared for (timestamp)
     - Accessories (optional)

3. **Care System**
   - Users perform actions: Watering, Fertilizing, Pruning, Sunlight Adjustment.
   - Care actions affect plant health:
     - Correct care increases health.
     - Incorrect care slightly decreases health.
   - Actions are timestamped and tracked in **CareAction** and **PlantActivity** models.

4. **Growth & Neglect**
   - Plant growth stages automatically update based on health.
   - Health decreases over time if plants are neglected.
   - Visual indicators show growth and health status.

5. **Accessories**
   - Attach accessories (pots, decorations, fertilizers) to plants.
   - Optional effects on health or growth speed.

6. **Dashboard**
   - Overview of the user’s garden.
   - Highlights plants that need attention.
   - Displays health, growth stage, accessories, and care history.

7. **Gamification**
   - Achievements for reaching full growth.
   - Badges for consistent care streaks.

---

## Tech Stack

- **Backend:** Django 5.x, Python 3.11  
- **Database:** PostgreSQL (production), SQLite (development)  
- **Frontend:** HTML5, CSS3, Django Templates  
- **Background Tasks:** Cron jobs for daily updates  
- **Version Control:** Git, GitHub  
- **Development Tools:** VSCode, Python virtual environment  

---

## Project Structure
- Current Structure
```
Verdant
 ┣ my_app
 ┃ ┣ static
 ┃ ┃ ┣ css
 ┃ ┃ ┃ ┣ accessories
 ┃ ┃ ┃ ┃ ┣ accessory-detail.css
 ┃ ┃ ┃ ┃ ┗ accessory-list.css
 ┃ ┃ ┃ ┣ careactions
 ┃ ┃ ┃ ┃ ┗ careaction-list.css
 ┃ ┃ ┃ ┣ plants
 ┃ ┃ ┃ ┃ ┣ plant-list.css
 ┃ ┃ ┃ ┃ ┗ plant-detail.css
 ┃ ┃ ┃ ┣ home.css
 ┃ ┃ ┃ ┣ form.css
 ┃ ┃ ┃ ┣ about.css
 ┃ ┃ ┃ ┗ base.css
 ┃ ┃ ┗ images
 ┃ ┃ ┃ ┣ plants
 ┃ ┃ ┃ ┃ ┣ dead.png
 ┃ ┃ ┃ ┃ ┣ healthy.png
 ┃ ┃ ┃ ┃ ┣ unhealthy.png
 ┃ ┃ ┃ ┃ ┣ weak.png
 ┃ ┃ ┃ ┃ ┣ wilting.png
 ┃ ┃ ┃ ┗ logo2.png
 ┃ ┣ migrations
 ┃ ┃ ┣ __init__.py
 ┃ ┃ ┗ 0001_initial.py
 ┃ ┣ management
 ┃ ┃ ┗ commands
 ┃ ┃ ┃ ┗ update_plants.py
 ┃ ┣ templates
 ┃ ┃ ┣ my_app
 ┃ ┃ ┃ ┣ accessories
 ┃ ┃ ┃ ┃ ┣ accessory_list.html
 ┃ ┃ ┃ ┃ ┣ accessory_form.html
 ┃ ┃ ┃ ┃ ┣ accessory_detail.html
 ┃ ┃ ┃ ┃ ┗ accessory_confirm_delete.html
 ┃ ┃ ┃ ┣ careactions
 ┃ ┃ ┃ ┃ ┣ careaction_list.html
 ┃ ┃ ┃ ┃ ┗ careaction_form.html
 ┃ ┃ ┃ ┗ plants
 ┃ ┃ ┃ ┃ ┣ plant_confirm_delete.html
 ┃ ┃ ┃ ┃ ┣ plant_form.html
 ┃ ┃ ┃ ┃ ┣ plant_list.html
 ┃ ┃ ┃ ┃ ┗ plant-detail.html
 ┃ ┃ ┣ home.html
 ┃ ┃ ┣ signup.html
 ┃ ┃ ┣ base.html
 ┃ ┃ ┗ about.html
 ┃ ┣ views.py
 ┃ ┣ tests.py
 ┃ ┣ __init__.py
 ┃ ┣ urls.py
 ┃ ┣ admin.py
 ┃ ┣ models.py
 ┃ ┣ apps.py
 ┃ ┗ forms.py
 ┣ Verdant
 ┃ ┣ __init__.py
 ┃ ┣ asgi.py
 ┃ ┣ settings.py
 ┃ ┣ urls.py
 ┃ ┗ wsgi.py
 ┣ Pipfile.lock
 ┣ manage.py
 ┣ README.md
 ┣ Pipfile
 ┗ verdant
```
---
## Models and ERD

**Main Models:**

1. **User** (Django auth user)  
   - Fields: username, email, password, etc.  
   - Relationships: One-to-Many with Plant

2. **Plant**  
   - Fields: name, species, planting_date, description, growth_stage, health, last_cared_for  
   - Relationships:
     - Many-to-One: User → Plant  
     - Many-to-Many: Plant ↔ Accessory  
     - One-to-Many: Plant → CareAction  
     - One-to-Many: Plant → PlantActivity

3. **Accessory**  
   - Fields: name, type, description  
   - Relationships: Many-to-Many with Plant

4. **CareAction**  
   - Fields: action_type, date, notes  
   - Relationships: Many-to-One with Plant

5. **PlantActivity**  
   - Fields: message, timestamp  
   - Relationships: Many-to-One with Plant

---

- **Relationships**
  - `User` → `Plant` : One-to-Many (a user can have many plants)
  - `Plant` → `Accessory` : Many-to-Many (plants can have multiple accessories)
  - `Plant` → `CareAction` : One-to-Many (each care action is recorded for a plant)
  - `Plant` → `PlantActivity` : One-to-Many (logs activity messages for a plant)


**ERD Diagram (Conceptual)**
```
User 1 ────< Plant >─────< Accessory
              │
              ├──< CareAction
              │
              └──< PlantActivity


``` 
```
+----------------+        +----------------+        +----------------+
|     User       |        |     Plant      |        |   Accessory    |
+----------------+        +----------------+        +----------------+
| id (PK)        |<------>| id (PK)        |<------>| id (PK)        |
| username       |        | name           |        | name           |
| email          |        | species        |        | type           |
| password       |        | description    |        | description    |        
+----------------+        | planting_date  |        +----------------+
                          | growth_stage   |
                          | health         |
                          | last_cared_for |
                          | owner (FK)     |
                          +----------------+
                                 ^
          +----------------------+-------------------+
          |                      |                   |
+----------------+       +----------------+    +------------------+
|  CareAction    |       | PlantActivity  |    | Many-to-Many     |
+----------------+       +----------------+    | Plant ↔ Accessory|
| id (PK)        |       | id (PK)        |    +------------------+
| plant (FK)     |       | plant (FK)     |
| action_type    |       | message        |
| date           |       | timestamp      |
| notes          |       +----------------+
+----------------+


```
## Deployment

[![VERDANT](/my_app/static/images/logo2.png)](https://verdant-t4w3.onrender.com/)
https://verdant-t4w3.onrender.com/



To run Verdant on your local machine, follow these steps:

1. **Clone the repository**
```bash
git clone https://github.com/your-username/verdant.git
cd verdant

pipenv shell
pipenv install django
pipenv install psycopg2-binary
pipenv install django-crontab

CREATE DATABASE verdant;

python manage.py makemigrations
python manage.py migrate

python manage.py runserver

python manage.py crontab add
```
---

## Conclusion

Verdant is designed to combine productivity, education, and fun by allowing users to nurture virtual plants while learning about plant care. With a robust CRUD system, a growth and neglect simulation, and gamification elements such as achievements and badges, Verdant encourages daily interaction and engagement. Its modular Django architecture, clean project structure, and scalable backend make it easy to extend and maintain. Whether used as a personal gardening companion or a learning tool, Verdant provides an engaging and rewarding experience for all plant enthusiasts.


Thanks for checking out this project!
