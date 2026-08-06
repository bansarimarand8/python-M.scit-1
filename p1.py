n = int(input("Enter number of elements: "))

a = []

print("Enter elements:")
for i in range(n):
    a.append(int(input()))

print("Consecutive duplicate numbers:")

for i in range(n - 1):
    if a[i] == a[i + 1]:
        if i == 0 or a[i] != a[i - 1]:
            print(a[i])