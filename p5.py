# Student Rank Processing Engine

students = []

# Number of students
n = int(input("Enter the number of students: "))

if n != 5:
    print("Error: Only 5 students are allowed.")
    exit()

# Input student details
for i in range(n):
    print(f"\nEnter details of Student {i + 1}")

    roll = input("Roll No: ")
    name = input("Name: ")

    marks = []
    for j in range(5):
        mark = float(input(f"Enter marks of Subject {j + 1}: "))
        marks.append(mark)

    total = sum(marks)
    percentage = total / 5

    # Grade Assignment
    if percentage >= 90:
        grade = "A+"
    elif percentage >= 80:
        grade = "A"
    elif percentage >= 70:
        grade = "B"
    elif percentage >= 60:
        grade = "C"
    elif percentage >= 50:
        grade = "D"
    else:
        grade = "F"

    students.append({
        "roll": roll,
        "name": name,
        "marks": marks,
        "total": total,
        "percentage": percentage,
        "grade": grade
    })

# Sort students by total marks (descending)
students.sort(key=lambda x: x["total"], reverse=True)

# Rank Assignment (Handles Ties)
rank = 1
for i in range(len(students)):
    if i == 0:
        students[i]["rank"] = rank
    else:
        if students[i]["total"] == students[i - 1]["total"]:
            students[i]["rank"] = students[i - 1]["rank"]
        else:
            rank = i + 1
            students[i]["rank"] = rank

# Display Results
print("\n" + "=" * 80)
print(f"{'Rank':<6}{'Roll':<10}{'Name':<20}{'Total':<10}{'%':<10}{'Grade':<8}")
print("=" * 80)

for s in students:
    print(f"{s['rank']:<6}{s['roll']:<10}{s['name']:<20}{s['total']:<10.2f}{s['percentage']:<10.2f}{s['grade']:<8}")

print("=" * 80)