# 📚 CS353 HW4 — Internship Application Portal

A web app where university students can apply for summer internships at different companies.  
Built using **Flask**, **MySQL**, and **Docker Compose** for CS353 — Spring 2025 Homework 4.

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/moinkhan30000/CS352-HW4_DB_Project.git
cd CS352-HW4_DB_Project
2. Build the Docker Images
bash
Copy
Edit
docker-compose build
3. Start the App
bash
Copy
Edit
docker-compose up
Then open your browser and go to:

👉 http://localhost:5000

📁 Folder Structure
bash
Copy
Edit
CS352-HW4_DB_Project/
├── app/
│   ├── app.py                # Flask app
│   ├── static/style.css      # CSS
│   └── templates/            # HTML pages (Jinja2)
├── schema.sql                # MySQL schema + sample data
├── requirements.txt          # Python dependencies
├── Dockerfile                # Flask app image build file
└── docker-compose.yaml       # Defines web + db stack
🔐 Login Instructions
Students use:

Username = their name (e.g., Ali)

Password = their student ID (e.g., S101)

Example:

text
Copy
Edit
Username: Ali
Password: S101
All credentials are listed in the preloaded schema.sql file.

🗄️ Database Summary
Tables

Table	Description
student	ID, name, birthdate, department, GPA
company	Internship info with quota & GPA rule
apply	Student applications (max 3 per student)
Sample Students

SID	Name	Dept	GPA
S101	Ali	CS	2.92
S102	Veli	EE	3.96
S103	Ayse	IE	3.30
🧠 Features
Student registration and login

Company listing with GPA filters

Internship applications (max 3)

Application cancellation

Summary page using raw SQL queries

MySQL seeding via schema.sql

Dockerized development and deployment

🛠️ Development Tips
Live Reload
Flask auto-reloads changes thanks to volume binding:

yaml
Copy
Edit
volumes:
  - ./app:/app
You can modify Python or HTML files and see changes immediately without restarting.

Detached Mode
Run in background:

bash
Copy
Edit
docker-compose up -d
Follow logs:

bash
Copy
Edit
docker-compose logs -f web
Stop everything:

bash
Copy
Edit
docker-compose down
❓ Troubleshooting
Reset DB if schema or data is wrong:

bash
Copy
Edit
docker-compose down -v
docker-compose up --build
Access MySQL manually:

bash
Copy
Edit
mysql -h 127.0.0.1 -P 3307 -u root -p
Password: password

✅ Status
This project meets all CS353 HW4 requirements:

 Registration & login

 Internship application (max 3)

 GPA & quota filtering

 SQL-only summary page

 Dockerized environment

 Seeded schema with data

📜 License
This project is open-source and available under the MIT License.
