import pandas as pd


def read_student_records(filename):
    """
    Reads student records from an Excel file.
    """
    try:
        df = pd.read_excel(filename)

        required_columns = [
            "Roll No",
            "Name",
            "Marks in Subject 1",
            "Marks in Subject 2",
            "Marks in Subject 3",
            "Marks in Subject 4",
            "Marks in Subject 5"
        ]

        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing column: {col}")

        return df

    except FileNotFoundError:
        print("Error: File not found.")
        return None

    except Exception as e:
        print("Error:", e)
        return None


def assign_grade(percentage):

    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


def process_student_records(df):

    mark_columns = [
        "Marks in Subject 1",
        "Marks in Subject 2",
        "Marks in Subject 3",
        "Marks in Subject 4",
        "Marks in Subject 5"
    ]

    df["Total"] = df[mark_columns].sum(axis=1)
    df["Percentage"] = df["Total"] / 5
    df["Grade"] = df["Percentage"].apply(assign_grade)

    return df
