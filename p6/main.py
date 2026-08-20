from student import read_student_records, process_student_records
from ranking import rank_students
from report import display_report, export_report


def main():

    input_file = "input.xlsx"
    output_file = "ranked_students.xlsx"

    try:
        students = read_student_records(input_file)

        if students is None:
            return

        students = process_student_records(students)

        students = rank_students(students)

        display_report(students)

        export_report(students, output_file)

    except Exception as e:
        print("Unexpected Error:", e)


if __name__ == "__main__":
    main()
