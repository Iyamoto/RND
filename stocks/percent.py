"""Financial strategy"""

import json
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
income_rate = 0.05  # 0.03 - Conservative, 0.05 - Normal, 0.07 - Aggressive

# Goals
goal = dict()

goal['fin_security'] = 10000  # For the flat
goal['fin_security'] += 30000  # For food
goal['fin_security'] += 10000  # For transportation

goal['style'] = goal['fin_security'] + 10000

goal['freedom'] = goal['style'] + 100000

achived = dict()
achived['fin_security'] = 0
achived['style'] = 0
achived['freedom'] = 0

print(json.dumps(goal, indent=4))

income = start
for i in range(30):
    income += income * income_rate + add
    income_per_month = round(income * income_rate / 12)

    for key in goal:
        if achived[key] == 0 and income_per_month >= goal[key]:
            achived[key] = i

print(json.dumps(achived, indent=4))
