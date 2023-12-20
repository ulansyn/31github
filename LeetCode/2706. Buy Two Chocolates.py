class Solution:
    def buyChoco(self, prices: List[int], money: int) -> int:
        prices.sort()
        if sum(prices[:2]) > money:
            return money
        return money - sum(prices[:2])
