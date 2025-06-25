from enum import Enum
import pandas as pd
from electricity_network_file_parser import FileParserGen
from electricity_network_file_parser.TextParser7x import TextParser7x
from electricity_network_file_parser.TextParser8x import TextParser8x
from electricity_network_file_parser.dataclasses import EntityDescription7x

class VersionNumber(Enum):
    G7 = "G7."
    G8 = "G8."

class GnfParser(FileParserGen):

    def __init__(self, file_path):
        super().__init__(file_path)
        if VersionNumber.G7 in self.version_string:
            self.version_number = VersionNumber.G8
            self.text_parser = TextParser8x(file_path)
        elif VersionNumber.G8 in self.version_string:
            self.version_number = VersionNumber.G7
            self.text_parser = TextParser7x(file_path)

        if self.text_parser is None:
            raise ValueError("Unsupported file format. Only G7 and G8 files are supported.")

        if self.version_number == VersionNumber.G8:
            self.parse_entities_dict = {
                "PROFILE" : ["General", "ProfileType"],
                "GM TYPE" : ["General"],
                "NODE" : ["General"],
                "LINK" : ["General"],
                "CABLE" : ["General", "CablePart", "CableType"],
                "TRANSFORMER" : ["General", "VoltageControl", "TransformerType"],
                "SOURCE" : ["General"],
                "LOAD" : ["General"],
                "HOME" : ["General", "ConnectionCableType", "FuseType"],
                "MEASURE FIELD" : ["General"],
                "FUSE": ["General"]
            }
        elif self.version_number == VersionNumber.G7:
            self.parse_entities_dict = {
                "PROFILE" : [EntityDescription7x(1, ["number", "name", "profiletype"])],
                "NODE" : [EntityDescription7x(1, ["number", "revision", "name", "shortname", "ID", "Unom", "GroundingConfig", "s_n_pe", "s_pe_a", "Ra", "k_h1", "k_h2", "k_h3", "k_h4", "s_h1", "s_h2", "s_h3", "s_h4", "gx", "gy", "SkipCalculation", "FailFrequency"])],
                "LINK" : [EntityDescription7x(1, ["number", "revision", "knr1", "knr2", "name", "s1_l1", "s1_l2", "s1_l3", "s1_n", "s1_pe", "s2_l1", "s2_l2", "s2_l3", "s2_n", "s2_pe", "field1", "field2", "failurefrequency", "s1_h1", "s1_h2", "s1_h3", "s1_h4", "s2_h1", "s2_h2", "s2_h3", "s2_h4"])],
                "CABLE" : [
                    # EntityDescription7x(1, ["number", "revision", "knr1", "knr2", "name", "s1_l1", "s1_l2", "s1_l3", "s1_n", "s1_pe", "s2_l1", "s2_l2", "s2_l3", "s2_n", "s2_pe", "field1", "field2", "failurefrequency", "new", "homegrouding", "homeRa", "PV-scaling", "PV-profilenr", "k1_1", "k1_2", "k1_3", "k1_4", "k1_5", "k1_6", "k1_7", "k1_8", "k1_9", "k2_1", "k2_2", "k2_3", "k2_4", "k2_5", "k2_6", "k2_7", "k2_8", "k2_9", "s1_h1", "s1_h2", "s1_h3", "s1_h4", "s2_h1", "s2_h2", "s2_h3", "s2_h4", "meltsafetytype1_h", "currenttype1_h", "meltsafetytype2_h", "currenttype2_h"]), 
                    EntityDescription7x(2, ["length", "cabletype"]),
                    EntityDescription7x(3, ["shortname", "Unom", "price", "C", "C0", "Inom0", "G1", "Inom1", "G2", "Inom2", "G3", "Inom3", "Ik1s", "TR", "TInom", "TIk1s", "frequency", "r_g", "x_g", "r_gg_n", "x_ggf_n", "r_gg_t", "x_gg_t", "r_a", "x_a", "r_ga", "x_ga", "r_h", "x_h", "r_gh_n", "x_gh_n", "r_gh_t", "x_gh_t", "r_hh_n", "x_hh_n", "r_hh_t", "x_hh_t", "r_ha", "x_ha", "Inom_a", "Ik1s_a", "Inom_h", "Ik1s_h", "r_g/r_n"]) 
                ],
                "TRANSFORMER" : [
                    EntityDescription7x(1, ["nr", "revision", "knr1", "knr2", "naam", "s1_l1", "s1_l2", "s1_l3", "s1_n", "s1_pe", "s2_l1", "s2_l2", "s2_l3", "s2_n", "s2_pe", "veld1", "veld2", "faalfrequentie", "trafotype", "s_n_pe", "s_pe_a", "Ra", "trapstand", "regelingstatus", "meetzijde", "regelknoopnr", "Uset", "Uband", "regelingsoort", "Rc", "Xc", "terugc", "Pmin", "Umin", "Pmax", "Umax"]), 
                    EntityDescription7x(2, ["kortenaam", "Snom", "Unom1", "Unom2", "Uk", "Pk", "Pnul", "Inul", "R0", "Z0", "Ik2s", "schak1", "schak2", "klok", "trapzijde", "trapgrootte", "trapmin", "trapnom", "trapmax", "regelbaar"]),
                ],
                "SOURCE" : ["General"],
                "LOAD" : ["General"],
                "HOME" : ["General", "ConnectionCableType", "FuseType"],
                "MEASURE FIELD" : ["General"],
                "FUSE": ["General"]
            }

    def parse_cable_types(self, cables_df : pd.DataFrame) -> pd.DataFrame:
        columns_to_group_by = ["C", "C0", 
                               "Inom0", "G1", "Inom1", "G2", 
                               "Inom2", "G3", "Inom3", "Ik1s", 
                               "Tr", "TInom", "TIk1s", "Frequency", 
                               "R_c", "X_c", "R_cc_n", "X_cc_n", "R_cc_o", 
                               "X_cc_o", "R_e", "X_e", "R_ce", "X_ce", "Inom_e", "Ik1s_e", 
                               "R_h", "X_h", "R_ch_n", "X_ch_n", "R_ch_o", 
                               "X_ch_o", "R_hh_n", "X_hh_n", "R_hh_o", "X_hh_o", "R_he", "X_he", 
                               "Inom_h", "Ik1s_h"]

        unique_cable_types = self.group_data_frame_by_columns(cables_df, columns_to_group_by)
        dictionaries = unique_cable_types.to_dict('records')
        long_names = []
        short_names = []
        for dictionary in dictionaries:
            dictionary.pop("count")
            cables_with_cable_type_params = self.get_records_containing_field_values(cables_df, dictionary)
            cable_types = cables_with_cable_type_params["CableType"].unique()
            short_names_values = cables_with_cable_type_params["ShortName"].unique()
            long_names.append(",".join(cable_types))
            short_names.append(",".join(short_names_values))

        unique_cable_types["Longnames"] = long_names
        unique_cable_types["Shortnames"] = short_names
        return unique_cable_types