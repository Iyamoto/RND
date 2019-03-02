"""Financial strategy"""

import json
from datetime import datetime
import configs.settings

# Add $ and rub
# Add inflation

# Initial state
start = configs.settings.START_RUB

# How much to invest?
invest_rate = 0.25
add = configs.settings.MONTHLY_INCOME * 12 * invest_rate
print('Yearly investment:', add)

# Chose strategy
income_rate = 0.08  # 0.05 - Conservative, 0.07 - Normal, 0.09 - Aggressive
inflation = 0.05

# Goals
goal = dict()

goal['fin_security'] = 11000  # For the flat
goal['fin_security'] += 40000  # For food
goal['fin_security'] += 6000  # For transportation
goal['fin_security'] += 2000  # For communications

goal['style'] = goal['fin_security']
goal['style'] += 7000  # Fitness club
goal['style'] += 20000  # Dressings
goal['style'] += 25000  # Travels
goal['style'] += 10000  # Restaurants, theaters
goal['style'] += 10000  # Beauty

goal['freedom'] = goal['style']

achived = dict()
achived['fin_security'] = 0
achived['style'] = 0
achived['freedom'] = 0

age = dict()

print(json.dumps(goal, indent=4))

today = datetime.today()
print('Now', today.year)

income = start
for i in range(1, 100):
    income += (income * income_rate + add) * (1 - inflation)
    income_per_month = round(income * income_rate / 12)

    for key in goal:
        goal[key] = goal[key] * (1 + inflation)
        if achived[key] == 0 and income_per_month >= goal[key]:
            achived[key] = i
            age[key] = today.year + i - configs.settings.BEARTH_YEAR

print(json.dumps(achived, indent=4))
print(json.dumps(age, indent=4))
