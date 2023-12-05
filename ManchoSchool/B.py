s = input()
mx = 0
prev = s[0]
cnt = 0
if len(s) == 1:
    print(1)
else:
    for i in range(len(s)):
        if s[i] == prev:
            cnt += 1
            mx = max(cnt, mx)
        else:
            mx = max(cnt, mx)
            cnt = 1
            prev = s[i]
    print(mx)
