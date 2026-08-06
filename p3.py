password = input("Enter Password: ")

has_upper = False
has_lower = False
has_digit = False
has_special = False
consecutive = False

special = "!@#$%^&*()_+-=[]{}|;:',.<>?/"

for i in range(len(password)):
    if password[i].isupper():
        has_upper = True
    if password[i].islower():
        has_lower = True
    if password[i].isdigit():
        has_digit = True
    if password[i] in special:
        has_special = True

    if i < len(password) - 1:
        if password[i] == password[i + 1]:
            consecutive = True

print("\nFailed Rules:")

if not has_upper:
    print("- Missing Uppercase Letter")

if not has_lower:
    print("- Missing Lowercase Letter")

if not has_digit:
    print("- Missing Digit")

if not has_special:
    print("- Missing Special Character")

if consecutive:
    print("- Repeated Consecutive Characters Found")

if has_upper and has_lower and has_digit and has_special and not consecutive:
    print("Password is Strong")