import re

print(re.findall(r'^/echo.(.*?)$', '/echo 12345678'))
