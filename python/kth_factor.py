class KthFactor:
    def kth_factor(self, n: int, k: int) -> int:
        # List to store all factors
        factors = []
        
        # Find all factors of n
        for i in range(1, n + 1):
            if n % i == 0:  # If i divides n evenly, it's a factor
                factors.append(i)
        
        # Check if k is greater than the number of factors
        if k > len(factors):
            return -1
        
        # Return the kth factor (k-1 because list is 0-indexed)
        return factors[k-1]
