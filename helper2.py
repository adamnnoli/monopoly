testString = "('Vermont Avenue',)"
testString2 = "('ant', 'bee', 'cicada', 'dung beetle')"

def fixer(messyString):
  result = []
  for entry in messyString.strip('()').split(','):
    fixed = entry.strip(' ').strip('\'')
    if fixed != '':
      result.append(fixed)
  return result

print(fixer(testString))
print(fixer(testString2)) 