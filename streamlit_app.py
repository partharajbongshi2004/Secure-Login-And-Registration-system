import hashlib
import re
import sqlite3
import streamlit as st

# --- DATABASE SETUP ---
DB_NAME = "users.db"


def init_db():
    """Initializes the SQLite database and creates the users table if it doesn't exist."""
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


# --- SECURITY & VALIDATION HELPERS ---
def hash_password(password: str) -> str:
    """Hashes a plain-text password using SHA-256."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def is_valid_email(email: str) -> bool:
    """Validates basic email formatting."""
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


# --- DATABASE OPERATIONS ---
def register_user(username: str, email: str, password: str) -> tuple[bool, str]:
    """Registers a new user in the database. Returns (success, message)."""
    password_hash = hash_password(password)
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username.strip(), email.strip().lower(), password_hash),
            )
            conn.commit()
        return True, "Account created successfully! Please switch to the Login tab."
    except sqlite3.IntegrityError as e:
        if "username" in str(e).lower():
            return False, "That username is already taken."
        elif "email" in str(e).lower():
            return False, "An account with that email already exists."
        return False, "Registration failed due to a database conflict."


def authenticate_user(username: str, password: str) -> dict | None:
    """Verifies user credentials. Returns user dict if valid, else None."""
    password_hash = hash_password(password)
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, email, created_at FROM users WHERE username = ? AND password_hash = ?",
            (username.strip(), password_hash),
        )
        row = cursor.fetchone()
        if row:
            return {
                "id": row[0],
                "username": row[1],
                "email": row[2],
                "created_at": row[3],
            }
    return None


# --- UI VIEWS ---
def show_dashboard():
    """Displays the protected dashboard for logged-in users."""
    user = st.session_state["user"]

    # Top bar with logout button
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title(f"Welcome, {user['username']}! 👋")
    with col2:
        st.write("")  # Vertical spacing alignment
        if st.button("Logout", type="primary", use_container_width=True):
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.rerun()

    st.divider()

    # Dashboard Content
    st.subheader("Your Account Overview")
    st.info(
        f"**Email:** {user['email']}  \n"
        f"**User ID:** #{user['id']}  \n"
        f"**Member Since:** {user['created_at']}"
    )

    st.write("### Protected Workspace")
    st.write("You are currently viewing a secure area accessible only to authenticated users.")


def show_auth_page():
    """Displays the Login and Sign Up tabs."""
    st.title("🔐 Secure Access Portal")
    st.write("Please log in to your account or register to get started.")

    login_tab, signup_tab = st.tabs(["Login", "Sign Up"])

    # --- LOGIN TAB ---
    with login_tab:
        with st.form("login_form"):
            st.subheader("Sign In")
            login_username = st.text_input("Username")
            login_password = st.text_input("Password", type="password")
            login_submitted = st.form_submit_button("Login", type="primary", use_container_width=True)

            if login_submitted:
                if not login_username or not login_password:
                    st.error("Please enter both your username and password.")
                else:
                    user_data = authenticate_user(login_username, login_password)
                    if user_data:
                        st.session_state["logged_in"] = True
                        st.session_state["user"] = user_data
                        st.rerun()
                    else:
                        st.error("Invalid username or password.")

    # --- SIGN UP TAB ---
    with signup_tab:
        with st.form("signup_form", clear_on_submit=False):
            st.subheader("Create a New Account")
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")
            signup_submitted = st.form_submit_button("Sign Up", type="primary", use_container_width=True)

            if signup_submitted:
                if not all([new_username, new_email, new_password, confirm_password]):
                    st.error("All fields are required.")
                elif len(new_username.strip()) < 3:
                    st.error("Username must be at least 3 characters long.")
                elif not is_valid_email(new_email.strip()):
                    st.error("Please enter a valid email address.")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long.")
                elif new_password != confirm_password:
                    st.error("Passwords do not match.")
                else:
                    success, message = register_user(new_username, new_email, new_password)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)


# --- MAIN APP ENTRYPOINT ---
def main():
    st.set_page_config(page_title="Secure Auth App", page_icon="🔐", layout="centered")
    init_db()

    # Initialize session state variables
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user" not in st.session_state:
        st.session_state["user"] = None

    # Route based on authentication status
    if st.session_state["logged_in"]:
        show_dashboard()
    else:
        show_auth_page()


if __name__ == "__main__":
    main()
