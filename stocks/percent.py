"""Financial strategy"""

import json
from datetime import datetime
import configs.settings

# Add $ and rub

# How much to invest?
invest_rate = 0.25
add = configs.settings.MONTHLY_INCOME * 12 * invest_rate
print('Yearly investment:', add)

# Chose strategy
income_rate = 0.07  # 0.05 - Conservative, 0.07 - Normal, 0.09 - Aggressive
inflation = 0.04

# Prepare data
data = dict()
data['fin_security'] = dict()
data['fin_security']['achived'] = 0
data['style'] = dict()
data['style']['achived'] = 0
data['freedom'] = dict()
data['freedom']['achived'] = 0

# Goals
data['fin_security']['goal'] = 11000  # For the flat
data['fin_security']['goal'] += 40000  # For food
data['fin_security']['goal'] += 6000  # For transportation
data['fin_security']['goal'] += 2000  # For communications

data['style']['goal'] = data['fin_security']['goal']
data['style']['goal'] += 7000  # Fitness club
data['style']['goal'] += 20000  # Dressings
data['style']['goal'] += 25000  # Travels
data['style']['goal'] += 10000  # Restaurants, theaters
data['style']['goal'] += 10000  # Beauty

data['freedom']['goal'] = data['style']['goal']
data['freedom']['goal'] += 100000

today = datetime.today()
print('Now', today.year)
print(json.dumps(data, indent=4))

income = configs.settings.START_RUB
for i in range(1, 100):
    income += (income * income_rate + add) * (1 - inflation)
    income_per_month = round(income * income_rate / 12)

    for key in data:
        if not data[key]['achived']:
            data[key]['goal'] = round(data[key]['goal'] * (1 + inflation), 0)
            if income_per_month >= data[key]['goal']:
                data[key]['achived'] = i
                data[key]['age'] = today.year + i - configs.settings.BEARTH_YEAR
                data[key]['income'] = round(income, 0)

    if data['fin_security']['achived'] and data['style']['achived'] and data['freedom']['achived']:
        break

print('Future')
print(json.dumps(data, indent=4))
