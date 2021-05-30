import requests, csv
from collections import defaultdict
from statistics import mean

PAGE_SIZE = 50
TOTAL_APES = 10000

url = "https://api.opensea.io/api/v1/assets"
querystring = {"asset_contract_address": "0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d", "order_direction": "desc", "offset": "0", "limit": str(PAGE_SIZE)}

apes = []
traits = ['Earring', 'Background', 'Fur', 'Mouth', 'Clothes', 'Hat', 'Eyes']
fieldnames = ['token_id', 'price', 'numTraits', 'maxRarity', 'avgRarity'] + traits + ['permalink']

while len(apes) < TOTAL_APES:
	response = requests.request("GET", url, params=querystring).json()

	for ape in response['assets']:
		
		thisApe = {'token_id': ape['token_id']}

		if ape['sell_orders']:
			thisApe['price'] = float(ape['sell_orders'][0]['current_price']) / 1000000000000000000.0
		else:
			thisApe['price'] = None

		rarity = 1
		traitPercents = []

		for trait in ape['traits']:
			thisApe[trait['trait_type']] = trait['value']
			traitPercents.append(float(trait['trait_count']) / float(10000))
		
		avgRarity = mean(traitPercents)

		traitPercents.remove(max(traitPercents))
		rarity = max(traitPercents)

		thisApe['numTraits'] = len(ape['traits'])
		thisApe['maxRarity'] = rarity
		thisApe['avgRarity'] = avgRarity
		thisApe['permalink'] = ape['permalink']

		for trait in traits:
			if trait not in thisApe:
				thisApe[trait] = None

		apes.append(thisApe)

	querystring['offset'] = str(int(querystring['offset']) + int(querystring['limit']))

	print len(apes)


with open('apes.csv', 'w') as csvfile:
	writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
	writer.writeheader()

	for ape in apes:
		writer.writerow(ape)

