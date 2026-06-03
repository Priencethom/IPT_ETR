import matplotlib
matplotlib.use('Agg') 

from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector

from werkzeug.utils import secure_filename
import os


from cleaning import DataCleaning
from analytics import DataAnalytics
from visualization import DataVisualization

import numpy as np

app = Flask(__name__)
app.secret_key = "mind123"  # For session and flash messages

# MySQL configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Your MySQL password
    'database': 'ipt'  # Your MySQL database name
}

# -----------------------
# LOGIN ROUTE
# -----------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip().lower()  # Remove whitespace
        password = request.form['password']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True, buffered=True)

        cursor.execute(
            "SELECT * FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user is not None:
            session['username'] = user['username']
            session['role'] = user['role']

            flash(f"Welcome {user['username']}!", "success")
            return redirect(url_for('dashboard'))

        else:
            flash("Invalid username or password", "error")
            return redirect(url_for('login'))

    return render_template('login.html')

# -----------------------
# DASHBOARD ROUTE
# -----------------------


_clean = DataCleaning()
_clean.load_data()
_clean.fill_missing_values()
_clean.remove_duplicate_rows()
_clean.standardize_gender()
_clean.convert_data_types()
_clean.create_usage_level()
_clean.create_sleep_category()

_df = _clean.df

# Pre-compute stats once
_avg_usage      = round(float(_df["daily_social_media_hours"].mean()), 2)
_avg_academic   = round(float(_df["academic_performance"].mean()), 2)
_avg_stress     = round(float(_df["stress_level"].mean()), 2)
_avg_sleep      = round(float(_df["sleep_hours"].mean()), 2)
_avg_anxiety    = round(float(_df["anxiety_level"].mean()), 2)
_total_students = len(_df)

_corr_val = round(float(np.corrcoef(
    _df["daily_social_media_hours"],
    _df["academic_performance"]
)[0, 1]), 2)
_avg_correlation = _corr_val

# Correlation label based on actual value
if _corr_val >= 0.5:
    _corr_label = "Strong positive correlation"
elif _corr_val >= 0.2:
    _corr_label = "Moderate positive correlation"
elif _corr_val >= -0.2:
    _corr_label = "Weak / no correlation"
elif _corr_val >= -0.5:
    _corr_label = "Moderate negative correlation"
else:
    _corr_label = "Strong negative correlation"

# Platform breakdown from real data
_platform_counts = _df["platform_usage"].value_counts()
_platform_total  = _platform_counts.sum()
_platform_data   = [
    {"name": p, "count": int(c), "pct": round(int(c) / _platform_total * 100, 1)}
    for p, c in _platform_counts.items()
]

# Gender & usage level breakdowns
_gender_counts      = _df["gender"].value_counts().to_dict()
_usage_level_counts = _df["Social_Media_Usage_Level"].value_counts().to_dict()

# Generate charts only if they don't already exist
_charts_exist = all(os.path.exists(f"static/Images/{f}") for f in [
    "scatter_plot.png", "histogram_plot.png",
    "boxplot_chart.png", "grouped_bar_chart.png", "pie_chart.png"
])
if not _charts_exist:
    _visuals = DataVisualization(_df)
    _visuals.generate_all_charts()

    import matplotlib.pyplot as plt
    plt.close('all')


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('login'))

    # Read filter params from URL query string
    gender_filter      = request.args.get('gender', 'All')
    platform_filter    = request.args.get('platform', 'All')
    usage_level_filter = request.args.get('usage_level', 'All')

    # Start from the full cleaned dataframe
    df = _df.copy()

    # Apply filters
    if gender_filter != 'All':
        df = df[df['gender'].str.lower() == gender_filter.lower()]
    if platform_filter != 'All':
        df = df[df['platform_usage'].str.lower() == platform_filter.lower()]
    if usage_level_filter != 'All':
        df = df[df['Social_Media_Usage_Level'].str.lower() == usage_level_filter.lower()]

    # Recompute stats on filtered data
    if len(df) == 0:
        # Edge case: no rows match — return zeroes
        avg_usage = avg_academic = avg_stress = avg_sleep = avg_anxiety = 0
        total_students = 0
        avg_correlation = 0
        corr_label = "No data"
        platform_data = []
    else:
        avg_usage      = round(float(df["daily_social_media_hours"].mean()), 2)
        avg_academic   = round(float(df["academic_performance"].mean()), 2)
        avg_stress     = round(float(df["stress_level"].mean()), 2)
        avg_sleep      = round(float(df["sleep_hours"].mean()), 2)
        avg_anxiety    = round(float(df["anxiety_level"].mean()), 2)
        total_students = len(df)

        corr_val = round(float(np.corrcoef(
            df["daily_social_media_hours"],
            df["academic_performance"]
        )[0, 1]), 2) if len(df) > 1 else 0
        avg_correlation = corr_val

        if corr_val >= 0.5:
            corr_label = "Strong positive correlation"
        elif corr_val >= 0.2:
            corr_label = "Moderate positive correlation"
        elif corr_val >= -0.2:
            corr_label = "Weak / no correlation"
        elif corr_val >= -0.5:
            corr_label = "Moderate negative correlation"
        else:
            corr_label = "Strong negative correlation"

        platform_counts = df["platform_usage"].value_counts()
        platform_total  = platform_counts.sum()
        platform_data   = [
            {"name": p, "count": int(c), "pct": round(int(c) / platform_total * 100, 1)}
            for p, c in platform_counts.items()
        ]

    # Generate filtered charts
    import matplotlib.pyplot as plt
    visuals = DataVisualization(df)
    visuals.generate_all_charts()
    plt.close('all')

    return render_template(
        'dashboard1.html',
        username=session['username'],
        avg_usage=avg_usage,
        avg_academic=avg_academic,
        avg_stress=avg_stress,
        avg_sleep=avg_sleep,
        avg_anxiety=avg_anxiety,
        total_students=total_students,
        avg_correlation=avg_correlation,
        corr_label=corr_label,
        platform_data=platform_data,
        gender_counts=_gender_counts,
        usage_level_counts=_usage_level_counts,
        scatter_chart='Images/scatter_plot.png',
        histogram_chart='Images/histogram_plot.png',
        boxplot_chart='Images/boxplot_chart.png',
        grouped_bar_chart='Images/grouped_bar_chart.png',
        pie_chart='Images/pie_chart.png',
        scatter_plot2="Images/scatter_plot2.png",
        histogram_plot2="Images/histogram_plot2.png",
        boxplot_chart2="Images/boxplot_chart2.png",
        grouped_bar_chart2="Images/grouped_bar_chart2.png",
        pie_chart2="Images/pie_chart2.png",
        # Pass current filter values back so selects stay in sync
        selected_gender=gender_filter,
        selected_platform=platform_filter,
        selected_usage_level=usage_level_filter,
    )

@app.route('/account')
def account():
    # Check if user is logged in
    if 'username' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('login'))

    username = session['username']

    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True, buffered=True)

    # Fetch user info from the database
    cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
    user_info = cursor.fetchone()  # returns a dictionary

    # Close cursor and connection
    cursor.close()
    conn.close()

    if not user_info:
        flash("User not found.", "error")
        return redirect(url_for('login'))

    # Pass the user dictionary to the template
    return render_template('account.html', user=user_info)


# -------------------------
# Edit Account Page
# -------------------------
@app.route('/account/edit', methods=['GET', 'POST'])
def edit_account():
    if 'username' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('login'))

    username = session['username']
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        new_username = request.form['username']
        new_role = request.form['role']
        new_password = request.form['password'] or None

        # Handle photo upload
        photo = request.files.get('profile_photo')
        photo_filename = None

        if photo and photo.filename:
            photo_filename = secure_filename(photo.filename)

            upload_folder = os.path.join(
                app.static_folder,
                'uploads'
            )

            os.makedirs(upload_folder, exist_ok=True)

            photo.save(
                os.path.join(upload_folder, photo_filename)
            )

        # Update database
        if new_password:
            if photo_filename:
                cursor.execute("""
                    UPDATE users
                    SET username=%s,
                        role=%s,
                        password=%s,
                        profile_photo=%s
                    WHERE username=%s
                """, (
                    new_username,
                    new_role,
                    new_password,
                    photo_filename,
                    username
                ))
            else:
                cursor.execute("""
                    UPDATE users
                    SET username=%s,
                        role=%s,
                        password=%s
                    WHERE username=%s
                """, (
                    new_username,
                    new_role,
                    new_password,
                    username
                ))
        else:
            if photo_filename:
                cursor.execute("""
                    UPDATE users
                    SET username=%s,
                        role=%s,
                        profile_photo=%s
                    WHERE username=%s
                """, (
                    new_username,
                    new_role,
                    photo_filename,
                    username
                ))
            else:
                cursor.execute("""
                    UPDATE users
                    SET username=%s,
                        role=%s
                    WHERE username=%s
                """, (
                    new_username,
                    new_role,
                    username
                ))

        conn.commit()
        session['username'] = new_username

        flash("Profile updated successfully!", "success")

        cursor.close()
        conn.close()

        return redirect(url_for('account'))

    cursor.execute(
        "SELECT * FROM users WHERE username=%s",
        (username,)
    )

    user_info = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template('_edit.html', user=user_info)


# -----------------------
# LEARNINGS ROUTE
# -----------------------
@app.route('/learnings')
def learnings():
    if 'username' not in session:
        flash("Please login first.", "warning")
        return redirect(url_for('login'))
    return render_template('learnings.html', username=session['username'])




# -----------------------
# LOGOUT ROUTE
# -----------------------
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))

# -----------------------
# ROOT ROUTE
# -----------------------
@app.route('/')
def home():
    return redirect(url_for('login'))

# -----------------------
# RUN APP
# -----------------------
if __name__ == '__main__':
    app.run(debug=True)
