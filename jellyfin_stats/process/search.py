import re
import pandas as pd
from jellyfin_stats.common import DEBUG

class SearchExpr():
    REGEX = r"^(?P<data>base|streams)\.(?P<column>[^=]+)(?P<operator>==|>|<|!=|<=|>=)(?P<value>.*)$"
    def __init__(self, expr):
        match = re.match(self.REGEX, expr)
        if not match:
            raise ValueError(f"Expr {expr} is invalid.")

        self.data = match.group('data')
        self.column = match.group('column')
        self.operator = match.group('operator')
        self.value = match.group('value')


    def apply(self, data):
        if self.data == 'base':
            data.df = self.apply_to_df(data.df)
            return data
        elif self.data == 'streams':
            data.df_streams = self.apply_to_df(data.df_streams)
            return data
        else:
            return data

    def apply_to_df(self, df):
        if self.column not in df:
            raise ValueError(f"Expr column {self.column} does not exist in data {self.data}.")

        value = self.convert_value(df[self.column].dtype,self.value)

        is_expr = None
        if self.operator == "==":
            is_expr = df[self.column]==value
        elif self.operator == "!=":
            is_expr = df[self.column]!=value
        elif self.operator == ">":
            is_expr = df[self.column]>value
        elif self.operator == "<":
            is_expr = df[self.column]<value
        elif self.operator == "<=":
            is_expr = df[self.column]<=value
        elif self.operator == ">=":
            is_expr = df[self.column]>=value
        else:
            raise ValueError(f"Expr operator {self.operator} is not yet supported.")

        if DEBUG:
            print("Expr:\n",is_expr)
            print("Expr count:\n",is_expr.value_counts())
            print("Results:\n",df[is_expr])
        return df[is_expr]

    def convert_value(self, col_type, value):
        if pd.api.types.is_integer_dtype(col_type):
            return int(value)
        elif pd.api.types.is_float_dtype(col_type):
            return float(value)
        elif pd.api.types.is_bool_dtype(col_type):
            return bool(value)
        #elif pd.api.types.is_categorical_dtype(col_type):
        return value


