import pulp

def optimize_nutrition(constraints, foods_data):
    """
    ILP that:
      - Minimizes total cost
      - Potential constraints:
        * min_calories
        * max_calories
        * min_protein
        * min_fiber
        * max_sugars
        * min_vitamin_c
    """

    # Create the problem
    problem = pulp.LpProblem("Nutrition_Optimization", pulp.LpMinimize)

    # Define decision variables
    food_items = list(foods_data.keys())
    x = pulp.LpVariable.dicts('quantity', food_items, lowBound=0, cat=pulp.LpInteger)
    # If you want fractional amounts, use cat=pulp.LpContinuous

    # Objective: minimize total cost
    problem += pulp.lpSum([foods_data[f]['cost'] * x[f] for f in food_items]), "Total_Cost"

    # ---------- CALORIES (min / max) ----------
    if 'min_calories' in constraints and constraints['min_calories']:
        min_cal = float(constraints['min_calories'])
        problem += (
            pulp.lpSum([foods_data[f]['calories'] * x[f] for f in food_items])
            >= min_cal
        ), "MinCalories"

    if 'max_calories' in constraints and constraints['max_calories']:
        max_cal = float(constraints['max_calories'])
        problem += (
            pulp.lpSum([foods_data[f]['calories'] * x[f] for f in food_items])
            <= max_cal
        ), "MaxCalories"

    # ---------- PROTEIN (min) ----------
    if 'min_protein' in constraints and constraints['min_protein']:
        min_prot = float(constraints['min_protein'])
        problem += (
            pulp.lpSum([foods_data[f].get('protein', 0) * x[f] for f in food_items])
            >= min_prot
        ), "MinProtein"

    # ---------- FIBER (min) ----------
    if 'min_fiber' in constraints and constraints['min_fiber']:
        min_fiber = float(constraints['min_fiber'])
        problem += (
            pulp.lpSum([foods_data[f].get('fiber', 0) * x[f] for f in food_items])
            >= min_fiber
        ), "MinFiber"

    # ---------- SUGARS (max) ----------
    if 'max_sugars' in constraints and constraints['max_sugars']:
        max_sugars = float(constraints['max_sugars'])
        problem += (
            pulp.lpSum([foods_data[f].get('sugars', 0) * x[f] for f in food_items])
            <= max_sugars
        ), "MaxSugars"

    # ---------- VITAMIN C (min) ----------
    if 'min_vitamin_c' in constraints and constraints['min_vitamin_c']:
        min_vit_c = float(constraints['min_vitamin_c'])
        problem += (
            pulp.lpSum([foods_data[f].get('vitamin_c', 0) * x[f] for f in food_items])
            >= min_vit_c
        ), "MinVitaminC"

    # Solve the problem
    solver = pulp.PULP_CBC_CMD(msg=0)
    problem.solve(solver)

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
