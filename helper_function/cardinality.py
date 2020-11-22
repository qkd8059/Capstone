def cardinality (principal):
  if principal <= 10000:
    card = 10
  elif principal > 10000 and principal <= 100000:
    card = 15
  else: card = 20
  return card
