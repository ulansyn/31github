n = int(input())
cnt = 0
for i in range(n):
    x = input()
    cnt += 1 if '+' in x else -1
print(cnt)
