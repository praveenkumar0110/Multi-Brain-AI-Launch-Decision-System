from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
from flask_bcrypt import Bcrypt
from datetime import datetime
from bson.objectid import ObjectId
import os

# ---------------------------------------------------------
# 🧠 IMPORTING OUR MODULAR AI BRAIN
# ---------------------------------------------------------
from ai_core.brain_orchestrator import MultiAgentOrchestrator

app = Flask(__name__)

# --- CONFIGURATION ---
app.config['MONGO_URI'] = 'mongodb://localhost:27017/'
app.config['SECRET_KEY'] = 'super_secret_key_for_session' 
app.config['JWT_SECRET_KEY'] = 'jwt_secret_key_for_auth' 
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False 

# --- INITIALIZATION ---
client = MongoClient(app.config['MONGO_URI'])
db = client['ai_launch_system']  
users_col = db['users']          
products_col = db['products']    

jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# 🔥 Initialize the Multi-Agent AI Engine
ai_engine = MultiAgentOrchestrator()

# --- ROUTES ---

@app.route('/')
def home():
    return redirect(url_for('login'))

# 🔐 LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = users_col.find_one({'email': email})
        
        if user and bcrypt.check_password_hash(user['password'], password):
            access_token = create_access_token(identity=email)
            resp = make_response(redirect(url_for('dashboard')))
            set_access_cookies(resp, access_token)
            return resp
        else:
            flash("Invalid Email or Password", "danger")
            
    return render_template('login.html')

# 🆕 REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if users_col.find_one({'email': email}):
            flash("User already exists! Please login.", "warning")
            return redirect(url_for('login'))
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        users_col.insert_one({'email': email, 'password': hashed_password})
        
        flash("Account Created Successfully! Login now.", "success")
        return redirect(url_for('login'))
            
    return render_template('register.html')

# 🏠 DASHBOARD
@app.route('/dashboard')
@jwt_required()
def dashboard():
    current_user = get_jwt_identity()
    history = list(products_col.find({'user': current_user}).sort('timestamp', -1))
    return render_template('dashboard.html', user=current_user, history=history)

# 📝 INPUT PAGE & ANALYZE TRIGGER
@app.route('/analyze', methods=['GET', 'POST'])
@jwt_required()
def analyze_product():
    if request.method == 'POST':
        # Collect data from form
        data = {
            "name": request.form['name'],
            "type": request.form['type'],
            "completion": request.form['completion'],
            "users": request.form['users'],
            "date": request.form['date'],
            "marketing": request.form['marketing']
        }
        
        # ⚠️ CRITICAL FIX HERE: 
        # Send to 'loader.html' (The Animation), NOT 'analyzing.html'
        # This fixes the "record is undefined" error.
        return render_template('loader.html', data=data)
    
    return render_template('input.html')

# 🤖 AI PROCESSING (Called automatically by loader.html)
@app.route('/process_ai', methods=['POST'])
@jwt_required()
def process_ai():
    data = request.form.to_dict()
    current_user = get_jwt_identity()
    
    # 🔥 RUN AI ENGINE
    ai_result = ai_engine.run_simulation(data)
    
    # Save to MongoDB
    record = {
        "user": current_user,
        "details": data,
        "ai_result": ai_result,
        "timestamp": datetime.now()
    }
    inserted_id = products_col.insert_one(record).inserted_id
    
    # Redirect to Result Page (Image 1 - The Grid)
    return redirect(url_for('result', pid=str(inserted_id)))

# 📊 RESULT PAGE (Image 1 - Grid View)
@app.route('/result/<pid>')
@jwt_required()
def result(pid):
    record = products_col.find_one({'_id': ObjectId(pid)})
    if not record:
        return "Analysis not found", 404
    return render_template('result.html', record=record)

# 🏆 FINAL DECISION PAGE (Image 2 - The Modal View)
@app.route('/decision/<pid>')
@jwt_required()
def decision_page(pid):
    record = products_col.find_one({'_id': ObjectId(pid)})
    if not record:
        return "Record not found", 404
    return render_template('decision.html', record=record)

# 📈 VISUALIZATION PAGE (Image 3 - Bars)
@app.route('/visualization/<pid>')
@jwt_required()
def visualization_page(pid):
    record = products_col.find_one({'_id': ObjectId(pid)})
    if not record:
        return "Record not found", 404
    
    scores = record['ai_result']['scores']
    
    # Logic for Bottom Stats
    highest_brain = max(scores, key=scores.get)
    highest_score = scores[highest_brain]
    
    lowest_brain = min(scores, key=scores.get)
    lowest_score = scores[lowest_brain]
    
    avg_score = int(sum(scores.values()) / len(scores))

    return render_template('visualization.html', 
                           record=record, 
                           high=(highest_brain, highest_score), 
                           low=(lowest_brain, lowest_score), 
                           avg=avg_score)

# 📄 REPORT PAGE (Image 4 - Download)
@app.route('/report/<pid>')
@jwt_required()
def report_page(pid):
    record = products_col.find_one({'_id': ObjectId(pid)})
    if not record:
        return "Record not found", 404
    return render_template('report.html', record=record)

# 📜 HISTORY PAGE
@app.route('/history')
@jwt_required()
def history_page():
    current_user = get_jwt_identity()
    records = list(products_col.find({'user': current_user}).sort('timestamp', -1))
    
    # Calculate Stats
    total_count = len(records)
    launched_count = sum(1 for r in records if 'LAUNCH' in r['ai_result']['decision'])
    delayed_count = sum(1 for r in records if 'DELAY' in r['ai_result']['decision'])
    
    return render_template('history.html', 
                           history=records, 
                           total=total_count, 
                           launched=launched_count, 
                           delayed=delayed_count)

# 🚪 LOGOUT
@app.route('/logout')
def logout():
    resp = make_response(redirect(url_for('login')))
    unset_jwt_cookies(resp)
    return resp

if __name__ == "__main__":
    app.run(debug=True, port=5000)