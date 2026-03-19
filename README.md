# 🏏 Cric-Analytics
**A Full-Stack Cricket Statistics & Live Scoring Platform**

[![Live Demo](https://img.shields.io/badge/demo-Live%20on%20Render-brightgreen)](https://cric-analytics.onrender.com)

## 📌 Project Overview
Cric-Analytics is a comprehensive web application designed for cricket enthusiasts and data analysts. It provides a deep dive into historical player statistics, the official Laws of Cricket, and real-time match scoring. The platform successfully manages a relational database of over **7,200 records**, migrated from legacy flat-file systems to a high-performance PostgreSQL production environment.

**🔗 Live Link:** [https://cric-analytics.onrender.com](https://cric-analytics.onrender.com)

---

## ✨ Key Features
* **Live Match Center:** Real-time updates for ongoing international and domestic cricket matches via external API integration.
* **Extensive Player Database:** Detailed statistics for over 7,000 players across Batting, Bowling, Fielding, and All-rounder categories.
* **Digital Law Book:** A searchable, categorized database of the official Laws of Cricket, including detailed subsections.
* **Player Comparison:** (Optional: if active) A dedicated tool to compare performance metrics between two players side-by-side.
* **Responsive Design:** Fully optimized for mobile, tablet, and desktop viewing.

---

## 🛠️ Technical Stack
* **Backend:** Python 3.x, Django 5.x
* **Database:** PostgreSQL (Production), SQLite (Development)
* **Frontend:** HTML5, CSS3 (Custom Styling), JavaScript
* **Deployment:** Render (Web Service + Managed PostgreSQL)
* **Static/Media Handling:** WhiteNoise (v6.x)
* **Data Migration:** Custom Python ETL scripts for JSON/CSV serialization and UTF-8 encoding verification.



---

## 🚀 Installation & Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/[Your-GitHub-Username]/cricket_site.git
   cd cricket_site
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add:
   ```env
   SECRET_KEY=your_django_secret_key
   DATABASE_URL=your_postgres_url
   CRICKET_API_KEY=your_live_score_api_key
   ```

5. **Run Migrations and Load Data:**
   ```bash
   python manage.py migrate
   python manage.py loaddata cricket_data.json
   ```

6. **Start the Server:**
   ```bash
   python manage.py runserver
   ```

---

## 📂 Project Structure
```text
├── cricket_site/          # Project configuration (settings, urls, wsgi)
├── stats/                 # Main application logic
│   ├── templates/         # HTML files (Player lists, Laws, Live Scores)
│   ├── models.py          # Database schema (Player, Law, Stats)
│   └── views.py           # Logic for data processing and API calls
├── static/                # CSS, JS, and global images (default.png)
├── media/                 # User-uploaded content (Player photos)
├── build.sh               # Deployment script for Render
├── cricket_data.json      # Master data fixture (7,000+ objects)
└── manage.py              # Django management utility
```

---

## 🛡️ Challenges Overcome
* **Data Collection:** Collected and Filtered Data From various different sources.
* **Data Migration:** Resolved complex encoding issues (UTF-8) and hidden character conflicts during the transfer of 7,000+ objects from SQLite to PostgreSQL.
* **Performance Optimization:** Implemented pagination and queryset slicing to handle large datasets on a cloud-hosted free tier.
* **Security:** Transitioned sensitive API credentials to environment variables to protect project integrity.

---

## 👤 Author
* **Pranav Shende** - *Initial Work & Deployment*
* GitHub: [@Pranav-Shende](https://github.com/Pranav-Shende/))
