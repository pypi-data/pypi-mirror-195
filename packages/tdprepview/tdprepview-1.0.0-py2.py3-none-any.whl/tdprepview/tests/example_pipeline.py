from tdprepview.preprocessing import *

steps =[
    (["col1","col2"], Impute(kind="mean")),
    (["col3","col4"], Impute(kind="median")),
    (["col5","col6"], Impute(kind="custom", value= 3)),
    (["col7", "col8"], Impute(kind="mode")),

    (["varcharcol1", "varcharcol2"], ImputeText(kind="mode")),
    (["varcharcol3", "varcharcol4"], ImputeText(kind="custom", value="missing")),

    (["varcharcol5"], TryCast(new_type="FLOAT")), # TODO: maybe state requiirement that all trycastss must be on top, only custom SQL can be beforehand

    (["col1"], Scale(kind="minmax")),
    (["col2"], Scale(kind="zscore")),
    (["col3"], Scale(kind="robust")),
    (["col4"], Scale(kind="custom", numerator_subtr="mean", denominator="max-min"  )),
    (["col2"], Scale(kind="custom", numerator_subtr=-5, denominator=1/2 )), #STANINE
    (["col7"], Scale(kind="custom", numerator_subtr=0, denominator="P75-P25" )),

    (["col6"], CutOff(cutoff_min=0, cutoff_max=10 )),
    (["col8"], CutOff(cutoff_min="P5", cutoff_max="P95" )), #ausreiser

    (["varcharcol5"], FixedWidthBinning(n_bins = 10)), # TODO: check if statistics canalso be collected after conversion,  standard is "max" and "min"
    (["col5"], FixedWidthBinning(n_bins = 10, lower_bound = 2, upper_bound = 10)), # check upper > lower

    (["col9", "col10"], ThresholdBinarizer(threshold="mode")),
    (["col11", "col12"], ThresholdBinarizer(threshold="median")),
    ("col13", ThresholdBinarizer(threshold="P80")),
    ("col14", ThresholdBinarizer(threshold=34.5)),

    ("col14", ThresholdBinarizer(threshold=34.5)),

    ("varcharcol4", ListBinarizer(elements1=["red","green"])),
    ("varcharcol3", ListBinarizer(elements1="TOP5")), # top 5 most frequent elements
    ("varcharcol3", ListBinarizer(elements1="mode")),  # top 5 most frequent elements

    (["col3"], VariableWidthBinning(kind="quantiles", no_quantiles = 5)), #no_quantiles in 100, 50, 25, 10, 5, 4, 3, 2

    (["col15"], VariableWidthBinning(kind="custom", boundaries = [-5,0,10,50,500,100])),

("varcharcol7", LabelEncoder(elements=["tomato","potato","lettuce"])), # other will be 4
("varcharcol8", LabelEncoder(elements="TOP5")), # top 5 most frequent elements will get encoding, rest will be 6

    (["col29"], CustomTransformation(custom_str="POWER(%%COL%%, 3)")),
    (["col40"], CustomTransformation(custom_str="2* POWER(%%COL%%, 2) - 5 * %%COL%%  + 2")),
]
