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
income_rate = 5  # 3 - Conservative, 5 - Normal, 7 - Aggressive

# Goals
goal = dict()

goal['fin_security'] = 10000  # For the flat
goal['fin_security'] += 30000  # For food
goal['fin_security'] += 10000  # For transportation

goal['style'] = 10000

goal['freedom'] = 100000

achived = dict()
achived['fin_security'] = 0
achived['style'] = 0
achived['freedom'] = 0

print(json.dumps(goal, indent=4))

income = start
for i in range(30):
    income = income * (100 + income_rate) / 100 + add

    income_per_month = round(income * income_rate / (12 * 100))
    for key in goal:
        if achived['fin_security'] == 0 and income_per_month >= goal['fin_security']:
            achived['fin_security'] = i
        if achived['style'] == 0 and income_per_month >= (goal['style'] + goal['fin_security']):
            achived['style'] = i

print(json.dumps(achived, indent=4))
