import requests
from xml.etree import ElementTree as ET

# Constants
URL = 'http://www.bnr.ro/nbrfxrates.xml'


def getRates():
    # Make a dictionary to store the exchange rates
    exchange_rates = {}

    response = requests.get(URL)

    try:
        tree = ET.fromstring(response.content)

        target = tree.findall(".//{http://www.bnr.ro/xsd}Rate")

        for element in target:
            multiplier = 1
            # if the element has the multiplier attribute
            if 'multiplier' in element.attrib:
                # get the multiplier attribute
                multiplier = element.attrib['multiplier']
            # get the currency name from the currency attribute
            currency = element.attrib['currency']
            # get the exchange rate from the text
            rate = element.text
            # add the exchange rate to the dictionary
            exchange_rates[currency] = float(rate) * int(multiplier)

        return exchange_rates

    except Exception as e:
        print(e)
        return None
