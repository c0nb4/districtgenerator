import unittest
import random as rd
from random import sample
import os
import pandas as pd
from districtgenerator.classes import datahandler
from districtgenerator.functions import path_checks
# Should create simulations for residential buildings
# Write a test that all functions run through without errors
# Check if the results exist and are not zero

PARENT_FOLDER_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestResidential(unittest.TestCase):
    def setUp(self):
        # Create test scenario
        self.test_data = { 
            'id': [0, 1, 2, 3],
            'building': ["SFH", "SFH", "TH", "MFH"],
            'year': [rd.randint(1900, 2024) for _ in range(4)],
            'retrofit': [rd.randint(0 , 2 ) for _ in range(4)],
            'area': [rd.randint(10, 100) for _ in range(4)],
            'construction_type': ["", "", "", ""],
            'night_setback': [rd.randint(0, 1) for _ in range(4)],
            'heater': ["HP", "BOI", "HP", "BOI"],
            'PV': [rd.randint(0, 1) for _ in range(4)],
            'STC': [rd.randint(0, 1) for _ in range(4)],
            'EV': [rd.randint(0, 1) for _ in range(4)],
            'BAT': [rd.randint(0, 1) for _ in range(4)],
            'f_TES': [rd.randint(0, 1) for _ in range(4)],
            'f_BAT': [rd.randint(0, 1) for _ in range(4)],
            'f_EV': ["M", "M", "M", "M"],
            'f_PV': [rd.randint(0, 1) for _ in range(4)],
            'f_STC': [rd.randint(0, 1) for _ in range(4)],
            'gamma_PV': [rd.randint(0, 1) for _ in range(4)],
            'ev_charging': ["on_demand", "on_demand", "on_demand", "on_demand"]
        }
        df = pd.DataFrame(self.test_data, columns=self.test_data.keys())
        self.scenario_path = os.path.join(PARENT_FOLDER_PATH, 'districtgenerator', 'data', 'scenarios', 'test_scenario.csv')
        df.to_csv(self.scenario_path, index=False, sep=';')
        print(df.head())
        # Define a consistent results path
        #C:\Users\felix\Programmieren\tecdm\src\districtgenerator\test_scenario
        self.results_path = os.path.join(PARENT_FOLDER_PATH,  'test_scenario', 'demands')
        

    def test_residential(self):
        data = datahandler.Datahandler()
        data.setWeatherFile(os.path.join(PARENT_FOLDER_PATH, 'districtgenerator', 'data', 'weather', 'EPW', 'DEU_BE_Berlin-Schonefeld.AP.103850_TMYx.2004-2018.epw'))
        data.generateEnvironment(plz="52070")
        data.initializeBuildings('test_scenario')
        data.setResultPath('test_scenario')
        data.generateBuildings()
        data.generateDemands()
        # Verify that results are generated
        self.assertTrue(os.path.exists(self.results_path), f"Results directory not found: {self.results_path}")
        self.assertTrue(any(fname.endswith('.csv') for fname in os.listdir(self.results_path)), "No CSV files found in results directory.")
        for file in os.listdir(self.results_path):
            if file.endswith('.csv'):
                file_path = os.path.join(self.results_path, file)
                df = pd.read_csv(file_path, sep=',')
                required_columns = ["elec", "dhw", "occ", "gains", "heat"]
                for column in required_columns:
                    self.assertIn(column, df.columns, f"Column {column} not found in file: {file_path}")
                self.assertGreaterEqual(df["heat"].sum(), 0, f"Heat sum is negative in file: {file_path}")
                self.assertGreaterEqual(df["elec"].sum(), 0, f"Electricity sum is negative in file: {file_path}")
                self.assertGreaterEqual(df["dhw"].sum(), 0, f"DHW sum is negative in file: {file_path}")
                self.assertGreaterEqual(df["occ"].sum(), 0, f"Occupancy sum is negative in file: {file_path}")
                self.assertTrue(df["gains"].notna().any(), f"Gains column has no values in file: {file_path}")
        
        scenario_data = pd.read_csv(self.scenario_path, sep=';')
        for index, row in scenario_data.iterrows():
            building = row['building']
            print(building)
            
            building_id = str(index)
            building_file = None
            for file in os.listdir(self.results_path):
                if file.startswith(f"{building_id}_{building}") and file.endswith(".csv"):
                    building_file = os.path.join(self.results_path, file)
                    df = pd.read_csv(building_file, sep=',')
                    energy_demand = df['heat'].sum() / 1000
                    area = row['area']
                    energy_demand_per_square_meter = energy_demand / area
                    print(f"Energy demand per square meter for building {building}: {energy_demand_per_square_meter} with area {area}")
                    self.assertGreaterEqual(energy_demand_per_square_meter, 0, f"Energy demand per square meter is negative for building {building}: {energy_demand_per_square_meter}")
            self.assertIsNotNone(building_file, f"No results file found for building {building_id}")


    def tearDown(self):
        if os.path.exists(self.scenario_path):
            os.remove(self.scenario_path)
        if os.path.exists(self.results_path):
            for file in os.listdir(self.results_path):
                file_path = os.path.join(self.results_path, file)
                if os.path.isfile(file_path):
                    try:
                        os.remove(file_path)
                    except PermissionError:
                        print(f"Unable to delete {file_path}. File may be in use.")
            try:
                os.rmdir(self.results_path)
            except OSError:
                print(f"Unable to remove directory {self.results_path}. It may not be empty or you may not have permission.")
        else:
            print(f"Results directory not found: {self.results_path}")


if __name__ == '__main__':
    unittest.main()