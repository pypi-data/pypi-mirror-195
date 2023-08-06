import pandas


class DataFrameToolkit:

    @classmethod
    def convert_from_json(cls, json):
        df = pandas.DataFrame.from_dict(json, orient='columns')
        df = df.set_index('timestamp')
        return df

    @classmethod
    def convert_to_json(cls, df):
        df_json = {"timestamp": list(df.index)}
        for col in list(df.columns):
            df_json[col] = list(df[col].values)
        return df_json
