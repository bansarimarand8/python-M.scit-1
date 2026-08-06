n = int(input("Enter value of N: "))

a = []

print("Enter", n - 1, "roll numbers:")
for i in range(n - 1):
    a.append(int(input()))

total = n * (n + 1) // 2
missing = total - sum(a)

print("Missing Roll Number:", missing)