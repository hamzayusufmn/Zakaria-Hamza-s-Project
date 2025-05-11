# Mediterranean Delights  
_(Zakaria-Hamza-s-Project)_

This is our capstone project—a simple Mediterranean restaurant website where users can:
- Browse the menu
- Place an order ahead
- Check hours
- Leave feedback

Built with Flask, HTML/CSS, and SQLite. (4/21/2025)

---

## Quick start

1. **Clone the repo**  
   ```bash
   git clone https://github.com/hamzayusufmn/Zakaria-Hamza-s-Project.git
   cd Zakaria-Hamza-s-Project

2. create a virtual environment  and add this to terminal

python -m venv venv
source venv/bin/activate  or   # on Windows: venv\Scripts\activate

3. install requirments 

pip install -r requirements.txt

4. run the app

flask run.

file setup
templates/
All the HTML pages: home, menu, cart, gallery, feedback, contact, about
static/
css/styles.css (custom styles)
menu/ (food images)
routes/
Blueprints for main, menu, admin, and order flows
models/
SQLAlchemy models for hours, menu items, orders
config.py & extensions.py
App settings and database setup
seed_data.py



 
