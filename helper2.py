testString = "('ant', 'bee', 'cicada')"
final = list(map(lambda string: string.strip('\''), testString.strip('()').split(', ')))
print(final)