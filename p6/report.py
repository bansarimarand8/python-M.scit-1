def display_report(df):

    print("\nSTUDENT RANK REPORT")
    print("-" * 95)

    print("{:<6} {:<20} {:<8} {:<12} {:<8} {:<6}".format(
        "Rank",
        "Name",
        "Roll",
        "Total",
        "Percent",
        "Grade"
    ))

    print("-" * 95)

    for _, row in df.iterrows():
        print("{:<6} {:<20} {:<8} {:<12} {:<8.2f} {:<6}".format(
            row["Rank"],
            row["Name"],
            row["Roll No"],
            row["Total"],
            row["Percentage"],
            row["Grade"]
        ))


def export_report(df, filename):

    try:
        df.to_excel(filename, index=False)
        print("\nReport exported successfully to", filename)

    except Exception as e:
        print("Error exporting file:", e)
