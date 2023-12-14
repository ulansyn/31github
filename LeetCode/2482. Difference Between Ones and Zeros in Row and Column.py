class Solution:
    def onesMinusZeros(self, A: List[List[int]]) -> List[List[int]]:
        onesRow, onesCol, zerosRow, zerosCol = [], [], [], []
        for i in range(len(A)):
            ones, zeros = 0, 0
            for j in range(len(A[0])):
                if A[i][j]:
                    ones += 1
                else:
                    zeros += 1
            onesRow.append(ones)
            zerosRow.append(zeros)

        for i in range(len(A[0])):
            ones, zeros = 0, 0
            for j in range(len(A)):
                if A[j][i]:
                    ones += 1
                else:
                    zeros += 1
            onesCol.append(ones)
            zerosCol.append(zeros)
        diff = [[None for i in range(len(A[0]))] for j in range(len(A))]
        for i in range(len(A)):
            for j in range(len(A[0])):
                diff[i][j] = (onesRow[i] + onesCol[j] - zerosRow[i] - zerosCol[j])
        return diff
        
