import uuid

import pandas as pd

@pd.api.extensions.register_dataframe_accessor("max_metadata")
class MetaDataFrame:
    """
    Extension class for Pandas dataframes which adds useful metadata and helpers
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df

        # Use attrs field to persist metadata on the dataframe
        # https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.attrs.html
        self.df.attrs["id"] = uuid.uuid4().hex
        self.df.attrs["dimensions"] = []
        self.df.attrs["measures"] = []
        self.df.attrs["filters"] = []
        self.df.attrs["description"] = ""

        self._set_metadata_from_dtypes()

        self.error_state = None

    def get_all(self):
        return {
            "dimensions": self.get_dimensions(),
            "measures": self.get_measures(),
            "filters": self.get_filters(),
            "description": self.get_description(),
            "id": self.get_id(),
        }

    def hydrate(self, metadata: dict):
        """
        Hydrate the metadata from a dictionary.
        :param metadata: dictionary containing metadata
        """
        self.set_dimensions(metadata.get("dimensions", []))
        self.set_measures(metadata.get("measures", []))
        self.set_filters(metadata.get("filters", []))
        self.set_description(metadata.get("description", ""))
        self.df.attrs["id"] = metadata.get("id", uuid.uuid4().hex)

    def set_error_state(self, is_error: bool, message: str=None, logs=None):
        if not is_error:
            self.error_state=None
        else:
            self.error_state = {
                "message": message,
                "logs": logs
            }

    def get_full_description(self) -> str:
        description_lines = [self.get_description()]
        for col in self.df.columns:
            description_lines.append(f'{col}: {self.get_column_domain_object(col)["description"]}')
        return "\n".join(description_lines)

    def get_prompt_data(self, sample_rows: int = 100) -> str | None:
        """
        Formats a sample of the data into a string for use in a prompt.
        :param sample_rows: number of rows to include in the sample
        :return: string containing a sample of the data
        """
        import yaml
        try:
            data = [{k: str(v) for k, v in row.items()} for row in self.df.head(sample_rows).reset_index().to_dict(orient='records')]
            table_str = yaml.dump(data, sort_keys=False, width=72, indent=4, default_flow_style=None)
        except Exception:
            table_str = "error generating table data"

        if len(self.df) > sample_rows:
            return f"Here is a sample of the data values that does not include the full dataset:\n{table_str}"
        else:
            return f"Here is the full content of the dataset:\n{table_str}"

    def set_dataset_metadata(self, dataset_metadata: dict):
        # make a copy so we don't affect what's passed in
        combined_metadata = dataset_metadata.copy()

        # Add in anything that's in the dataframe but not the metadata

        for dimension in self.get_dimensions():
            existing_dim = next((x for x in combined_metadata["dimensions"] if x["name"].lower() == dimension["name"].lower()), None)

            if existing_dim is None:
                if not any(
                    (x for x in combined_metadata["measures"] if x["name"].lower() == dimension["name"].lower())):
                    combined_metadata["dimensions"].append(dimension)

        for measure in self.get_measures():
            existing_dim = next((x for x in combined_metadata["measures"] if x["name"].lower() == measure["name"].lower()), None)

            if existing_dim is None:
                if not any(
                    (x for x in combined_metadata["dimensions"] if x["name"].lower() == measure["name"].lower())):
                    combined_metadata["measures"].append(measure)

        # Only keep metadata relevant to the dataframe

        all_names = [x["name"].lower() for x in
                     self.get_dimensions() + self.get_measures()]

        combined_metadata["dimensions"] = [x for x in combined_metadata["dimensions"] if x["name"].lower() in all_names]

        combined_metadata["measures"] = [x for x in combined_metadata["measures"] if x["name"].lower() in all_names]

        self.set_dimensions(combined_metadata["dimensions"])
        self.set_measures(combined_metadata["measures"])

    def get_column_domain_object(self, column: str):
        domain_object = next((x for x in self.get_dimensions() if x["name"].lower() == column.lower()), None)

        if domain_object:
            return domain_object

        domain_object = next((x for x in self.get_measures() if x["name"].lower() == column.lower()), None)

        return domain_object

    def set_measures(self, measures: list):
        self.df.attrs["measures"] = measures

    def set_dimensions(self, dimensions: list):
        self.df.attrs["dimensions"] = dimensions

    def set_filters(self, filters: list):
        self.df.attrs["filters"] = filters

    def set_description(self, description: str):
        self.df.attrs["description"] = description

    def get_dimensions(self) -> list:
        return self.df.attrs["dimensions"]

    def get_measures(self) -> list:
        return self.df.attrs["measures"]

    def get_filters(self) -> list:
        return self.df.attrs["filters"]

    def get_description(self) -> str:
        return self.df.attrs["description"]

    def get_dataset_description(self) -> str:
        """
        DEPRECATED: Use get_full_description() instead.

        Gets the full description for a dataset
        """
        return self.get_full_description()

    def get_id(self) -> str:
        return self.df.attrs["id"]

    def _set_metadata_from_dtypes(self):
        """Set columns metadata based on the DataFrame dtypes."""
        for column, dtype in self.df.dtypes.items():
            id = f"__unknown__{column}"
            name = str(column).lower()
            sql = column
            type = "string"
            is_calculated = False

            description = f"{column}".replace("_", " ").capitalize() # TODO: get description from LLM?

            long_description = description
            label = description

            format = "str"

            domain_object_dict = {
                "id": id,
                "name": name,
                "label": label,
                "description": description,
                "long_description": long_description,
                "sql": sql,
                "is_calculated": is_calculated,
            }

            if pd.api.types.is_numeric_dtype(dtype):
                type = "number"

                domain_object_dict["aggregation"] = "sum"
                domain_object_dict["growth_output_format"] = ",.2%"
                domain_object_dict["hide_percentage_change"] = False
                domain_object_dict["sql_agg_expression"] = None

                if pd.api.types.is_integer_dtype(dtype):
                    format = "d"
                elif pd.api.types.is_float_dtype(dtype):
                    format = ",.2f"
            elif pd.api.types.is_datetime64_any_dtype(dtype):
                type = "date"
            elif pd.api.types.is_bool_dtype(dtype):
                type = "boolean"

            domain_object_dict["type"] = type
            domain_object_dict["format"] = format

            if type == "number":
                self.df.attrs["measures"].append(domain_object_dict)
            else:
                self.df.attrs["dimensions"].append(domain_object_dict)