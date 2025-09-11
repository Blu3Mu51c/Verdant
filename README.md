# Florafy 🌱

Florafy is a Django web application that allows users to manage and care for virtual plants. Each plant grows over time, but requires attention from the user. Neglected plants may wilt or regress in growth. The app encourages daily interaction and gamifies plant care with growth stages, health tracking, and achievements.

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
     - Growth Stage (Seedling → Juvenile → Mature → Flowering)
     - Health (0–100)
     - Last cared for (timestamp)
     - Optional: water level, sunlight, nutrients

3. **Growth System**
   - Plants grow over time if properly cared for.
   - Requirements for growth:
     - Water
     - Sunlight
     - Fertilizer
   - Actions are recorded with timestamps.
   - Plants advance to next growth stage only if requirements are met.
   - Visual indicators for growth and health.

4. **Neglect System**
   - If a plant is not tended for 1 week:
     - Health decreases gradually.
     - Growth may stagnate or regress.
     - Plant may wilt (visual change).
   - Cron jobs / background tasks automatically update plant health and growth status daily.

5. **Dashboard**
   - User’s garden overview showing all plants.
   - Highlights plants that need attention.
   - Displays health, growth stage, and care history.

6. **Gamification**
   - Achievements for reaching full growth.
   - Badges for streaks of consistent care.
   - Optional leveling system for plants.

7. **Accessories (Optional)**
   - Users can attach accessories to plants (pots, decorations, fertilizers).
   - Accessories have optional effects (bonus health or growth speed).



## Tech Stack

- **Backend:**  
  - **Django 5.x** – Main web framework handling routing, views, models, forms, authentication, and CRUD functionality.  
  - **Python 3.11** – Programming language for all backend logic, including plant growth simulation and accessory management.

- **Database:**  
  - **PostgreSQL** – For production for scalability and advanced querying capabilities.
  - **SQLite** – Lightweight, easy to set up for development and testing.  

- **Frontend:**  
  - **HTML5 & CSS3** – Structure and styling for pages, responsive layouts, and component styling.  
  - **Django Templates** – Dynamic rendering of data with template inheritance, loops, and conditionals.  

- **Styling:**  
  - **CSS:** Stylesheet language used to describe the presentation of a document written in HTML.
  - **Images & Icons:** Stored in `/static/images/` for plant icons, accessories, and UI enhancements.

- **Background Tasks / Scheduling:**  
  - **Cron Jobs** – Automatically update plant growth and reminders if plants haven’t been tended.  

- **Version Control & Collaboration:**  
  - **Git** – Local version control.  
  - **GitHub** – Remote repository for collaboration, backup, and version tracking.

- **Development Tools & Environment:**  
  - **Python Virtual Environment (pipenv)** – Isolated project dependencies.  
  - **IDE / Editor:** VSCode for Django development.  
---

## Project Structure
- Current Structure
```
my_app/
florafy/
 ┣ my_app/
 ┃ ┣ static/
 ┃ ┃ ┗ css/
 ┃ ┃   ┣ base.css
 ┃ ┃   ┣ home.css
 ┃ ┃   ┣ form.css
 ┃ ┃   ┣ plants/
 ┃ ┃   ┃ ┣ plant-index.css
 ┃ ┃   ┃ ┗ plant-detail.css
 ┃ ┃   ┣ accessories/
 ┃ ┃   ┃ ┣ accessory-index.css
 ┃ ┃   ┃ ┗ accessory-detail.css
 ┃ ┗ templates/
 ┃     ┗ my_app/
 ┃       ┣ base.html
 ┃       ┣ home.html
 ┃       ┣ signup.html
 ┃       ┣ login.html
 ┃       ┣ about.html
 ┃       ┣ plants/
 ┃       ┃ ┣ plant_list.html
 ┃       ┃ ┣ plant_form.html
 ┃       ┃ ┣ plant_detail.html
 ┃       ┣ accessories/
 ┃       ┃ ┣ accessory_list.html
 ┃       ┃ ┣ accessory_form.html
 ┃       ┃ ┣ accessory_detail.html
 ┃       ┃ ┗ accessory_confirm_delete.html
 ┃       ┣ users/
 ┃       ┃ ┣ user_profile.html
 ┃       ┃ ┣ user_edit.html
 ┃       ┣ shared/
 ┃       ┃ ┣ navbar.html
 ┃       ┃ ┗ footer.html
 ┃ ┣ models.py
 ┃ ┣ views.py
 ┃ ┣ forms.py
 ┃ ┣ urls.py
 ┃ ┗ admin.py
 ┣ manage.py
 ┣ requirements.txt
 ┣ README.md
 ┗ .gitignore

```
---
## Models and ERD
Florafy has the following main models:

1. **User** (built-in Django auth user)  
   - Fields: username, email, password, etc.  
   - Relationship: One-to-Many with Plant

2. **Plant**  
   - Fields: name, species, planting_date, description, growth_stage  
   - Relationships:  
     - Many-to-One: User → Plant  
     - Many-to-Many: Plant ↔ Accessory  
     - One-to-Many: Plant → CareAction

3. **Accessory**  
   - Fields: name, type, description
   - Relationships: Many-to-Many with Plant

4. **CareAction**
   - Fields: date, action_type (watering, fertilizing, pruning), notes  
   - Relationships: Many-to-One with Plant

- **Relationships**
  - `User` → `Plant` : One-to-Many (a user can have many plants)
  - `Plant` → `Accessory` : Many-to-Many (plants can have multiple accessories)
  - `Plant` → `CareAction` : One-to-Many (each care action is recorded)

**ERD Diagram (Conceptual)**
```
User 1 ────< Plant >─────< Accessory
  │
  └───< CareAction >────── Plant

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
                          | owner (FK)     |
                          +----------------+
                                 ^
                                 |
                                 |
                          +----------------+
                          |  CareAction    |
                          +----------------+
                          | id (PK)        |
                          | plant (FK)     |
                          | action_type    |
                          | date           |
                          | notes          |
                          +----------------+

```
---


---

## Conclusion

Florafy is designed to combine productivity, education, and fun by allowing users to nurture virtual plants while learning about plant care. With a robust CRUD system, a growth and neglect simulation, and gamification elements such as achievements and badges, Florafy encourages daily interaction and engagement. Its modular Django architecture, clean project structure, and scalable backend make it easy to extend and maintain. Whether used as a personal gardening companion or a learning tool, Florafy provides an engaging and rewarding experience for all plant enthusiasts.


Thanks for checking out this project!
