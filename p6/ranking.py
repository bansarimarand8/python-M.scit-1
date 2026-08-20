def rank_students(df):
    """
    Sort students by total marks and assign ranks.
    Handles tied ranks correctly.
    """

    df = df.sort_values(by="Total", ascending=False).reset_index(drop=True)

    ranks = []
    rank = 1

    for i in range(len(df)):
        if i == 0:
            ranks.append(rank)
        else:
            if df.loc[i, "Total"] == df.loc[i-1, "Total"]:
                ranks.append(ranks[-1])
            else:
                rank = i + 1
                ranks.append(rank)

    df["Rank"] = ranks

    return df
