import re
name = "sdaf - ./sdfsdf/ffffff"
spitresult = name.split(' - ')
spitresult[1] = re.split('./.*/',spitresult[1])

print(spitresult[1][1])