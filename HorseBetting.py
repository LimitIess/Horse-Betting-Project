#TODO:
#Kommentarer
#   Förklara när du ändra state
#Splitta upp i flera filer

#Libraries
import pandas as pd
import numpy as np
from random import sample
import matplotlib.pyplot as plt

#Tar in en dictionary och gör om alla nan värden till 0
#Skickar tillbaka samma dictionary
def delete_nan(dictionary_horse):
    for key, value in dictionary_horse.items():        
        if value != value:
           dictionary_horse[key] = 0
        #if isnan(value):
        #    print("Found nan")
        #if not value:
        #    dictionary_horse[key] = 0
    return dictionary_horse

#Tar in ett värde som speglar sista två siffror för år (90,01,10,20) och returnerar hela året
def convertdate(years):
    if (years//10) == 9:
        return 1900+years
    else:
        return 2000+years 

#Lämnar tillbaka en int, annars rekursivt frågar om nytt värde i en try and except block.
def checkifint(input_choice):
    try:
        if isinstance(int(input_choice), int):
            return int(input_choice)
    except:
        print("Wrong Input\nTry Again")
        input_choice = checkifint(input())
        return input_choice

#Lämnar tillbaka True 
def checkiffloat(input_choice):
    try: 
        if isinstance(float(input_choice), float):
            return float(input_choice) 
    except ValueError:
        print("Wrong input")
        input_choice = checkiffloat(input())
        return False


#Lägger till parametrar som ska testas i modellen.
def add_parameters(bettingcolumns):
    parameterlist = ["RPR", "TR", "OR","weight","prize","class"]
    #Att lägga in add, saddle, isFav och annat
    
    #Kollar om de de möjliga parametrar finns i test parametrar. Isåfall tas de bort.
    for x in bettingcolumns.keys():
        if x in parameterlist:
            parameterlist.remove(x)
    while(True):
        #Skriver ut test parametrar och möjliga parametrar att välja mellan.
        print("\n\nFollowing columns are available: ")
        print(*("{}.{}, ".format(*element) for element in enumerate(parameterlist)))        
        print("\nYour parameters: ")
        print(*("{}.{}, ".format(*element) for element in enumerate(bettingcolumns)))
        print("\n1. Add new parameter \n2. Delete one of your parameters \n3. Go back\n")

        choice_parameters = checkifint(input())
        #Om användaren skriver in 1, får den välja ny test parameter. Därefter tas parametern bort från möjliga parametrar.
        if choice_parameters == 1:
            print("\nWhich column would you like to add?")
            choice_columns = checkifint(input())
            if choice_columns <= len(parameterlist):
                bettingcolumns[parameterlist[choice_columns]] = 0
                parameterlist.pop(choice_columns)
            else:
                print("Incorrect input")
        #Om användaren skriver in 2, får den ta bort en test parameter och den läggs in i listan med möjliga parametrar.
        elif choice_parameters == 2:
            print("Which column would you like to delete? Write a number")
            tmp_dictionary = dict(list(enumerate(bettingcolumns.keys())))
            choice_columns = checkifint(input())
            if choice_columns <= len(bettingcolumns):
                parameterlist.append(tmp_dictionary[choice_columns])
                del bettingcolumns[tmp_dictionary[choice_columns]]
            else:
                print("Incorrect input")
        #Om användaren skriver in 3, returneras test parametrarna.
        elif choice_parameters == 3:
            return bettingcolumns
        else:
            print("Incorrect input")

#Användaren skriver vilken parameter som ska få en "vikt". Därefter matas in vikten på parametern.
def changeparameters(bettingcolumns):
    tmp_dictionary = dict(list(enumerate(bettingcolumns.keys())))
    while (True):
        print("Your parameters: ")
        for tmp_key, tmp_value in bettingcolumns.items():
            print("{}:{} ".format(tmp_key, tmp_value))

        print("\nWhich parameter would you like to change")
        for tmp_key, tmp_value in tmp_dictionary.items():
            print("{}.{}".format(tmp_key, tmp_value))
        print("{}.Go back\n".format(len(tmp_dictionary)))        
        choice_parameter = checkifint(input())
        if choice_parameter >= 0 and choice_parameter < len(tmp_dictionary):
            print("\nWhat should be the new Value?")
            tmp_choice = input()
            if checkiffloat(tmp_choice):
                bettingcolumns[tmp_dictionary[choice_parameter]] = tmp_choice
            else:
                print("Incorrect input")
        elif choice_parameter == len(tmp_dictionary):
            return bettingcolumns
        else:
            print("Incorrect input")

"""Först frågas användaren hur många tester som ska utföras.
Därefter väljs slumpmässiga lopp där man jämför parametrarna med varje häst. Viktigt att påpeka att högsta parameter motsvarar historikens 
värden. Varje häst får två poängsystem, först för varje parameter
vilket jämför för varje parameter och hästen med högsta parameter får poäng som motsvarar vikten. I slutet jämförs alla parametrar
och hästen med högst antal poäng väljs ut. Därefter kollar programmet om hästen har vunnit och sparar resultatet med oddsen i wins och 
odds listan."""
def HorseBettingTest(bettingcolumns, betting_data):
    race_list = betting_data.rid.unique()
    race_list = set(race_list)
    wins = []
    odds = []
    print("How many test would you like to run?")
    test_runs = checkifint(input())
    #Väljer slumpmässiga lopp och därefter körs en loop som går igenom varje lopp.
    randomly_chosen_races = sample(race_list, test_runs)
    for x in range(len(randomly_chosen_races)):
        #En mindre dataframe skapas med id på racet och datum lagras i variabel date. Därefter skapas poängsystem för varje häst.
        tmp_df = betting_data.loc[betting_data['rid'] == randomly_chosen_races[x]]
        date = tmp_df.iat[0,-1]      
        tmp_dict = dict.fromkeys(tmp_df["horseName"].tolist(), float(0))
        #For loop som går igenom varje parameter och skapar en poängsystem för varje parameter.
        #En max_value och counter används för att spara hästar som har samma värden. Exempelvis häst 1 och häst 3 har samma parameter värden
        #hade programmet alltid valt häst 1 vilket är hästen som har vunnit. Därav har man bestämt för att slumpmässigt välja en hästa
        for y in bettingcolumns:
            tmp_horse_comparison = dict.fromkeys(tmp_df["horseName"].tolist(), float(0))
            max_value = 0
            counter = 0
            #En ny dataframe skapas för varje häst, där man tar fram högsta värdet på parametern och kollar på alla datum innan racet.
            for key, value in tmp_dict.items():
                tmp_horse = betting_data.loc[(betting_data['horseName'] == key) & (betting_data['date'] < date)]
                highestcolumnvalue = tmp_horse[y].max()
                tmp_horse_comparison[key] = highestcolumnvalue
                #Undersöker om antal hästar som har samma värde
                if highestcolumnvalue > max_value:
                    max_value = highestcolumnvalue
                    counter = 0
                elif highestcolumnvalue == max_value:
                    counter += 1 
            #Hästarna med nan värden ersätts med 0, då annars hade programmet alltid valt nan värden.
            tmp_horse_comparison = delete_nan(tmp_horse_comparison)
            print(tmp_horse_comparison)
            #Om det finns fler hästar med samma värden skapas en lista med alla dessa hästar. Därefter väljs en häst slumpmässigt.
            #Annars väljer man hästen med högst värde och slutligen multipliceras vikten till slutliga poängsystemet.
            if counter > 0:
                tmp_list = [horses for horses, horse_value in tmp_horse_comparison.items() if float(horse_value) == tmp_horse_comparison[max(tmp_horse_comparison, key=tmp_horse_comparison.get)]]
                horse_won = sample(tmp_list, 1)[0]
            else:
                horse_won = max(tmp_horse_comparison, key=tmp_horse_comparison.get)
            tmp_dict[horse_won] = float(bettingcolumns[y]*1)
        #Hästen med högst värde i slutliga poängsystemet väljs ut, programmet skriver ut hästen och raceid.
        #Därefter lagras resultatet av racet i listan wins och oddsen i listan odds.
        highest_scored_horse = max(tmp_dict, key=tmp_dict.get)
        print("Race: {}  Horse: {}".format(randomly_chosen_races[x],highest_scored_horse))
        wins.append(tmp_df.loc[(betting_data["horseName"] == highest_scored_horse), "res_win"].values[0])
        odds.append((1/tmp_df.loc[(betting_data["horseName"] == highest_scored_horse), "decimalPrice"].values[0]))
    #Om fler än 0 tester har utförts, skrivs antal race, antal vinster och procentuell vinstchans av modellen.
    if len(wins) != 0:
        print("Races: {}\nWins: {}\nWinrate: {}".format(len(wins),wins.count(1),wins.count(1)/len(wins)))
    return wins, odds

#Användaren väljer storleken på varje bet, därefter beräknas balansen. Om hästen har vunnit multipliceras bet storleken med oddsen.
#Annars har man förlorat bet storleken och slutligen skrivs ut hela balansen och en graf visualiserar resultatet efter varje bet.
def results(results_array,odds):
    print("\nWhats your betsize")
    betsize = checkiffloat(input())
    Balance = 0
    Balance_graph = []
    for x in range(len(results_array)):
        if results_array[x] == 1:
            Balance += betsize*odds[x]
        else:
            Balance -= betsize
        Balance_graph.append(Balance)
    print("Your balance is : {}".format(Balance))
    plt.plot(list(range(1,len(Balance_graph)+1)),Balance_graph)
    plt.ylabel("Balance in Dollars")
    plt.xlabel("Number of races")
    plt.title("Balance")
    plt.show()

#Huvudmeny för programmet, användaren måste först välja parametrar i 1, därefter sätta vikt på de i 2.
#Efter man har utfört de 2 stegen, kan man testa modellen mot riktig data i 3.
#När man har fått resultat testerna kan man visualisera och få fram vinsten i 4. 
#Om 5 matas in avslutas programmet. 
def HorseBetting(dataframe, bettingparameters):
    choice_3 = 0
    choice_2 = 0
    while (True):
        print("\n1. Choose your parameters \n2. Set value for your parameters \n3. Test your parameters\n4. Choose betsize\n5. End program")
        choice = checkifint(input())
        if choice == 1:
            bettingparameters = add_parameters(bettingparameters)
        elif choice == 2:
            if len(bettingparameters) == 0:
                print("There are no parameters to change")
            else:
                bettingparameters = changeparameters(bettingparameters)
                choice_2 = 1
        elif choice == 3:
            if choice_2 == 0:
                print("You need to do step 2")
            else:
                wins, odds = HorseBettingTest(bettingparameters, dataframe)
                choice_3 = 1
        elif choice == 4:
            if (choice_3 == 1):
                results(wins,odds)
            else:
                print("You need to do step 3")
        elif choice == 5:
            return
        else: 
            print("Wrong input")

#För att starta programmet, läses data filen in med allt häst info, det skapas även en kolumn med datum och slutligen skickas allt till en
#funktion som är en huvudmeny.
if __name__ == "__main__":
    path = 'C:\\Users\\damia\\Desktop\\Betting\\DVGB06Betting\\'
    bettingcolumns = {}
    betting_data = pd.read_csv(path+'\\Bettingdata.csv', dtype={"rclass": 'str'})
    betting_data["Year"] = betting_data["Year"].map(convertdate)
    betting_data["date"] = pd.to_datetime(betting_data[["Year","Month","Day"]]) 
    HorseBetting(betting_data, bettingcolumns)
