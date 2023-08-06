import teradataml as tdml
from string import Template
from .statistics import collector
from .preprocessing._preprocessing import Preprocessor

import os

current_directory = os.path.dirname(os.path.abspath(__file__))
#print(current_directory)

SQL_TEMPLATE_NESTED_FROM = os.path.join(current_directory, "sql/templates/from.sql")
SQL_TEMPLATE_NESTED_WITHAS = os.path.join(current_directory, "sql/templates/withas.sql")
SQL_TEMPLATE_REPLACE_VIEW = os.path.join(current_directory, "sql/templates/replaceview.sql")


class Pipeline:
    """
    A class for chaining multiple preprocessing steps together.
    
    The Pipeline class is used for chaining multiple preprocessing steps together. It takes a list of tuples, where 
    each tuple contains a list of column names and a Preprocessor object that applies a transformation to those columns.

    Parameters
    ----------
    steps : list of tuples
        List of preprocessing steps to apply, where each tuple contains a list of column names and a
        `Preprocessor` object that applies a transformation to those columns.

    Attributes
    ----------
    steps : list of tuples
        List of column names and corresponding `Preprocessor` objects.
    statistics_num : None
        Placeholder for numeric column statistics computed during fitting.
    statistics_varchar : None
        Placeholder for string column statistics computed during fitting.
    colwise_processing : dict
        Mapping of column names to corresponding preprocessing steps.

    Notes
    -----
    The `Pipeline` class can be fitted to data in Vantage using the `fit` method. Once
    fitted, the `transform` method can be used to apply the entire pipeline to a new teradata.DataFrame.

    Examples
    --------
    >>> from tdprepview import Impute, Scale
    >>> from tdprepview import Pipeline
    >>> # Define a pipeline with two steps
    >>> steps = [
    ...     (['age', 'income'], Impute(kind="mean")),
    ...     (['age', 'income'], Scale(kind="minmax"))
    ... ]
    >>> pipeline = Pipeline(steps=steps)
    """

    def __init__(self, steps):
        assert isinstance(steps, list)

        new_steps = []
        for i, step in enumerate(steps):
            assert isinstance(step, tuple)
            assert len(step) == 2
            assert isinstance(step[1], Preprocessor)
            col_list = step[0]
            if isinstance(col_list, str):
                col_list = [col_list]
            else:
                assert isinstance(col_list, list)
            assert all([isinstance(col, str) for col in col_list])
            new_steps.append((col_list, step[1]))

        self.steps = new_steps

        self.statistics_num = None
        self.statistics_varchar = None

        self.colwise_processing = self._parse_pipeline_columnwise()

        self._is_fitted = False
        self._fit_df = None

    def fit(self, DF: tdml.DataFrame = None, schema_name: str = None, table_name: str = None):
        """Fits the pipeline on the provided DataFrame and calculates necessary statistics for each column.

        If statistics are required for any of the steps, a DataFrame needs to be provided for fitting. Then it also
        requires a database connection (Context) that can be retrieved with `tdml.get_context()`

        Parameters
        ----------
        DF : tdml.DataFrame, optional
            The input data to fit the transformers on. This can be provided either as a DataFrame object or by
            specifying the schema and table names to read from the database. Can be ommited if none of the
            `Preprocessor`s require a statistic
        schema_name : str, optional
            The schema name to read the input data from. This is required if `DF` is not provided and if statistics
            need to be calculated.
        table_name : str, optional
            The table/view name to read the input data from. This is required if `DF` is not provided and if statistics
            need to be calculated.

        Raises
        ------
        AssertionError
            If statistics are needed and no DataFrame is provided, or if no DB connection exists.

        Returns
        -------
        None

        Examples
        --------
        # fitting without data
        steps = [
           (['age', 'income'], Impute(kind="custom", value = 3)),
           (['age', 'income'], CutOff(cutoff_min=0))
           ]
        pipeline = Pipeline(steps=steps)
        pipeline.fit()
        
        # fitting with data as tdml.DataFrame
        steps = [
          (['age', 'income'], Impute(kind="mean")),
          (['age', 'income'], Scale(kind="minmax"))
           ]
        DF_train = tdml.DataFrame(tdml.in_schema("datalab", "train_data"))
        pipeline = Pipeline(steps=steps)
        pipeline.fit(DF_train)
        
        #alternatively, with data in table/view
        steps = [
          (['age', 'income'], Impute(kind="mean")),
          (['age', 'income'], Scale(kind="minmax"))
           ]
        pipeline = Pipeline(steps=steps)
        pipeline.fit(schema_name = "datalab", table_name = "train_data")
        """

        # AKA calculate_statistics

        # 1. collect necessary statistics for every column.
        stats_dict = {}  # col -> set of statistics
        statistics_needed = False
        for step in self.steps:
            cols = step[0]
            preprocesor = step[1]
            stats = preprocesor.necessary_statistics

            if len(stats) > 0:
                # when statistics are needed, a dataframe needs to be provided for fitting
                statistics_needed = True

            for c in cols:
                if c not in stats_dict:
                    stats_dict[c] = []

                stats_dict[c] += stats

        if statistics_needed:
            # existing DB connection necessary
            assert tdml.get_context() is not None
            assert not ((DF is None) and ((schema_name is None) or (table_name is None)))
        else:
            # no statistics need to be collected: only manually set values are used
            self._is_fitted = True
            return

        if (DF is None):
            DF = tdml.DataFrame(tdml.in_schema(schema_name, table_name))

        # 3. get statistics for different column types
        # start with numeric columns
        cols_standard = [
            c for c, stats in stats_dict.items() if (
                    ("standard" in stats) and all([x == "standard" for x in stats])
            )]
        cols_median_percentile = [
            c for c, stats in stats_dict.items() if (
                    ("median" in stats) or
                    (any(x[0] == "P" for x in stats if isinstance(x, tuple)))
            )]

        centiles = []
        for c, stats in stats_dict.items():
            for s in stats:
                if (isinstance(s, tuple) & (s[0] == "P")):
                    centiles.append(s[1])
        centiles = sorted(list(set(centiles)))

        # varchar_column
        col_maxtop_dict = {}
        for c, stats in stats_dict.items():
            if any([isinstance(x, tuple) & (x[0] == "TOP") for x in stats]):
                tops = [x[1] for x in stats if isinstance(x, tuple) & (x[0] == "TOP")]
                maxtop = max(tops)
                col_maxtop_dict[c] = maxtop

        self.statistics_num = collector.get_numeric_statistics(DF, cols_standard, cols_median_percentile, centiles)
        self.statistics_varchar = collector.get_varchar_statistics(DF, col_maxtop_dict)

        self._is_fitted = True
        DF._DataFrame__execute_node_and_set_table_name(DF._nodeid, DF._metaexpr)
        view_name = DF._table_name
        self._fit_df = view_name

        #print(stats_dict)

    def transform(self,
                  DF=None,
                  schema_name=None, table_name=None,
                  return_type="df",
                  create_replace_view=False,
                  output_schema_name=None,
                  output_view_name=None,
                  use_with_as=True
                  ):
        """Apply transformation to the input DataFrame or specified table and schema, and return results in specified format.

        Teradataml DataFrame are evaluated in a lazy fashion. Hence, no data is actually transformed until the returned
        DataFrame or View is called!

        Parameters
        ----------
        DF : tdml.DataFrame, optional
            Input DataFrame to apply the transformation. Should be directly based on an existing View/Table
        schema_name : str, optional
            The schema name of the table to apply the transformation. Ignored if `DF` provided
        table_name : str, optional
            The table name to apply the transformation. Ignored if `DF` provided
        return_type : str, optional
            Format of the return value. Valid options are "df" (tdml.DataFrame), "str" (query as str), or None.
            Defaults to "df".
        create_replace_view : bool, optional
            Whether to create a view with the results of the transformation. Defaults to False.
        output_schema_name : str, optional
            The schema name of the output view if `create_replace_view` is True.
        output_view_name : str, optional
            The view name of the output view if `create_replace_view` is True.
        use_with_as : bool, optional
            Whether to use the WITH AS clause in the generated SQL query. Otherwise nested FROM subqueries are used.
            Defaults to True.

        Raises
        ------
        AssertionError
            If input arguments do not satisfy the expected format or types.

        Examples
        --------
        # Apply transformation to DataFrame
        DF_score_tf = pipeline.transform(DF_score)

        # Create View with transformed data
        pipeline.transform(DF_score, return_type = None, create_replace_view = True,
               output_schema_name="datalab", output_view_name = "data_score_transf")
        DF_score_tf = tdml.DataFrame(tdml.in_schema("datalab", "data_score_transf")

        # return only query
        sql =  transform(DF_score, return_type = "str")
        print(sql)
        DF_score_tf = tdml.DataFrame.from_query(sql)

        """
        # argument checking
        if DF is not None:
            assert isinstance(DF, tdml.DataFrame)
            DF._DataFrame__execute_node_and_set_table_name(DF._nodeid, DF._metaexpr)
            view_name = DF._table_name
            # remove leading and trailing `"` to allow concatenation
            schema_name, table_name = [vn.replace('"', '') for vn in view_name.split(".")]
        else:
            assert isinstance(schema_name, str) and isinstance(table_name, str)

        assert return_type in ["df", "str", None]

        if create_replace_view is True:
            assert isinstance(output_schema_name, str) and isinstance(output_view_name, str)

        DbCon = tdml.get_context()
        if (create_replace_view is True) or (return_type == "df"):
            assert DbCon is not None

        # get query
        query = self.generate_query(schema_name, table_name,
                                    minimize_n_subqueries=True,  # to ensure Parser can handle query
                                    single_view_obj=True,
                                    use_with_as=use_with_as,  # only relevant if single single_view_obj is true
                                    )

        if create_replace_view is True:
            assert isinstance(output_schema_name, str) and isinstance(output_view_name, str)
            with open(SQL_TEMPLATE_REPLACE_VIEW, "r", encoding="utf-8") as sql_file:
                strSqlTemplate = sql_file.read()
            objSqlTemplate = Template(strSqlTemplate)
            pdicMapping = {
                "output_schema_name": output_schema_name,
                "output_view_name": output_view_name,
                "select_query": query
            }
            final_sql = objSqlTemplate.substitute(pdicMapping)
            with DbCon.connect() as conn:
                #print(final_sql)
                #print("-------")
                conn.execute(final_sql)
                #print(f"VIEW {output_schema_name}.{output_view_name} created.")

        if return_type == "str":
            return query
        elif return_type == "df":
            if create_replace_view is True:
                DF_ret = tdml.DataFrame(tdml.in_schema(output_schema_name, output_view_name))
            else:
                #print(query)
                DF_ret = tdml.DataFrame.from_query(query)
            return DF_ret
        else:  # also in case of None
            return

    # "str", None
    def _parse_pipeline_columnwise(self):
        colwise_processing = {}
        for step in self.steps:
            cols = step[0]
            preprocessor = step[1]
            for c in cols:
                if c not in colwise_processing:
                    colwise_processing[c] = []
                colwise_processing[c].append(preprocessor)
        return colwise_processing

    def _get_final_cols(self, minimize_n_subqueries, col_names):
        # Squeeze or not squeeze processing into subqueries
        final_cols = {c: [] for c in col_names}
        # final_cols has as many entries as there are columns, and every value is a list with as many str as elements as there are maximum subqueries
        if minimize_n_subqueries:
            max_no_subqueries = 1
            for col in col_names:
                if col not in (self.colwise_processing.keys()):
                    # columns that were not present during fitting or without transformation
                    final_cols[col] = [col]
                else:
                    sql_cols = []
                    previous_str = col
                    for p in self.colwise_processing[col]:
                        if p.needs_subquery() and (previous_str != col):
                            sql_cols += [previous_str]
                            previous_str = col
                        previous_str = p.generate_sql_column(previous_str, col, self.statistics_num,
                                                             self.statistics_varchar)
                    sql_cols += [previous_str]
                    max_no_subqueries = max(max_no_subqueries, len(sql_cols))
                    final_cols[col] = sql_cols

            # fill up difference to maximal number of subqueries
            for col, sql_cols in final_cols.items():
                n_sql_cols = len(sql_cols)
                if n_sql_cols < max_no_subqueries:
                    final_cols[col] += [col] * (max_no_subqueries - n_sql_cols)

        else:
            # 1 query per pipeline step for all column
            max_no_subqueries = 0
            for step in self.steps:
                cols = step[0]
                preprocessor = step[1]
                # if column not in step --> just forward column name
                unchangend_cols = list(set(col_names) - set(cols))
                changed_cols = list(set(col_names).intersection(set(cols)))
                if len(changed_cols) == 0:
                    # skip iteration as no column affected
                    continue
                max_no_subqueries += 1
                for u_col in unchangend_cols:
                    final_cols[u_col] += [u_col]

                for col in changed_cols:
                    final_cols[col] += [preprocessor.generate_sql_column(col, col,
                                                                         self.statistics_num,
                                                                         self.statistics_varchar)]

        return final_cols, max_no_subqueries

    def generate_query(self, schema_name, table_name,
                       minimize_n_subqueries=True,
                       single_view_obj=True,
                       use_with_as=False,  # only relevant if single single_view_obj is true,
                       manual_column_names=None
                       ):
        if (schema_name is None) or (table_name is None):
            assert manual_column_names is not None
            col_names = manual_column_names
        else:
            #print(schema_name, table_name)
            col_names = tdml.DataFrame(tdml.in_schema(schema_name, table_name)).columns

        assert (single_view_obj), "only one view currently supported"

        final_cols, max_no_subqueries = self._get_final_cols(minimize_n_subqueries, col_names)

        def get_single_view_sql():

            final_sql_text = ""

            if not use_with_as:

                with open(SQL_TEMPLATE_NESTED_FROM, "r", encoding="utf-8") as sql_file:
                    strSqlTemplate = sql_file.read()
                objSqlTemplate = Template(strSqlTemplate)

                table_view_query = "%%%BASE_SCHEMA_NAME%%%.%%%BASE_TABLE_VIEW_NAME%%%"
                new_sql = ""

                def get_sql_col_description(col, this_i):
                    val_from_dict = final_cols[col][this_i]
                    if val_from_dict == col:
                        return col
                    else:
                        return val_from_dict + " AS " + col

                for i in range(max_no_subqueries):
                    column_definitions = "    " + ",\n    ".join([get_sql_col_description(col, i) for col in col_names])

                    pdicMapping = {
                        "column_definitions": column_definitions,
                        "table_view_query": table_view_query
                    }

                    new_sql = objSqlTemplate.substitute(pdicMapping)
                    if i < max_no_subqueries - 1:
                        new_sql = "    " + new_sql.replace("\n", "\n    ")
                    # after updating changing template --> recursive step
                    table_view_query = "( " + new_sql + " )"

                final_sql_text = new_sql

            else:
                # use with as

                with open(SQL_TEMPLATE_NESTED_FROM, "r", encoding="utf-8") as sql_file:
                    strSqlTemplate = sql_file.read()
                objSqlTemplate = Template(strSqlTemplate)

                with open(SQL_TEMPLATE_NESTED_WITHAS, "r", encoding="utf-8") as sql_file:
                    strSqlTemplate_withAs = sql_file.read()
                strSqlTemplate_withAs = Template(strSqlTemplate_withAs)

                table_view = "%%%BASE_SCHEMA_NAME%%%.%%%BASE_TABLE_VIEW_NAME%%%"
                with_as_queries = []

                def get_sql_col_description(col, this_i):
                    val_from_dict = final_cols[col][this_i]
                    if val_from_dict == col:
                        return col
                    else:
                        return val_from_dict + " AS " + col

                for i in range(max_no_subqueries):
                    column_definitions = "        " + ",\n        ".join(
                        [get_sql_col_description(col, i) for col in col_names])

                    new_view_name = f"%%%BASE_TABLE_VIEW_NAME%%%__preprocessing_step_{i + 1}"
                    pdicMapping = {
                        "intermediate_name": f"%%%BASE_TABLE_VIEW_NAME%%%__preprocessing_step_{i + 1}",
                        "column_definitions": column_definitions,
                        "table_view": table_view
                    }

                    new_sql = strSqlTemplate_withAs.substitute(pdicMapping)
                    with_as_queries.append(new_sql)

                    # chaining with "with as"
                    table_view = new_view_name

                with_as_queries = "WITH " + ",\n\n".join(with_as_queries)

                # final step, no with as
                pdicMapping = {
                    "column_definitions": "*",
                    "table_view_query": table_view
                }
                final_sql = objSqlTemplate.substitute(pdicMapping)
                final_sql_text = "\n\n".join([with_as_queries, final_sql])

            return final_sql_text

            # subqueries are

        if single_view_obj:
            single_view_qu = get_single_view_sql()
            if (schema_name is not None) and (table_name is not None):
                single_view_qu = (single_view_qu
                                  .replace("%%%BASE_SCHEMA_NAME%%%", schema_name)
                                  .replace("%%%BASE_TABLE_VIEW_NAME%%%", table_name))
            return single_view_qu
