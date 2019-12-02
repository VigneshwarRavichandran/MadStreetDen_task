# Design and implement a distributed worker system to update data in Redis using Python.

## Installation
This requires python3.

To build the docker:
```sh
$ docker-compose build
```

To up the docker:
```sh
$ docker-compose up
```


## Get Started

#### Pre-execution:

The pre-execution is done by `MadStreetDen_task/pyspark_script/prepare_and_execute.sh`. 

```sh
cd pyspark_script
unzip womens-shoes-prices.zip
pip install -r requirements.txt
python importer.py
```

The `MadStreetDen_task/pyspark_script/womens-shoes-prices.zip` file contains the large .csv files. The `MadStreetDen_task/pyspark_script/importer.py` contains the python script for reading the csv files and storing it in the redis store.


### Endpoints

The endpoinds operations are done in `MadStreetDen_task/app.py`.

#### getRecentItem

To getRecentItem ping to http://0.0.0.0:8000/getRecentItem?date=2017-02-03.
JSON object returned for the above usecase

```
{
	"brand": "In-Sattva",
	"colors": "Yellow",
	"date_added": "2017-02-03T22:06:20Z",
	"id": "AVpfGgD5ilAPnD_xU-VH"
}
```


#### getBrandsCount

To getBrandsCount ping to http://0.0.0.0:8000/getBrandsCount?date=2017-02-03.
JSON object returned for the above usecase

```
{
	"result": [
		[
			"In-Sattva",
			9
		],
		[
			"Novica",
			8
		],
		[
			"Birkenstock",
			2
		],
		[
			"Journee Collection",
			2
		],
		[
			"Moksha Imports",
			1
		],
		[
			"Joules",
			1
		],
		[
			"Nature Breeze",
			1
		],
		[
			"Muk Luks",
			1
		],
		[
			"Beston",
			1
		],
		[
			"Qupid",
			1
		],
		[
			"LILIANA",
			1
		],
		[
			"UGG Australia",
			1
		],
		[
			"VIA PINKY",
			1
		],
		[
			"Sperry",
			1
		],
		[
			"Alfani",
			1
		],
		[
			"Naturalizer",
			1
		],
		[
			"Asics",
			1
		],
		[
			"1 World Sarongs",
			1
		]
	]
}
```

#### getItemsbyColor

To getRecentItem ping to http://0.0.0.0:8000/getItemsbyColor?color=chocolate.
JSON object returned for the above usecase

```
{
	"result": [
		{
			"brand": "SKECHERS",
			"colors": "CHOCOLATE",
			"date_added": "2019-04-28T08:10:06Z",
			"id": "AWpjGQEEM263mwCq9udy"
		},
		{
			"brand": "Lamo",
			"colors": "Chocolate",
			"date_added": "2019-04-28T03:18:36Z",
			"id": "AWph_EFu0U_gzG0hiYRP"
		},
		{
			"brand": "Giani Bernini",
			"colors": "Chocolate",
			"date_added": "2019-04-27T06:20:07Z",
			"id": "AWpdhraEJbEilcB6Px-E"
		},
		{
			"brand": "Corral",
			"colors": "Chocolate",
			"date_added": "2019-04-26T07:09:16Z",
			"id": "AWpYiX17M263mwCq85wx"
		},
		{
			"brand": "Skechers",
			"colors": "Chocolate",
			"date_added": "2019-04-24T03:19:38Z",
			"id": "AWpNdXa7AGTnQPR7tdsJ"
		},
		{
			"brand": "Skechers",
			"colors": "Chocolate",
			"date_added": "2019-04-24T03:19:37Z",
			"id": "AWpNaeHzM263mwCq8RFC"
		},
		{
			"brand": "Skechers",
			"colors": "Chocolate",
			"date_added": "2019-04-24T03:19:37Z",
			"id": "AWpNYelkM263mwCq8Q05"
		},
		{
			"brand": "UGG",
			"colors": "Chocolate",
			"date_added": "2019-04-23T08:20:32Z",
			"id": "AWpJXKEoAGTnQPR7tQ0u"
		},
		{
			"brand": "Giani Bernini",
			"colors": "Chocolate",
			"date_added": "2019-04-23T06:28:01Z",
			"id": "AWpJEShIM263mwCq8A3p"
		},
		{
			"brand": "Caterpillar",
			"colors": "Chocolate",
			"date_added": "2019-04-20T03:22:53Z",
			"id": "AWo40d770U_gzG0hfc6Z"
		}
	]
}
```
