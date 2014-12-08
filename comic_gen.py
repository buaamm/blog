import os
import sys


#param = sys.argv[1]
names = os.listdir(".")
for name in names:
    param = name
    if param[-1] == "/":
        param = param[:-1]
    if os.path.isdir(param) == False:
        continue
    L = os.listdir(param)
    L.sort()
    ans = "|".join(L)
    print "/static/examples/comic/" + param + "/|" + ans


