from typing import List
import pandas as pd

from pathlib import Path

from electricity_network_file_parser import FileParserGen
from electricity_network_file_parser.dataclasses import PropertyDescription

class TextParser8x:
    def __init__(self, file_path):
        super().__init__(file_path)

    def parse_property_line(self, property_line : str):
        property_name = property_line[1: property_line.index(" ")]
        property_attributes = property_line[property_line.index(" "):]
        col_name = ''
        value = ''
        reading_value = False
        reading_string = False
        property_dict = {}
        for char in property_attributes:
            if char == ':' and not reading_value:
                reading_value = True
            elif not reading_value:
                col_name += char
            elif char == ' ' and not reading_string and value != '':
                property_dict[col_name.strip()] = self.parse_value(value)
                reading_value = False
                value = ''
                col_name = ''
            elif reading_value:
                if char == "'" and not reading_string:
                    reading_string = True
                elif char == "'" and reading_string:
                    reading_string = False
                value += char

        property_dict[col_name.strip()] = self.parse_value(value)
        return PropertyDescription(property_name, property_dict)

    def parse_entities(self, lines : List[str], property_attributes_to_parse : List[str]):
        parsed_property_types = []
        data_instance = {}
        data_instances = []
        for line in lines:
            line_stripped = line.strip()
            property_name = ""
            if " " in line_stripped:
                property_name = line_stripped[1: line_stripped.index(" ")]
            started_new_entity = property_name in parsed_property_types and property_name == "General"
            all_property_types_parsed = len(parsed_property_types) == len(property_attributes_to_parse)
            if started_new_entity or all_property_types_parsed:
                if not all_property_types_parsed:
                    print(f"Not all property types are present for entity {line_stripped}")
                data_instances.append(data_instance)
                data_instance = {}
                parsed_property_types = []
            if property_name in property_attributes_to_parse:
                general_properties = self.parse_property_line(line_stripped)
                self.extend_dictionary(data_instance, general_properties.property_attributes)
                parsed_property_types.append(general_properties.property_type)

        if len(data_instance.items()) > 0:
            data_instances.append(data_instance)

        return pd.DataFrame(data_instances)

    def parse_cable_types(self, cables_df : pd.DataFrame) -> pd.DataFrame:
        pass
