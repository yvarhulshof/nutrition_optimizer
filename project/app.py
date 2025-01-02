import os
import json
import io
import base64

import matplotlib
# Use a non-GUI backend to avoid "Starting a Matplotlib GUI outside the main thread" warnings
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from flask import Flask, request, render_template

from optimization.ilp_solver import optimize_nutrition

app = Flask(__name__)

# Load foods data at startup
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
FOODS_FILE = os.path.join(DATA_DIR, "foods.json")

with open(FOODS_FILE, 'r') as f:
    foods_data = json.load(f)

@app.route('/')
def index():
    """
    Render the 'index.html' template for the main form and script.
    """
    return render_template('index.html')

@app.route('/optimize', methods=['POST'])
def optimize():
    """
    1. Read JSON constraints from request (since front-end is using fetch + JSON or form data).
       (We'll check how main.js sends data—here we assume JSON or you can adapt for form data.)
    2. Solve ILP using 'optimize_nutrition'.
    3. Generate a chart in memory with Matplotlib.
    4. Return an HTML snippet that includes the base64-encoded chart <img>.
    """

    # If main.js sends JSON, do:
    # constraints = request.get_json()
    # If main.js sends form data, do something else. 
    # For now, let's assume JSON:
    constraints = request.get_json()
    if constraints is None:
        constraints = {}

    solution = optimize_nutrition(constraints, foods_data)

    # If not Optimal, return a small HTML snippet
    if solution['status'] != 'Optimal':
        return f"""
        <p>Solution Status: {solution['status']}</p>
        <p>No feasible solution found.</p>
        """

    # Build data for a stacked bar chart (protein, carbs, fat)
    selected_foods = []
    protein_vals = []
    carbs_vals = []
    fat_vals = []

    for food_name, qty in solution['quantities'].items():
        selected_foods.append(food_name)

        protein = foods_data[food_name].get('protein', 0)
        carbs   = foods_data[food_name].get('carbs',   0)
        fat     = foods_data[food_name].get('fat',     0)

        protein_vals.append(protein * qty)
        carbs_vals.append(carbs * qty)
        fat_vals.append(fat * qty)

    # Generate Matplotlib figure
    fig, ax = plt.subplots(figsize=(7, 5))
    x_positions = range(len(selected_foods))

    # Protein bars
    ax.bar(x_positions, protein_vals, label='Protein (g)', color='steelblue')
    # Carbs on top
    bottom_for_carbs = protein_vals
    ax.bar(x_positions, carbs_vals, bottom=bottom_for_carbs, label='Carbs (g)', color='gold')
    # Fat on top
    bottom_for_fat = [p + c for p, c in zip(protein_vals, carbs_vals)]
    ax.bar(x_positions, fat_vals, bottom=bottom_for_fat, label='Fat (g)', color='salmon')

    ax.set_xticks(list(x_positions))
    ax.set_xticklabels(selected_foods, rotation=45, ha='right')
    ax.set_ylabel('Grams')
    ax.set_title('Macro Contributions by Selected Foods')
    ax.legend()
    plt.tight_layout()

    # Convert to base64
    png_buffer = io.BytesIO()
    fig.savefig(png_buffer, format='png')
    png_buffer.seek(0)
    encoded_chart = base64.b64encode(png_buffer.read()).decode()
    plt.close(fig)

    # Build an HTML snippet containing the solution + chart
    html_response = f"""
    <h2>Solution Status: {solution['status']}</h2>
    <p>Objective Value (Total Cost): {solution['objective_value']}</p>
    <h3>Quantities:</h3>
    <ul>
    """
    for f, q in solution['quantities'].items():
        html_response += f"<li>{f}: {q}</li>"
    html_response += "</ul>"

    html_response += f"""
    <h3>Macro Chart</h3>
    <img src="data:image/png;base64,{encoded_chart}" alt="Stacked Bar Chart" />
    """

    return html_response

if __name__ == '__main__':
    app.run(debug=True)
