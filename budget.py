class Category():
  
  def __init__(self, name):
    self.name = name
    self.ledger = []
    self.balance = 0.0

  def check_funds(self, amount):
    if self.balance >= amount:
      return True
    else:
      return False
    
  def deposit(self, amount, description = ''):
    self.ledger.append({'amount':amount, 'description': description})
    self.balance += amount

  def withdraw(self, amount, description = ''):
    if self.check_funds(amount):
      self.ledger.append({'amount': -1 * amount,'description': description})
      self.balance -= amount
      return True
    else:
      return False

  def get_balance(self):
    return self.balance

  def transfer(self, amount, other_category):
    if self.check_funds(amount):
      self.withdraw(amount, description = f'Transfer to {other_category.name}')
      other_category.deposit(amount, description = f'Transfer from {self.name}')
      return True
    else:
      return False

  def __repr__(self): #for printing format
    top = self.name.center(30, '*')+'\n'
    body = ''
    for item in self.ledger:
      descrip = '{:<23}'.format(item['description'])
      cant = '{:>7.2f}'.format(item['amount'])
      body +="{}{}\n".format(descrip[:23], cant[:7])
    total = 'Total: {:.2f}'.format(self.balance)
    return top + body + total

def create_spend_chart(categories):
  negative_amounts = []
  for category in categories:
    spent = 0 #total spent for each category
    for item in category.ledger:
      if item['amount'] < 0:
        spent += abs(item['amount'])
    
    negative_amounts.append(round(spent,2))

  #Percentaje
  spent_percent = []
  total = round(sum(negative_amounts),2)
  for spent in negative_amounts:
    percen = int(spent * 100 // total)
    spent_percent.append(percen)

  #Bar chart
  top = 'Percentage spent by category \n'
  chart = '' #Draw the bars
  for x in reversed(range(0,101,10)):
    chart += str(x).rjust(3)+'|'
    for percen in spent_percent:
      if percen >= x:
        chart += ' o '
      else:
        chart += '   '
    chart += '\n'

  line = '    '+ '-' * (3*(len(categories)) + 1)+'\n'
  bottom = '   ' #Write name in columns
  max_str = 0
  for category in categories:
    if len(category.name) > max_str:
      max_str = len(category.name)
  for category in categories: #adjusting lenght
    category.name = category.name.ljust(max_str, ' ')
  for x in range(max_str):
    for category in categories:
      bottom += '  '+ category.name[x]
    bottom += '\n' + '   '

  return top + chart + line + bottom