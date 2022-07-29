def BadWordFilter(msg):
    # bad word filter
    ls = msg.split(' ')
    for o in BADWORDS:
        if o in ls:
            ls[ls.index(o)] = '*'*len(o)

    # Create new message
    msg = ''
    for o in ls:
        msg += o + ' '
    return msg

BADWORDS = ['bad']

while True:
    try:
        print(BadWordFilter(input()))
    except KeyboardInterrupt:
        exit()