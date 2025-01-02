import pulp
import logging
import os

# 1. Configure Python's logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# 2. Set up a file handler for logs. You can name your log file anything.
log_file = os.path.join(os.path.dirname(__file__), 'solver_debug.log')
fh = logging.FileHandler(log_file)
fh.setLevel(logging.DEBUG)

# Optional: Add a formatter
formatter = logging.Formatter(
    '%(asctime)s - [%(levelname)s] - %(filename)s:%(lineno)d - %(message)s'
)
fh.setFormatter(formatter)

# 3. Add the handler to the logger
logger.addHandler(fh)


def optimize_nutrition(constraints, foods_data):
    """
    Example ILP that:
    - Minimizes total cost
    - Enforces optional min/max constraints on:
        * Calories
        * Protein
        * Fiber (min)
        * Sugars (max)
        * Vitamin C (min)
        etc.
    """
    logger.info("Starting optimization with constraints: %s", constraints)

    # Create the problem
    problem = pulp.LpProblem("Nutrition_Optimization", pulp.LpMinimize)

    # Define decision variables:
    food_items = list(foods_data.keys())

    # If using integer quantities, cat=pulp.LpInteger
    # For easier feasibility, you might consider pulp.LpContinuous
    x = pulp.LpVariable.dicts('quantity', food_items, lowBound=0, cat=pulp.LpInteger)

    # Objective: minimize total cost
    problem += pulp.lpSum([foods_data[f]['cost'] * x[f] for f in food_items]), "Total_Cost"

    # ------------------ SAMPLE CONSTRAINTS ------------------
    # Calories (min / max)
    if 'min_calories' in constraints and constraints['min_calories']:
        min_cal = float(constraints['min_calories'])
        problem += pulp.lpSum([foods_data[f]['calories'] * x[f] for f in food_items]) >= min_cal, "MinCalories"

    if 'max_calories' in constraints and constraints['max_calories']:
        max_cal = float(constraints['max_calories'])
        problem += pulp.lpSum([foods_data[f]['calories'] * x[f] for f in food_items]) <= max_cal, "MaxCalories"

    # Protein (min)
    if 'min_protein' in constraints and constraints['min_protein']:
        min_prot = float(constraints['min_protein'])
        problem += pulp.lpSum([foods_data[f]['protein'] * x[f] for f in food_items]) >= min_prot, "MinProtein"

    # Fiber (min)
    if 'min_fiber' in constraints and constraints['min_fiber']:
        min_fiber = float(constraints['min_fiber'])
        problem += pulp.lpSum([foods_data[f].get('fiber', 0) * x[f] for f in food_items]) >= min_fiber, "MinFiber"

    # Sugars (max)
    if 'max_sugars' in constraints and constraints['max_sugars']:
        max_sugars = float(constraints['max_sugars'])
        problem += pulp.lpSum([foods_data[f].get('sugars', 0) * x[f] for f in food_items]) <= max_sugars, "MaxSugars"

    # Vitamin C (min)
    if 'min_vitamin_c' in constraints and constraints['min_vitamin_c']:
        min_vit_c = float(constraints['min_vitamin_c'])
        problem += pulp.lpSum([foods_data[f].get('vitamin_c', 0) * x[f] for f in food_items]) >= min_vit_c, "MinVitaminC"

    # ---------------------------------------------------------
    # Write out the LP model for inspection
    lp_file = os.path.join(os.path.dirname(__file__), "model.lp")
    problem.writeLP(lp_file)
    logger.debug("Wrote LP model to %s", lp_file)

    # Solve the problem
    # - msg=1 prints solver output to console
    # - logPath='cbc_log.txt' writes solver logs to a file
    solver = pulp.PULP_CBC_CMD(msg=1, logPath=os.path.join(os.path.dirname(__file__), "cbc_solver.log"))
    result = problem.solve(solver)

    # Prepare the result
    status = pulp.LpStatus[problem.status]
    logger.info("Solver finished. Status: %s", status)

    if status == 'Optimal':
        obj_value = pulp.value(problem.objective)
        logger.info("Optimal objective value: %s", obj_value)
    else:
        logger.warning("No optimal solution found. Status: %s", status)

    solution = {
        "status": status,
        "objective_value": pulp.value(problem.objective) if status == 'Optimal' else None,
        "quantities": {}
    }

    if status == 'Optimal':
        # Extract chosen quantities (only list foods with quantity > 0)
        for f in food_items:
            qty = x[f].varValue
            if qty > 0:
                solution["quantities"][f] = int(qty)
                logger.debug("Selected %s units of %s", qty, f)

    return solution
