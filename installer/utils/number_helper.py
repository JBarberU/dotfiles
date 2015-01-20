
def number_string_with_postfix(number):
  if number == 1:
    return "1st"
  elif number == 2:
    return "2nd"
  elif number == 3:
    return "3rd"
  else:
    return "%sth" % number

