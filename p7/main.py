
from datetime import datetime


class Course:
    def __init__(self, course_code, day, start_time, end_time):
        self.course_code = course_code
        self.day = day
        self.start_time = start_time
        self.end_time = end_time

        # Convert time into datetime objects for validation
        start = datetime.strptime(start_time, "%H:%M")
        end = datetime.strptime(end_time, "%H:%M")

        if start >= end:
            raise ValueError(
                "End time must be later than start time."
            )

    def __str__(self):
        return (
            f"{self.course_code} | {self.day} | "
            f"{self.start_time} - {self.end_time}"
        )


class Student:
    def __init__(self, student_id, student_name):
        self.student_id = student_id
        self.student_name = student_name
        self.registered_courses = []

    def add_course(self, course):
        self.registered_courses.append(course)

    def detect_conflicts(self):
        conflicts = []
        courses = self.registered_courses

        for i in range(len(courses)):
            for j in range(i + 1, len(courses)):
                c1 = courses[i]
                c2 = courses[j]

                if c1.day == c2.day:
                    start1 = datetime.strptime(
                        c1.start_time, "%H:%M"
                    )
                    end1 = datetime.strptime(
                        c1.end_time, "%H:%M"
                    )
                    start2 = datetime.strptime(
                        c2.start_time, "%H:%M"
                    )
                    end2 = datetime.strptime(
                        c2.end_time, "%H:%M"
                    )

                    # Courses conflict if their time intervals overlap
                    if start1 < end2 and start2 < end1:
                        conflicts.append((c1, c2))

        return conflicts

    def __str__(self):
        return (
            f"Student ID: {self.student_id}\n"
            f"Student Name: {self.student_name}\n"
            f"Total Registered Courses: "
            f"{len(self.registered_courses)}"
        )

    def display_timetable(self):
        print("\nTimetable:")

        sorted_courses = sorted(
            self.registered_courses,
            key=lambda c: (
                ["Monday", "Tuesday", "Wednesday",
                 "Thursday", "Friday", "Saturday",
                 "Sunday"].index(c.day),
                c.start_time
            )
        )

        for course in sorted_courses:
            print(course)


def main():
    students = []

    try:
        n = int(input("Enter number of students: "))

        if n <= 0:
            raise ValueError("Number of students must be positive.")

        for i in range(n):
            print(f"\n--- Student {i + 1} ---")

            student_id = input("Enter Student ID: ").strip()
            student_name = input("Enter Student Name: ").strip()

            if not student_id or not student_name:
                raise ValueError(
                    "Student ID and name cannot be empty."
                )

            student = Student(student_id, student_name)

            number_of_courses = int(
                input("Enter number of registered courses: ")
            )

            if number_of_courses < 0:
                raise ValueError(
                    "Number of courses cannot be negative."
                )

            for j in range(number_of_courses):
                print(f"\nCourse {j + 1}")

                course_code = input("Enter Course Code: ").strip()
                day = input(
                    "Enter Day (Monday-Sunday): "
                ).strip().title()

                valid_days = [
                    "Monday", "Tuesday", "Wednesday",
                    "Thursday", "Friday", "Saturday", "Sunday"
                ]

                if day not in valid_days:
                    raise ValueError("Invalid day of the week.")

                start_time = input(
                    "Enter Start Time (HH:MM, 24-hour format): "
                ).strip()

                end_time = input(
                    "Enter End Time (HH:MM, 24-hour format): "
                ).strip()

                course = Course(
                    course_code, day, start_time, end_time
                )
                student.add_course(course)

            students.append(student)

        # Display results for every student
        for student in students:
            print("\n" + "=" * 40)
            print(student)

            conflicts = student.detect_conflicts()

            if conflicts:
                print("\nTimetable Conflicts Found:")

                for c1, c2 in conflicts:
                    print(f"Conflict: {c1.course_code} <-> "
                          f"{c2.course_code}")
                    print(f"  {c1}")
                    print(f"  {c2}")
            else:
                print("\nNo timetable conflicts found.")
                student.display_timetable()

            print(
                f"\nTotal Courses: "
                f"{len(student.registered_courses)}"
            )

    except ValueError as e:
        print(f"\nInput Error: {e}")
    except Exception as e:
        print(f"\nUnexpected Error: {e}")


if __name__ == "__main__":
    main()
