# -*- coding: utf-8 -*-


"""
This is the second example to create the environment of the district.

If you run the examples with Python console, you can see the output file.
To do this right-hand click the example.py file (e1.0_generate_first_district.py).
Then choose 'Modify Run Configuration' and tick 'Run with Python Console'.
"""

# Import classes of the districtgenerator to be able to use the district generator.
from districtgenerator.classes import *

def example1_1_generate_first_district():

    # Initialize District (description in the first example)
    data = Datahandler()

    # Next we generate the environment of the district
    data.generateEnvironment()

    ### =====================================  Output  ===================================== ###
    # Based on the location of the district the environment includes outside temperatures and
    # sun radiation. When you open data.site, you see the "location" is [51.0,6.55], the
    # "climateZone" 0 and the "altitude" 0. The weather data is taken from a Test Reference
    # Year Database from the DWD.
    # You find the time resolution in data.time. For this example it is 900 seconds,
    # which is equal to 15 Minutes.

    print("\nOur district now looks like this:")
    print("District:" + str(data.district))
    print("There is still no information about our district.\n")
    print("But we added information about our environment into 'site'.\n")

    return data


if __name__ == '__main__':
    data = example1_1_generate_first_district()


