KEY = '1'
asnswer = None

with open('keys.txt') as f:
    if '2' in f.read():
        print("true")
    else:
        print(False)