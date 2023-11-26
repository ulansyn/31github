# python3
class Solution:
    def generateMatrix(self, n):
        arr = [[0] * n for i in range(n)]
        k = 1
        for i in range((n + 1) // 2):
            for j in range(i, n - i):
                arr[i][j], k = k, k + 1
            for j in range(i + 1, n - i):
                arr[j][~i], k = k, k + 1
            for j in range(i + 1, n - i):
                arr[~i][~j], k = k, k + 1
            for j in range(i + 1, n + ~i):
                arr[~j][i], k = k, k + 1
        return arr
