# class Solution:
def generateParenthesis( n: int):  # -> list
    if n == 0: return []
    dp = [0  for _ in range(n + 1)]
    dp[0] = [""]
    for i in range(1, n+1):
        cur = []
        for j in range(i):
            left = dp[j]
            right = dp[i - j - 1]
            for s1 in left:
                for s2 in right:
                    cur.append("(" + s1 + ")" + s2)
        dp[i] = cur
    return dp[n]



if __name__ == '__main__':
    # new = Solution
    print(generateParenthesis(3))