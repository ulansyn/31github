n = int(input())
arr = sum(list(map(int, input().split())))
sm = (n * (n + 1))//2
print((sm - arr))
