#!/usr/bin/env python3
import os
import zipfile

# Dictionary mapping file paths to file contents
FILES = {
    # ---------- ROOT FILES ----------
    "nutrition_optimizer/requirements.txt": """Flask==2.3.2
PuLP==2.7.0
""",
    "nutrition_optimizer/app.py": '''from flask import Flask, render_template, request, jsonify
import json
import os

from optimization.ilp_solver import optimize_nutrition

app = Flask(__name__)

# Load foods data at startup
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
FOODS_FILE = os.path.join(DATA_DIR, "foods.json")

with open(FOODS_FILE, 'r') as f:
    foods_data = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/optimize', methods=['POST'])
def optimize():
    # Extract JSON from the request
    constraints = request.get_json()

    # Call the solver
    solution = optimize_nutrition(constraints, foods_data)

    return jsonify(solution)


if __name__ == '__main__':
    # For local development only; not recommended for production
    app.run(debug=True)
''',

    # ---------- DATA FILES ----------
    "nutrition_optimizer/data/foods.json": '''{
  "apple": {
    "calories": 95,
    "protein": 0.5,
    "fat": 0.2,
    "carbs": 25,
    "cost": 0.5
  },
  "banana": {
    "calories": 105,
    "protein": 1.3,
    "fat": 0.4,
    "carbs": 27,
    "cost": 0.3
  },
  "chicken_breast": {
    "calories": 165,
    "protein": 31,
    "fat": 3.6,
    "carbs": 0,
    "cost": 2.0
  }
}
''',

    # ---------- OPTIMIZATION FILES ----------
    "nutrition_optimizer/optimization/ilp_solver.py": '''import pulp

def optimize_nutrition(constraints, foods_data):
    """
    Example ILP that:
    - Minimizes total cost
    - Meets min/max calories if provided
    - Meets minimum protein if provided
    """

    # Create the problem
    problem = pulp.LpProblem("Nutrition_Optimization", pulp.LpMinimize)

    # Define decision variables:
    food_items = list(foods_data.keys())
    x = pulp.LpVariable.dicts('quantity', food_items, lowBound=0, cat=pulp.LpInteger)

    # Objective: minimize total cost
    problem += pulp.lpSum([foods_data[f]['cost'] * x[f] for f in food_items]), "Total_Cost"

    # min_calories constraint
    if 'min_calories' in constraints and constraints['min_calories']:
        min_cal = float(constraints['min_calories'])
        problem += pulp.lpSum([foods_data[f]['calories'] * x[f] for f in food_items]) >= min_cal, "MinCalories"

    # max_calories constraint
    if 'max_calories' in constraints and constraints['max_calories']:
        max_cal = float(constraints['max_calories'])
        problem += pulp.lpSum([foods_data[f]['calories'] * x[f] for f in food_items]) <= max_cal, "MaxCalories"

    # min_protein constraint
    if 'min_protein' in constraints and constraints['min_protein']:
        min_prot = float(constraints['min_protein'])
        problem += pulp.lpSum([foods_data[f]['protein'] * x[f] for f in food_items]) >= min_prot, "MinProtein"

    # Solve the problem
    problem.solve(pulp.PULP_CBC_CMD(msg=0))

    # Prepare the result
    status = pulp.LpStatus[problem.status]
    solution = {
        "status": status,
        "objective_value": pulp.value(problem.objective) if status == 'Optimal' else None,
        "quantities": {}
    }

    if status == 'Optimal':
        # Extract chosen quantities
        for f in food_items:
            qty = x[f].varValue
            if qty > 0:
                solution["quantities"][f] = int(qty)

    return solution
''',

    # ---------- STATIC FILES ----------
    "nutrition_optimizer/static/css/style.css": '''body {
    font-family: Arial, sans-serif;
    margin: 20px;
}
label {
    display: inline-block;
    width: 120px;
}
input {
    margin-bottom: 10px;
}
#result {
    margin-top: 20px;
    white-space: pre;
    background: #f9f9f9;
    padding: 10px;
    border: 1px solid #ccc;
}
''',

    "nutrition_optimizer/static/js/main.js": '''document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('optimizationForm');
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const formData = {
            min_calories: document.getElementById('min_calories').value,
            max_calories: document.getElementById('max_calories').value,
            min_protein: document.getElementById('min_protein').value,
        };

        // Send a POST request to /optimize
        const response = await fetch('/optimize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData),
        });

        const result = await response.json();
        document.getElementById('result').innerText = JSON.stringify(result, null, 2);
    });
});
''',

    # ---------- TEMPLATE FILES ----------
    "nutrition_optimizer/templates/index.html": '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Nutrition Optimizer</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <h1>Nutrition Optimizer</h1>
    <form id="optimizationForm">
        <label for="min_calories">Min Calories:</label>
        <input type="number" name="min_calories" id="min_calories" required><br>

        <label for="max_calories">Max Calories:</label>
        <input type="number" name="max_calories" id="max_calories"><br>

        <label for="min_protein">Min Protein (g):</label>
        <input type="number" name="min_protein" id="min_protein"><br>

        <!-- Add more fields here if needed -->

        <button type="submit">Optimize</button>
    </form>

    <div id="result"></div>

    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
'''
}

def main():
    # Create a ZIP file with the above structure
    zip_filename = "nutrition_optimizer.zip"
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zf:
        for filepath, content in FILES.items():
            zf.writestr(filepath, content)
    print(f"Created {zip_filename} with the nutrition_optimizer project structure.")

if __name__ == "__main__":
    main()
