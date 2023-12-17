class Solution:
    def findMissingAndRepeatedValues(self, A: List[List[int]]) -> List[int]:
        arr = [0 for i in range(len(A) ** 2)]
        ans = []
        for i in range(len(A)):
            for j in range(len(A)):
                if arr[A[i][j] - 1] == 0:
                    arr[A[i][j] - 1] = A[i][j]
                else:
                    ans.append(A[i][j])
        for i, v in enumerate(arr):
            if v == 0:
                ans.append(i + 1)
        return ans
