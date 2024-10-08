![E.ON EBC RWTH Aachen University](./img/EBC_Logo.png)

# districtgenerator

[![License](http://img.shields.io/:license-mit-blue.svg)](http://doge.mit-license.org)

The districtgenerator is a Python tool for generating building-specific thermal, electrical and occupancy profiles for districts. 
By integrating several open-source data bases and tools like [TEASER](https://github.com/RWTH-EBC/TEASER) and 
[richardsonpy](https://github.com/RWTH-EBC/richardsonpy), 
the districtgenerator is designed to provide easy access to profile generation. 

The districtgenerator is being developed at [RWTH Aachen University, E.ON Energy
Research Center, Institute for Energy Efficient Buildings and Indoor
Climate](https://www.ebc.eonerc.rwth-aachen.de/cms/~dmzz/E-ON-ERC-EBC/?lidx=1) and [TU Berlin, Institute for Digital Networking of Buildings, Energy Supply Systems and Users](https://www.tu.berlin/en/dvg).

## Version

The districtgenerator is an ongoing research project. The current version is v0.1.0.

## Getting started

### Install the districtgenerator

To install, first clone this repository with

```
git clone https://github.com/RWTH-EBC/districtgenerator

```

```
python -m venv .venv      
```

activate the envrionment and run:

```
pip install -e <path-to-districtgenerator> .
```

### How to get started?

Once you have installed the generator, you can check the [examples](./examples) to learn how to use the different components.

### Minimum required input data

To generate your district, you need to know some information about its buildings. 
The minimal input data set was defined following the [TABULA archetype approach](https://webtool.building-typology.eu/#bm) and related approach for non-residential buildings [DATA NWG](https://github.com/IWUGERMANY/Nichtwohngebaeude-Typologie-Deutschland):
* _id_: building ID (just numerate the buildings)
* _building_: building type (residential: single family house, terraced house, multi family house or apartment block, non-residential: Office, Administrative or Government Buildings, Research and University Teaching, Health and Care, School, Day Nursery and other Care, Culture and Leisure, Sports Facilities, Hotels, Boarding, Restaurants or Catering, Production, Workshop, Warehouse or Operations, Trade Buildings, Technical and Utility (supply and disposal), Transport, Generalized (1) Services building, Includes categories (1) to (7) and (9), Generalized (2) Production buildings and similar, Includes cat. (8), (10), (11) )
* _year_: construction year (the calendar year in which the building was constructed)
* _retrofit_: retrofit state according to TABULA (0: existing state, 1: usual refurbishment, 2: advanced refurbishment)
* _area_: reference floor area (given in square meters)

Please find a template [here](./data/scenarios/example.csv).

### What you get

After executing district generation you can find building-specific profiles in 
the .csv format in folder results/demands. The results contain: 
* _heat_: space heating demand
* _dhw_: domestic hot water demand
* _elec_: electricity demand for lighting and electric household devices
* _occ_: number of persons present
* _gains_: internal gains from persons, lighting and electric household devices

All values are given in Watt and for the [time resolution](./data/time_data.json) you require.


## Known Limitations

* Non-Residential Buildings need EPW-Files.

## License

The districtgenerator is released by RWTH Aachen University, E.ON Energy
Research Center, Institute for Energy Efficient Buildings and Indoor Climate,
under the
[MIT License](LICENSE.md).

## Reference

coming soon :)

## Acknowledgements

The districtgenerator has been developed within the public funded projects 
"BF2020 Begleitforschung ENERGIEWENDEBAUEN - Modul Quartiere" (promotional reference: 03EWB003B) and "BF2020 Begleitforschung ENERGIEWENDEBAUEN - Modul Digitalisierung" (promotional reference: 04EWB003A) and with financial support by BMWK (German Federal Ministry for Economic Affairs and Climate Action).

<img src="https://www.innovation-beratung-foerderung.de/INNO/Redaktion/DE/Bilder/Titelbilder/titel_foerderlogo_bmwi.jpg?__blob=normal" width="200">

## Problems?
Please [raise an issue here](https://github.com/RWTH-EBC/districtgenerator/issues/new).