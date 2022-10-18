import requests
from bs4 import BeautifulSoup
import json
import pickle
import sys
import tkinter as tk

class allInfo:

    def getJSON(extension):

        baseUrl = 'https://prices.runescape.wiki/api/v1/osrs'

        headers = {
            'User-Agent' : 'personal volume tracker project',
            'From' : 'bestorangesphere@gmail.com'
        }

        response = requests.get(baseUrl + extension, headers=headers)

        return response.json()

    def __init__(self) -> None:
        '''
        this will create a new dictionary that maps the id of each item (which is returned as the key in other methods)
        to the information about that item (very importantly the item name)
        '''
        def initIdMappings() -> dict:
            # this will make an API call to get the original mapping dictionary
            json = allInfo.getJSON('/mapping')
            idToItemDict = {}
            
            # item properties I wish to keep
            keep = ['members', 'lowalch', 'highalch', 'name', 'limit', 'value']

            for entry in json:
                idToItemDict.update( { entry['id'] : {}} ) # creates a new property of ID# : { list of properties }
                for property in entry:
                    if property in keep:
                        idToItemDict[entry['id']].update( { property : entry[property]})

            return idToItemDict
        
        self.idMappings = initIdMappings()

        def initNameMappings() -> dict:
            # this will make an API call to get the original mapping dictionary
            json = allInfo.getJSON('/mapping')
            nameToItemDict = {}
            
            # item properties I wish to keep
            keep = ['members', 'lowalch', 'highalch', 'name', 'limit', 'value']

            for entry in json:
                nameToItemDict.update( { entry['name'] : entry['id'] })

            return nameToItemDict

        self.nameMappings = initNameMappings()



def latestInfo(info) -> None:
    json = allInfo.getJSON('/latest')
    json = json.get('data')

    print('Crafting')
    print('----------------------------------')
    print('Sapphire Crafting methods')
    print('====================================')
    printOutput(json, 'Sapphire ring', 'Sapphire', 'Gold bar')
    printOutput(json, 'Sapphire necklace', 'Sapphire', 'Gold bar')
    printOutput(json, 'Sapphire amulet (u)', 'Sapphire', 'Gold bar')
    
    print('Emerald Crafting methods')
    print('=========================')
    printOutput(json, 'Emerald ring', 'Emerald', 'Gold bar')
    printOutput(json, 'Emerald necklace', 'Emerald', 'Gold bar')
    printOutput(json, 'Emerald amulet (u)', 'Emerald', 'Gold bar')

    print('Ruby Crafting methods')
    print('====================')
    printOutput(json, 'Ruby ring', 'Ruby', 'Gold bar')
    printOutput(json, 'Ruby necklace', 'Ruby', 'Gold bar')
    printOutput(json, 'Ruby amulet (u)', 'Ruby', 'Gold bar')

    print('Diamond Crafting methods')
    print('===========================')
    printOutput(json, 'Diamond ring', 'Diamond', 'Gold bar')
    printOutput(json, 'Diamond necklace', 'Diamond', 'Gold bar')
    printOutput(json, 'Diamond amulet (u)', 'Diamond', 'Gold bar')


    print('Enchanting')
    print('-----------------------------------')
    printOutput(json, 'Amulet of magic', 'Sapphire amulet', 'Cosmic rune')
    printOutput(json, 'Amulet of defence', 'Emerald amulet', 'Cosmic rune')
    printOutput(json, 'Amulet of strength', 'Ruby amulet', 'Cosmic rune')
    printOutput(json, 'Amulet of power', 'Diamond amulet', 'Cosmic rune')


    print('High Alching')
    print('----------------------------')
    highAlchSearch(json, 'Rune kiteshield')
    highAlchSearch(json, 'Rune full helm')
    highAlchSearch(json, 'Rune longsword')
    highAlchSearch(json, 'Rune platebody')
    highAlchSearch(json, 'Rune platelegs')
    highAlchSearch(json, 'Rune sq shield')
    highAlchSearch(json, 'Rune chainbody')
    highAlchSearch(json, 'Rune plateskirt')
    highAlchSearch(json, 'Adamant platebody')
    highAlchSearch(json, 'Rune 2h sword')
    highAlchSearch(json, 'Rune battleaxe')
    highAlchSearch(json, 'Rune med helm')
    highAlchSearch(json, 'Mithril platebody')
    highAlchSearch(json, 'Rune mace')
    highAlchSearch(json, 'Steel platebody')
    highAlchSearch(json, 'Rune scimitar')


    printOutput(json, 'Raw shrimps')

    pass

def search(item, json) -> int:
    return json.get(str(info.nameMappings.get(item))).get('low')

def printOutput(json, product, *reactants) -> None:
    reactantSum = 0
    productSellPrice = search(str(product), json)
    for reactant in reactants:
        reactantPrice = search(str(reactant), json)
        reactantSum += reactantPrice
        print(f'{reactant} sells for {reactantPrice}')
    
    print(f'Profit for {product}: {productSellPrice - reactantSum} as {product} sells for {productSellPrice} and reactants sell for {reactantSum}' )

#TODO add in limit to give amount every 4 hours
def highAlchSearch(json, item) -> None:
    itemPrice = search(item, json)
    highAlchPrice = info.idMappings.get(info.nameMappings.get(item))['highalch']
    print(f'High Alching a {item} will give a profit of {highAlchPrice - itemPrice}')
    print(f'{item} is currently selling for {itemPrice}')
    print(f'the high Alch ratio is {(highAlchPrice - itemPrice) / itemPrice}')


def sizeFrame(root):
    '''
    so what is happening here is that I am making the window size relative to the computer screen size and centering the window
    the window size is two thirds of the screen size in both dimensions (/1.5) 
    I center it by taking the middle of the screen and dividing it by half of the frame size to ensure that it is centered
    '''
    windowWidth = int(root.winfo_screenwidth() / 1.5)
    windowHeight = int(root.winfo_screenheight() / 1.5)
    xCoord = int(root.winfo_screenwidth() / 2) - int(windowWidth / 2) 
    yCoord = int(root.winfo_screenheight() / 2) - int(windowHeight / 2)
    root.geometry('{}x{}+{}+{}'.format(windowWidth, windowHeight, xCoord, yCoord))

    return root


def run(info):

    '''
    so I am thinking of just running each of these and seeing the greatest changes at runtime
    '''

    # 5 minute average
    fiveMin = '/5m'

    # 1 hour average
    hour = '1h'

    # time-series - this will require an id tag and a timestep tag -- look it up
    timeSeries = '/timeseries' 

    root = tk.Tk()
    root = sizeFrame(root)
    '''
    so what is happening here is that I am making the window size relative to the computer screen size and centering the window
    the window size is two thirds of the screen size in both dimensions (/1.5) 
    I center it by taking the middle of the screen and dividing it by 
    '''
    windowWidth = int(root.winfo_screenwidth() / 1.5)
    windowHeight = int(root.winfo_screenheight() / 1.5)
    xCoord = int(root.winfo_screenwidth() / 2) - int(windowWidth / 2) 
    yCoord = int(root.winfo_screenheight() / 2) - int(windowHeight / 2)
    root.geometry('{}x{}+{}+{}'.format(windowWidth, windowHeight, xCoord, yCoord))
    frame = tk.Frame(root)

    root.mainloop()

    


    pass




if __name__ == "__main__":
    info = allInfo()
    #latestInfo(info)
    run(info)


# TODO:
# will need to create a search so that I can enter the name of an item and get the prices back