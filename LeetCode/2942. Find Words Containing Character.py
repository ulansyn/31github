Python3
class Solution:
    def findWordsContaining(self, words: List[str], x: str) -> List[int]:
        arr = []
        for i, v in enumerate(words):
            if x in v:
                arr.append(i)
        return arr
