# 🔐 Streamlit & SQLite3 Secure Authentication System

A lightweight, self-contained user authentication system built with **Python**, **Streamlit**, and **SQLite3**. It features tabbed navigation for user login and registration, SHA-256 password hashing, input validation, and a protected dashboard with session management.

---

## ✨ Features

* **Tabbed Authentication UI:** Clean separation between **Login** and **Sign Up** workflows using `st.tabs`.
* **SHA-256 Password Hashing:** Passwords are hashed using Python's `hashlib` before being stored in the database—plain-text passwords are never saved.
* **SQL Injection Protection:** All database operations use parameterized SQL queries (`?` placeholders).
* **Form Validation:** Built-in checks for empty fields, username length, valid email formatting, minimum password length, and password confirmation matching.
* **Session Management:** Uses `st.session_state` to persist login states across reruns and protect the user dashboard until logout.
* **Zero-Config Database:** Automatically initializes a local `users.db` SQLite file on the first run.

---

## 📁 Project Structure

```text
├── app.py              # Main Streamlit application & database logic
├── requirements.txt    # Python dependencies
├── users.db            # Auto-generated SQLite database (created on first run)
└── README.md           # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.8 or higher
* `pip` (Python package installer)

### Installation

1. **Clone or download the project files** into a local directory.
2. **Create and activate a virtual environment (recommended):**
   ```bash
   python -m venv venv

   # On Windows:
   venv\Scripts\activate

   # On macOS/Linux:
   source venv/bin/activate
   ```
3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🖥️ Usage

1. **Run the Streamlit application:**
   ```bash
   streamlit run app.py
   ```
2. **Open your browser:** Streamlit will automatically open the app at `http://localhost:8501`.
3. **Register & Log In:**
   * Switch to the **Sign Up** tab to create a new account (username, email, password, and confirm password).
   * Switch to the **Login** tab to sign in and access the protected dashboard.
   * Click **Logout** in the top right corner of the dashboard to end your session.

---

## 🗄️ Database Schema

On startup, `app.py` automatically creates the `users` table in `users.db`:

| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | `INTEGER` | `PRIMARY KEY AUTOINCREMENT` | Unique user identifier |
| `username` | `TEXT` | `UNIQUE NOT NULL` | User's chosen login name |
| `email` | `TEXT` | `UNIQUE NOT NULL` | User's email address |
| `password_hash` | `TEXT` | `NOT NULL` | SHA-256 hex digest of the password |
| `created_at` | `TIMESTAMP` | `DEFAULT CURRENT_TIMESTAMP` | Account creation timestamp |

---

## ⚠️ Production Security Note

This project uses **SHA-256** hashing for simplicity and zero external cryptographic dependencies. If you plan to deploy this application to a public production environment, consider upgrading to a salted, slow-hashing algorithm such as **`bcrypt`** or **`argon2-cffi`** to protect against brute-force and rainbow-table attacks.
