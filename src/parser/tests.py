from parser.utils import clean_price

assert clean_price("""0,00 р.""") == 0.0
assert clean_price("""0.00 р.""") == 0.0
assert clean_price("""0 р.""") == 0.0
assert clean_price("""0,99 р.""") == 0.99
assert clean_price("""0.99 р.""") == 0.99
assert clean_price("""0.90 р.""") == 0.9

assert clean_price("""399,00 р.""") == 399.0
assert clean_price("""399.00 р.""") == 399.0
assert clean_price("""399 р.""") == 399.0
assert clean_price("""3 999,99 р.""") == 3999.99
assert clean_price("""3 999.99 р""") == 3999.99

assert clean_price("""399,00р.""") == 399.0
assert clean_price("""399.00р.""") == 399.0
assert clean_price("""399р.""") == 399.0
assert clean_price("""3 999,99р.""") == 3999.99
assert clean_price("""3 999.99р.""") == 3999.99

assert clean_price("""399,00 $""") == 399.0
assert clean_price("""399.00 $""") == 399.0
assert clean_price("""399 $""") == 399.0
assert clean_price("""3 999,99 $""") == 3999.99
assert clean_price("""3 999.99 $""") == 3999.99

assert clean_price("""399,00$""") == 399.0
assert clean_price("""399.00$""") == 399.0
assert clean_price("""399$""") == 399.0
assert clean_price("""3 999,99$""") == 3999.99
assert clean_price("""3 999.99$""") == 3999.99
