from flask import Flask, render_template, request
from flask import Flask, render_template, request
from datetime import date,datetime

app = Flask(__name__)

# 👇 ADD THIS BLOCK HERE
user_data = {
    "last_date": None,
    "streak": 0,
    "saplings": 0
}

# -------------------------
# HOME PAGE
# -------------------------
@app.route('/')
def home():
    return render_template('index.html')


# -------------------------
# DASHBOARD
# -------------------------
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


# -------------------------
# TRACKER PAGE
# -------------------------
@app.route('/tracker')
def tracker():
    return render_template('tracker.html')


# -------------------------
# CALCULATION LOGIC
# -------------------------
@app.route('/calculate', methods=['POST'])
def calculate():

    try:
        water = float(request.form.get('water', 0))
        electricity = float(request.form.get('electricity', 0))
        waste = float(request.form.get('waste', 0))
        transport = request.form.get('transport', 'Walk')
    except:
        water, electricity, waste = 0, 0, 0
        transport = "Walk"

    # -------------------------
    # SCORE CALCULATION
    # -------------------------
    score = 100

    score -= water * 0.1
    score -= electricity * 0.2
    score -= waste * 2

    if transport == "Car":
        score -= 15
    elif transport == "Bus":
        score -= 5
    elif transport == "Bicycle":
        score += 5
    elif transport == "Walk":
        score += 10

    score = max(0, min(100, score))

    # -------------------------
    # TREE STAGE
    # -------------------------
    if score <= 25:
        tree_stage = "🌱 Seed"
    elif score <= 50:
        tree_stage = "🌿 Sapling"
    elif score <= 75:
        tree_stage = "🌳 Young Tree"
    else:
        tree_stage = "🌲 Mature Tree"

    # -------------------------
    # BADGES
    # -------------------------
    if score >= 90:
        badge = "🏆 Sustainability Champion"
    elif score >= 75:
        badge = "⚡ Energy Hero"
    elif score >= 60:
        badge = "💧 Water Saver"
    else:
        badge = "🌱 Eco Beginner"

    # -------------------------
    # CARBON FOOTPRINT
    # -------------------------
    carbon = round((electricity * 0.5) + (waste * 0.3), 2)

    # -------------------------
    # RECOMMENDATIONS
    # -------------------------
    recommendations = []

    if water > 100:
        recommendations.append("💧 Reduce water usage to save resources.")

    if electricity > 50:
        recommendations.append("⚡ Use energy-efficient appliances.")

    if waste > 5:
        recommendations.append("♻ Reduce and recycle waste properly.")

    if transport == "Car":
        recommendations.append("🚲 Use public transport or cycling instead of cars.")

    if not recommendations:
        recommendations.append("🌱 Great job! Keep your eco habits strong.")

    # -------------------------
    # RESULT PAGE
    # -------------------------
    return render_template(
        'result.html',
        score=round(score, 2),
        carbon=carbon,
        tree_stage=tree_stage,
        badge=badge,
        recommendations=recommendations
    )


# -------------------------
# OTHER PAGES
# -------------------------
@app.route('/forest')
def forest():
    return render_template('forest.html')


@app.route('/badges')
def badges():
    return render_template('badges.html')


@app.route('/impact')
def impact():
    return render_template('impact.html')


@app.route('/plant-sapling')
def plant_sapling():

    today = date.today()

    # first time
    if user_data["last_date"] is None:
        user_data["streak"] = 1

    # same day already planted
    elif user_data["last_date"] == today:
        return "🌱 Already planted today!"

    # consecutive day
    elif user_data["last_date"] == (today - timedelta(days=1)):
        user_data["streak"] += 1

    # broken streak
    else:
        user_data["streak"] = 1

    user_data["last_date"] = today
    user_data["saplings"] += 1

    # BADGES
    if user_data["streak"] >= 30:
        badge = "🏆 Planet Protector"
    elif user_data["streak"] >= 15:
        badge = "🌲 Forest Guardian"
    elif user_data["streak"] >= 7:
        badge = "🌳 Eco Warrior"
    elif user_data["streak"] >= 3:
        badge = "🌿 Consistent Gardener"
    else:
        badge = "🌱 Beginner Planter"

    return render_template("plant_result.html",
        streak=user_data["streak"],
        saplings=user_data["saplings"],
        badge=badge
    )


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():

    sentiment = None
    category = None
    suggestion = None
    result = None

    if request.method == 'POST':

        text = request.form['message'].lower()

        # -------------------------
        # 1. SENTIMENT ANALYSIS
        # -------------------------
        positive_words = ["good", "great", "love", "excellent", "happy", "save", "clean", "reduce", "better"]
        negative_words = ["bad", "waste", "pollution", "dirty", "damage", "hate", "problem", "worst"]

        score = 0

        for w in positive_words:
            if w in text:
                score += 1

        for w in negative_words:
            if w in text:
                score -= 1

        if score > 0:
            sentiment = "😊 Positive Eco Mindset"
        elif score < 0:
            sentiment = "⚠ Negative Eco Impact"
        else:
            sentiment = "😐 Neutral"

        # -------------------------
        # 2. CATEGORY DETECTION
        # -------------------------
        if "water" in text:
            category = "💧 Water"
            suggestion = "Reduce water usage, fix leaks, and reuse water when possible."

        elif "electricity" in text or "energy" in text:
            category = "⚡ Energy"
            suggestion = "Switch off unused appliances and use LED bulbs."

        elif "waste" in text or "plastic" in text:
            category = "♻ Waste"
            suggestion = "Recycle properly and avoid single-use plastics."

        elif "car" in text or "transport" in text or "vehicle" in text:
            category = "🚗 Transport"
            suggestion = "Use public transport, cycling, or walking instead of cars."

        else:
            category = "🌍 General"
            suggestion = "Keep practicing sustainable eco-friendly habits."

        result = "Analysis Completed"

    return render_template(
        "feedback.html",
        sentiment=sentiment,
        category=category,
        suggestion=suggestion,
        result=result
    )



@app.route('/report')
def report():

    # Example data (later you can connect real user data)
    water = 120
    electricity = 60
    waste = 5

    score = max(100 - (water*0.1 + electricity*0.2 + waste*2), 0)

    # ECO LEVEL
    if score > 80:
        level = "🌳 Eco Warrior"
    elif score > 60:
        level = "🌿 Green Learner"
    else:
        level = "🌱 Beginner"

    # IMPACT
    carbon = round(electricity * 0.4 + waste * 1.2, 2)

    # BADGES
    badges = []
    if water < 100:
        badges.append("💧 Water Saver")
    if electricity < 50:
        badges.append("⚡ Energy Hero")
    if waste < 3:
        badges.append("♻ Waste Reducer")

    # FUTURE MESSAGE
    if score > 75:
        future = "🌍 You are on track to become a Climate Champion!"
    else:
        future = "⚠ Improve habits to reduce environmental impact."

    return render_template(
        "report.html",
        score=round(score,2),
        level=level,
        carbon=carbon,
        badges=badges,
        future=future,
        date=datetime.now().strftime("%d-%m-%Y")
    )


@app.route('/future-message', methods=['GET', 'POST'])
def future_message():

    message = None
    city = None
    future_type = None

    if request.method == 'POST':

        city = request.form['city']
        future_type = request.form['future_type']

        sustainable = {
            "Bengaluru": "Hello from Bengaluru 2050 🌿 Because people reduced plastic waste in 2026, lakes are clean and water is abundant.",
            "Delhi": "Hello from Delhi 2050 🌿 Air pollution reduced due to strict emission control.",
            "Mumbai": "Hello from Mumbai 2050 🌿 Coastal protection saved the city from flooding.",
            "Chennai": "Hello from Chennai 2050 🌿 Water conservation made the city drought-free.",
            "Hyderabad": "Hello from Hyderabad 2050 🌿 Green tech transformed the city into a clean energy hub."
        }

        unsustainable = {
            "Bengaluru": "Hello from Bengaluru 2050 🌫️ Lakes vanished due to pollution and waste.",
            "Delhi": "Hello from Delhi 2050 🌫️ Air is toxic due to uncontrolled emissions.",
            "Mumbai": "Hello from Mumbai 2050 🌫️ Rising sea levels flooded coastal areas.",
            "Chennai": "Hello from Chennai 2050 🌫️ Severe water shortage affects daily life.",
            "Hyderabad": "Hello from Hyderabad 2050 🌫️ Extreme heatwaves dominate the city."
        }

        if future_type == "sustainable":
            message = sustainable.get(city, "🌿 Sustainable future achieved!")
        else:
            message = unsustainable.get(city, "🌫️ Unsustainable future warning!")

    return render_template(
        "future.html",
        message=message,
        city=city,
        future_type=future_type
    )


# -------------------------
# BIRD REPORT SYSTEM
# -------------------------
reports = []

@app.route('/report-bird', methods=['GET', 'POST'])
def report_bird():

    message = None

    if request.method == 'POST':
        location = request.form['location']
        issue = request.form['issue']

        reports.append({
            "location": location,
            "issue": issue
        })

        message = "Report submitted successfully 🚨"

    return render_template('report_bird.html', message=message, reports=reports)


# -------------------------
# RISK ZONES (SIMULATED AI)
# -------------------------
@app.route('/risk-map')
def risk_map():

    zones = {
        "Central City": "🔴 High Risk (Power lines + traffic)",
        "Lake Area": "🟢 Safe Zone (Bird habitat)",
        "Industrial Area": "🔴 High Risk (Transformers)",
        "Green Park": "🟢 Safe Zone (Trees + nesting)"
    }

    return render_template('risk_map.html', zones=zones)


# -------------------------
# TREE CORRIDOR SUGGESTION
# -------------------------
@app.route('/corridor')
def corridor():

    suggestions = [
        "🌳 Plant trees near highways to reduce collisions",
        "🌿 Create green bridges between parks",
        "🐦 Protect lake edges as nesting zones",
        "⚡ Move new power lines underground in sensitive areas"
    ]

    return render_template('corridor.html', suggestions=suggestions)


# -------------------------
# BIRD FLIGHT SIMULATOR (UNIQUE FEATURE)
# -------------------------
@app.route('/simulator', methods=['GET', 'POST'])
def simulator():

    path = None

    if request.method == 'POST':
        area = request.form['area']

        if area == "City Center":
            path = "🐦 Bird path blocked by buildings and power lines ❌"
        elif area == "Lake Area":
            path = "🐦 Smooth flight path over water and trees 🌿"
        elif area == "Industrial Area":
            path = "🐦 High danger zone, avoid flying 🚨"
        else:
            path = "🐦 Moderate risk area, some obstacles ⚠"

    return render_template('simulator.html', path=path)


# 🌍 Personal Carbon Tracker
@app.route('/carbon', methods=['GET', 'POST'])
def carbon():

    score = None
    suggestion = None

    if request.method == 'POST':
        electricity = float(request.form['electricity'])
        transport = float(request.form['transport'])
        waste = float(request.form['waste'])

        score = electricity*0.5 + transport*0.8 + waste*0.6

        if score < 5:
            suggestion = "🌿 Low carbon footprint"
        elif score < 10:
            suggestion = "⚡ Moderate footprint"
        else:
            suggestion = "🚨 High carbon footprint"

    return render_template('carbon.html', score=score, suggestion=suggestion)


# 🐦 Wildlife Protection System
@app.route('/wildlife')
def wildlife():

    alerts = [
        "🐦 Bird collision risk near transformers",
        "🌳 Safe nesting zones in parks",
        "⚡ Power lines danger zones"
    ]

    return render_template('wildlife.html', alerts=alerts)


# 🏙 Smart City Pollution Analysis
@app.route('/pollution')
def pollution():

    cities = {
        "Bengaluru": 65,
        "Delhi": 180,
        "Mumbai": 120,
        "Chennai": 90
    }

    return render_template('pollution.html', cities=cities)


# 🤖 AI Eco Advisor
@app.route('/advisor', methods=['GET', 'POST'])
def advisor():

    advice = None

    if request.method == 'POST':
        issue = request.form['issue'].lower()

        if "water" in issue:
            advice = "💧 Save water using buckets"
        elif "plastic" in issue:
            advice = "♻ Use reusable items"
        elif "electricity" in issue:
            advice = "⚡ Switch off unused appliances"
        else:
            advice = "🌿 Plant trees"

    return render_template('advisor.html', advice=advice)


# 🌍 Future Simulation
@app.route('/future', methods=['GET', 'POST'])
def future():

    message = None

    if request.method == 'POST':
        city = request.form['city']
        mode = request.form['mode']

        if mode == "sustainable":
            message = f"🌿 {city} 2050: Clean, green, safe city"
        else:
            message = f"🌫️ {city} 2050: Pollution, heat, water shortage"

    return render_template('future.html', message=message)


@app.route('/report')
def report2():

    report_data = {
        "carbon": "Moderate footprint (reduce transport usage)",
        "pollution": "Delhi: High risk, Bengaluru: Moderate",
        "wildlife": "Bird collision zones near power lines",
        "ai_advice": "Switch to renewable energy + reduce plastic usage",
        "future_risk": "2050: Water shortage risk if usage continues"
    }

    return render_template("report.html", report=report_data)


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == '__main__':
    print("🌍 EcoGuardian Running at http://127.0.0.1:5000")
    app.run(debug=True)