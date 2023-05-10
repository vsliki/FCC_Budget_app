class Category():
  # --------------------- BUDGET --------------------

  def __init__(self, description):
    self.name = description
    self.ledger = list()
    self.balance = float(0)

  # ------------ PRINT BUDGET ---------------
  def __repr__(self):
    title = self.name.center(30, "*") + "\n"
    exp = ""

    for i in range(len(self.ledger)):
      desc = "{:<23}".format(str(self.ledger[i]["description"]))
      amo = "{:>7.2f}".format(self.ledger[i]["amount"])

      exp += "{}{}\n".format(desc[:23], amo[:7])

    bal = "Total: {:2}".format(self.get_balance())

    return title + exp + bal

  # --------- deposit method -----------
  def deposit(self, amount, description=""):
    self.ledger.append({"amount": float(amount), "description": description})
    self.balance += float(amount)

  # --------- withdraw method ----------
  def withdraw(self, new_amount, new_description=""):
    #print(self.ledger[0]["amount"])
    if self.balance - float(new_amount) >= 0:
      self.ledger.append({
        "amount": float(-new_amount),
        "description": new_description
      })
      self.balance -= float(new_amount)
      return True
    else:
      return False

    self.check_funds(new_amount)

  # --------- get_balance method --------
  def get_balance(self):
    return self.balance

  # --------- transfer method ------------
  def transfer(self, an_amount, budget_category):
    self.withdraw(an_amount, "Transfer to " + str(budget_category.name))
    budget_category.deposit(an_amount, "Transfer from " + str(self.name))

    self.check_funds(an_amount)

  # --------- check_funds method -----------
  def check_funds(self, amount):
    if amount > self.balance:
      return False
    else:
      return True


# --------------------- SPEND CHART -----------------


def create_spend_chart(categories):
  #amount spent in each category
  cat_amount = []
  for cat in categories:
    new_amount = 0
    for i in cat.ledger:
      if i["amount"] < 0:
        new_amount -= i["amount"]
    cat_amount.append(round(new_amount, 2))
  #print("total spent in each category: ")
  #print(cat_amount)
  # -----------------------------------------

  #compute % spent for each cat:
  total_spent = sum(cat_amount)
  #print("total expenses: ")
  #print(total_spent)

  perc_per_cat = []
  for cat in range(len(categories)):
    perc_per_cat.append(round(cat_amount[cat] / total_spent * 100, 2))
  #print("percentage spent per category: ")
  #print(perc_per_cat)
  # --------------------------------------------
  title = "Percentage spent by category \n"
  bar_chart = title

  #yaxis from 0 to 100
  yaxis = list(range(0, 101, 10))[::-1]

  # add percentage as "o"
  for unit in yaxis:
    bar_chart += str(unit).rjust(3) + "|"
    for val in perc_per_cat:
      if unit <= val:
        bar_chart += " o "
    bar_chart += "\n"

    #line to split x axis
  line = "    " + "-" * (len(categories) * 3 + 1) + "\n"
  bar_chart += line
  #print(bar_chart)

  # x axis
  desc = []
  for cat in categories:
    desc.append(cat.name)

  # longest word
  leng = []
  for words in desc:
    leng.append(len(words))
  maxlen = max(leng)

  xaxis = ""
  new_desc = []
  # words with all length max
  for word in desc:
    while len(word) <= maxlen:
      word += " "
    new_desc.append(word)

  # set vertically the words next to each other
  for word_letter in zip(*new_desc):
    xaxis += "    " + "".join(map(lambda w: w.center(3), word_letter)) + " \n"

  # complete bar chart
  bar_chart += xaxis
  print(bar_chart)

  return bar_chart
