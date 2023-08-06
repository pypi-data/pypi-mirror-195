import tdprepview

def test_simple():
    steps = [
        (["col5", "col6"], Impute(kind="custom", value=3)),
        (["varcharcol3", "varcharcol4"], ImputeText(kind="custom", value="missing")),
        (["varcharcol5"], TryCast(new_type="FLOAT")),
        (["col2"], Scale(kind="custom", numerator_subtr=-5, denominator=1 / 2)),  # STANINE
        (["col6"], CutOff(cutoff_min=0, cutoff_max=10)),
        (["col5"], FixedWidthBinning(n_bins=10, lower_bound=2, upper_bound=10)),  # check upper > lower
        (["col14"], ThresholdBinarizer(threshold=34.5)),
        (["varcharcol4"], ListBinarizer(elements1=["red", "green"])),
        (["col15"], VariableWidthBinning(kind="custom", boundaries=[-5, 0, 10, 50, 500, 100])),
        (["varcharcol7"], LabelEncoder(elements=["tomato", "potato", "lettuce"])),  # other will be 4
        (["col29"], CustomTransformer(custom_str="POWER(%%COL%%, 3)")),
        (["col40"], CustomTransformer(custom_str="2* POWER(%%COL%%, 2) - 5 * %%COL%%  + 2")),
    ]

    pipeline = Pipeline(steps)
    pipeline.fit(DF=None)
    query = pipeline.generate_query(schema_name = None, table_name = None,
                   minimize_n_subqueries=True,
                   single_view_obj=True,
                   use_with_as=False,  # only relevant if single single_view_obj is true,
                   manual_column_names=["col5", "col6", "varcharcol3", "varcharcol4",
                                        "col14", "col15", "varcharcol7",
                                        "col2", "col29", "col40"])
    #print(query)


if __name__ == '__main__':
    test_simple()
