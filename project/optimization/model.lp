\* Nutrition_Optimization *\
Minimize
Total_Cost: 0.5 quantity_almonds + 0.5 quantity_apple + 0.3 quantity_banana
 + 0.2 quantity_brown_rice_cooked + 0.2 quantity_carrot
 + 2 quantity_chicken_breast + 1.2 quantity_greek_yogurt_plain_nonfat
 + 0.3 quantity_oatmeal + 3 quantity_salmon + 0.2 quantity_spinach
Subject To
MaxCalories: 164 quantity_almonds + 95 quantity_apple + 105 quantity_banana
 + 216 quantity_brown_rice_cooked + 25 quantity_carrot
 + 284 quantity_chicken_breast + 130 quantity_greek_yogurt_plain_nonfat
 + 150 quantity_oatmeal + 175 quantity_salmon + 7 quantity_spinach <= 2000
MaxSugars: 1.2 quantity_almonds + 18.9 quantity_apple + 14.4 quantity_banana
 + 0.7 quantity_brown_rice_cooked + 2.9 quantity_carrot
 + 6 quantity_greek_yogurt_plain_nonfat + quantity_oatmeal
 + 0.1 quantity_spinach <= 20
MinCalories: 164 quantity_almonds + 95 quantity_apple + 105 quantity_banana
 + 216 quantity_brown_rice_cooked + 25 quantity_carrot
 + 284 quantity_chicken_breast + 130 quantity_greek_yogurt_plain_nonfat
 + 150 quantity_oatmeal + 175 quantity_salmon + 7 quantity_spinach >= 1000
MinFiber: 3.5 quantity_almonds + 4.4 quantity_apple + 3.1 quantity_banana
 + 3.5 quantity_brown_rice_cooked + 1.7 quantity_carrot + 4 quantity_oatmeal
 + 0.7 quantity_spinach >= 10
MinProtein: 6 quantity_almonds + 0.5 quantity_apple + 1.3 quantity_banana
 + 5 quantity_brown_rice_cooked + 0.6 quantity_carrot
 + 53.4 quantity_chicken_breast + 23 quantity_greek_yogurt_plain_nonfat
 + 5 quantity_oatmeal + 19.9 quantity_salmon + 0.9 quantity_spinach >= 140
MinVitaminC: 8.4 quantity_apple + 10.3 quantity_banana + 3.6 quantity_carrot
 + 8.4 quantity_spinach >= 1
Bounds
 0 <= quantity_almonds
 0 <= quantity_apple
 0 <= quantity_banana
 0 <= quantity_brown_rice_cooked
 0 <= quantity_carrot
 0 <= quantity_chicken_breast
 0 <= quantity_greek_yogurt_plain_nonfat
 0 <= quantity_oatmeal
 0 <= quantity_salmon
 0 <= quantity_spinach
Generals
quantity_almonds
quantity_apple
quantity_banana
quantity_brown_rice_cooked
quantity_carrot
quantity_chicken_breast
quantity_greek_yogurt_plain_nonfat
quantity_oatmeal
quantity_salmon
quantity_spinach
End
