import pandas


class DataFrameToolkit:

    @classmethod
    def convert_from_json(cls, json):
        df = pandas.DataFrame.from_dict(json, orient='columns')
        df = df.set_index('timestamp')
        return df

    @classmethod
    def convert_to_json(cls, df: pandas.DataFrame):
        df_json = {"timestamp": list(df.index)}
        for col in list(df.columns):
            if col is not 'Timestamp':
                df_json[col] = list(df[col].values.astype(float))
            else:
                df_json[col] = list(df[col].values)
        return df_json
