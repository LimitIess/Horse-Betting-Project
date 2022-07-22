#Libraries
from cmath import nan
import pandas as pd
import numpy as np
from random import sample
import matplotlib.pyplot as plt

#Tar in en dictionary och gör om alla nan värden till 0
#Skickar tillbaka samma dictionary
def delete_nan(dictionary_horse):
    for key, value in dictionary_horse.items():        
        if value != value or value == None:
           dictionary_horse[key] = 0
    return dictionary_horse

#Tar in ett värde som speglar sista två siffror för år (90,01,10,20) och returnerar hela året
def convertdate(years):
    if (years//10) == 9:
        return 1900+years
    else:
        return 2000+years 

#Funktionen kollar om värdet som matas in är en float eller int.
def validate_input(tpe):
    while True:
        try:
            if tpe == "float":
                return float(input())
            return int(input())
        except:
            print("Wrong input")

#Funktionen som kollar om värdet är först en int därefter om den är större än 0.
def validate_input_only_natural_numbers():
    input = -1
    while input <=0:
        input = validate_input("int")
        if input > 0:
            return input
        else:
            print("Input must be above 0")

#Lägger till parametrar som ska testas i modellen.
def add_parameters(bettingcolumns):
    parameterlist = ["RPR", "TR", "OR","weight","jockey_winrate","trainer_winrate","horse_winrate","avg_prize","tot_prize"]
    
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

        choice_parameters = validate_input("int")
        #Om användaren skriver in 1, får den välja ny test parameter. Därefter tas parametern bort från möjliga parametrar.
        if choice_parameters == 1:
            print("\nWhich column would you like to add?")
            choice_columns = validate_input("int")
            if choice_columns < 0:
                print("Incorrect Input")
            elif choice_columns <= len(parameterlist):
                bettingcolumns[parameterlist[choice_columns]] = 0
                parameterlist.pop(choice_columns)

        #Om användaren skriver in 2, får den ta bort en test parameter och den läggs in i listan med möjliga parametrar.
        elif choice_parameters == 2:
            print("Which column would you like to delete? Write a number")
            tmp_dictionary = dict(list(enumerate(bettingcolumns.keys())))
            choice_columns = validate_input("int")
            if choice_columns < 0:
                print("Incorrect Input")
            elif choice_columns <= len(bettingcolumns):
                parameterlist.append(tmp_dictionary[choice_columns])
                del bettingcolumns[tmp_dictionary[choice_columns]]
            
        #Om användaren skriver in 3, returneras test parametrarna.
        elif choice_parameters == 3:
            return bettingcolumns

#Användaren skriver vilken parameter som ska få en "vikt". Därefter matas in vikten på parametern.
def change_parameters(bettingcolumns):
    tmp_dictionary = dict(list(enumerate(bettingcolumns.keys())))
    while (True):
        print("Your parameters: ")
        for tmp_key, tmp_value in bettingcolumns.items():
            print("{}:{} ".format(tmp_key, tmp_value))

        print("\nWhich parameter would you like to change")
        for tmp_key, tmp_value in tmp_dictionary.items():
            print("{}.{}".format(tmp_key, tmp_value))
        print("{}.Go back\n".format(len(tmp_dictionary)))        
        choice_parameter = validate_input("int")
        if choice_parameter >= 0 and choice_parameter < len(tmp_dictionary):
            print("\nWhat should be the new Value?")
            tmp_choice = validate_input("float")
            if tmp_choice >= 0:
                bettingcolumns[tmp_dictionary[choice_parameter]] = tmp_choice
            else:
                print("Incorrect input")
        elif choice_parameter == len(tmp_dictionary):
            return bettingcolumns

"""Först frågas användaren hur många tester som ska utföras.
Därefter väljs slumpmässiga lopp där man jämför parametrarna med varje häst. 
Beroende på parameter kan metoderna skilja sig åt varandra.
"TR","OR","RPR","weight" : Programmet väljer värdet från senaste race.
"jockey_winrate" och "trainer_winrate": Programmet öppnar en csvfil som innehåller tränarens eller kuskens procentuella vinstchans.
"horse_winrate": Programmet beräknas hästens procentuella vinstchans från tidigare lopp.
"avg_prize" : Programmet beräknar snitt pris per lopp från tidigare data
"tot_prize" : Programmet beräknar totala priset från tidigare data.
Varje häst får två poängsystem, först för varje parameter och sedan för totala poängsystemet.
Poängen per parameter delas upp i procent, dvs. Hästen med högsta värdet får totala vikten, hästen med lägsta får 0 och för hästarna i mellan får procent motsvarade mellan
högsta och lägsta värdet.
I slutet jämförs alla parametrar och hästen med högst antal poäng väljs ut. Därefter kollar programmet om hästen har vunnit och sparar resultatet med oddsen i wins och 
odds listan. Om det finns hästar med lika mycket poäng väljer man ut slumpmässigt.
"""

def horse_betting_test(bettingcolumns, betting_data):
    race_list = betting_data.rid.unique()
    race_list = set(race_list)
    wins = []
    odds = []
    print("How many test would you like to run?")
    test_runs = validate_input_only_natural_numbers()
    #Väljer slumpmässiga lopp och därefter körs en loop som går igenom varje lopp.
    randomly_chosen_races = sample(race_list, test_runs)
    for x in range(len(randomly_chosen_races)):
        #En mindre dataframe skapas med id på racet och datum lagras i variabel date. Därefter skapas poängsystem för varje häst.
        tmp_df = betting_data.loc[betting_data['rid'] == randomly_chosen_races[x]]
        date = tmp_df.iat[0,-1]      
        tmp_dict = dict.fromkeys(tmp_df["horseName"].tolist(), float(0))
        #For loop som går igenom varje parameter och skapar en poängsystem för varje parameter.
        for y in bettingcolumns:
            tmp_horse_comparison = dict.fromkeys(tmp_df["horseName"].tolist(), float(0))
            if y in ["TR","OR","RPR","weight"]:
                tmp_horse_comparison = dict.fromkeys(tmp_df["horseName"].tolist(), float(0))
                #En ny dataframe skapas för varje häst, där man tar fram högsta värdet på parametern och kollar på alla datum innan racet.
                for key in tmp_dict:
                    tmp_horse = betting_data.loc[(betting_data['horseName'] == key) & (betting_data['date'] < date),y]
                    #Ändrar ordningen på dataframet då race är redan sorterade. I detta fall får man senaste lopp från first_valid_index.
                    tmp_horse = tmp_horse.iloc[::-1]
                    index = tmp_horse.first_valid_index()
                    #Om det saknas lopp för hästen, lagras det som None
                    latestcolumnvalue = tmp_horse.loc[index] if index is not None else None 
                    tmp_horse_comparison[key] = latestcolumnvalue
                print(tmp_horse_comparison)
                
            #Läser in jockey.csv som innehåller alla procentuella vinstchanser. Därefter väljer man rätt sort kusk och kollar på "winrate".
            elif y == "jockey_winrate":
                jockey_df = pd.read_csv(path+'\\jockey.csv')
                for key in tmp_dict:
                    try:
                        jockey = tmp_df.loc[(tmp_df['horseName'] == key), "jockeyName"].values[0]
                        tmp_horse_comparison[key] = jockey_df.loc[jockey_df["jockeyName"] == jockey, "winrate"].values[0]
                    except IndexError:
                        tmp_horse_comparison[key] = None

            #Fungerar på samma sätt som ovan men för tränare
            elif y == "trainer_winrate":
                trainer_df = pd.read_csv(path+'\\trainer.csv')
                for key in tmp_dict:
                    try:
                        trainer = tmp_df.loc[(tmp_df['horseName'] == key), "trainerName"].values[0]
                        tmp_horse_comparison[key] = trainer_df.loc[trainer_df["trainerName"] == trainer, "winrate"].values[0]
                    except IndexError:
                        tmp_horse_comparison[key] = None

            #Programmet skapar en mindre dataframe med häst namn och all historisk data innan loppet. Därefter kollar man antalet vinster med totala längden av dataframet.
            elif y == "horse_winrate":
                for key in tmp_dict.items():
                    tmp_horse = betting_data.loc[(betting_data['horseName'] == key) & (betting_data['date'] < date)]
                    winrate = 0
                    if len(tmp_horse.loc[(tmp_horse["res_win"] == 1)]) != 0:
                        wins_len = len(tmp_horse.loc[(tmp_horse["res_win"] == 1)])
                        winrate = (wins_len/len(tmp_horse))
                    tmp_horse_comparison[key] = winrate

            #Tar fram summan av alla priser delat med längden av dataframet för varje häst.
            elif y == "avg_prize":
                for key in tmp_dict.items():
                    tmp_horse = betting_data.loc[(betting_data['horseName'] == key) & (betting_data['date'] < date)]
                    try:
                        avg_prize = (tmp_horse["prize"].sum()/len(tmp_horse))
                    except:
                        avg_prize = None
                    tmp_horse_comparison[key] = avg_prize

            #Summerar totala summan av priset för tidigare race för varje häst.
            elif y == "tot_prize":
                for key in tmp_dict:
                    tmp_horse = betting_data.loc[(betting_data['horseName'] == key) & (betting_data['date'] < date)]
                    tot_prize = (tmp_horse["prize"].sum())
                    tmp_horse_comparison[key] = tot_prize
            #Tar bort nan, därefter tar man fram högsta och minsta värdet i dictionary. Därefter jämför man dessa, om de är lika stora får alla hästar "vikten"
            tmp_horse_comparison = delete_nan(tmp_horse_comparison)            
            max_value = max(tmp_horse_comparison.values())
            min_value = min(tmp_horse_comparison.values())
            print(tmp_horse_comparison)
            if max_value == min_value:
                for key in tmp_dict:
                    tmp_dict[key] = tmp_dict[key]+(1*float(bettingcolumns[y]))
                    tmp_dict[key] = tmp_dict[key] + float(bettingcolumns[y])
            #Annars beräknas procenten genom att ta (hästensvärde - minsta värde) delat med (största värdet - minsta värdet). Därefter multipliceras procenten med vikten.
            else:
                for key in tmp_dict:
                    tmp_dict[key] = tmp_dict[key]+ ((tmp_horse_comparison[key]-min_value)/(max_value-min_value))*float(bettingcolumns[y])
        print(tmp_dict)
        #Om två hästar har lika mycket poäng, tar man ut en slumpmässigt.
        #Annars hästen med högst värde i slutliga poängsystemet väljs ut, programmet skriver ut hästen och raceid.
        #Därefter lagras resultatet av racet i listan wins och oddsen i listan odds.
        max_value = float(max(tmp_dict.values()))
        min_value = float(min(tmp_dict.values()))
        if max_value == min_value:
            highest_scored_horse = sample(tmp_dict.keys(), 1)
        else:
            highest_scored_horse = max(tmp_dict, key=tmp_dict.get)
        print("Race: {}  Horse: {}".format(randomly_chosen_races[x],highest_scored_horse))
        wins.append(tmp_df.loc[(betting_data["horseName"] == highest_scored_horse), "res_win"].values[0])
        odds.append((1/tmp_df.loc[(betting_data["horseName"] == highest_scored_horse), "decimalPrice"].values[0]))
    #Om fler än 0 tester har utförts, skrivs antal race, antal vinster och procentuell vinstchans av modellen.
    if len(wins) != 0:
        print("Races: {}\nWins: {}\nWinrate: {}".format(len(wins),wins.count(1),wins.count(1)/len(wins)))
    return wins, odds

#Funktionen låter användaren välja en av 3 olika bankroll management metoder och visualisering av ekonomiska balansen.
#Metod 1: Användaren väljer storleken på varje bet, därefter beräknas balansen. Om hästen har vunnit multipliceras bet storleken med oddsen.
#Annars har man förlorat bet storleken och slutligen skrivs ut hela balansen.
#Metod 2: Användaren skriver in ekonomiska balansen och därefter väljer procentuella ansatsen för varje bet.
#Metod 3: Martingale system dubblar betstorleken vid varje förlust. Om man vinner går man tillbaka till vanliga betstorlek. 
#Visualisering: Graf visualiserar resultatet efter varje bet.
def results(results_array,odds):
    while (True):
        Balance = 0
        print("\n1.Constant betsize \n2.Percentual betsize depending on your balance \n3.Martingale \n4.Show graph \n5.Go back")
        decision = validate_input("int")
        if decision == 1:
            print("\n What's the betsize?")
            Balance_graph = []
            betsize = validate_input("float")
            for x in range(len(results_array)):
                if results_array[x] == 1:
                    Balance += betsize*odds[x]
                else:
                    Balance -= betsize
                Balance_graph.append(Balance)
            print("Your balance is : {}".format(Balance))
        elif decision == 2:
            print("\nBalance")
            Balance_graph = []
            Balance = validate_input("float")
            print("\nProcentual betsize write in decimals. Example (0.65 = 65%)")
            percentage = validate_input("float")
            if 0 < percentage <= 1:
                for x in range(len(results_array)):
                    if results_array[x] == 1:
                        Balance += (Balance*percentage)*odds[x]
                    else:
                        Balance -= (Balance*percentage)
                    Balance_graph.append(Balance)
                print("Your balance is : {}".format(Balance))
            else: 
                print("Percentage should be bigger than 0 and smaller or equal to 1.")
        elif decision == 3:
            print("\n What's the betsize?")
            Balance_graph = []
            betsize = validate_input("float")
            tmp_betsize = betsize
            for x in range(len(results_array)):
                if results_array[x] == 1:
                    Balance += tmp_betsize*odds[x]
                    tmp_betsize = betsize
                else:
                    Balance -= tmp_betsize
                    tmp_betsize = tmp_betsize*2
                Balance_graph.append(Balance)
            print("Your balance is : {}".format(Balance))
        elif decision == 4:    
            plt.plot(list(range(1,len(Balance_graph)+1)),Balance_graph)
            plt.ylabel("Balance in Dollars")
            plt.xlabel("Number of races")
            plt.title("Balance")
            plt.show()
        elif decision == 5:
            return False
        else:
            print("Wrong input")

#Huvudmeny för programmet, användaren måste först välja parametrar i 1, därefter sätta vikt på de i 2.
#Efter man har utfört de 2 stegen, kan man testa modellen mot riktig data i 3.
#När man har fått resultat testerna kan man visualisera och få fram vinsten i 4. 
#Om 5 matas in avslutas programmet. 
def HorseBetting(dataframe, bettingparameters):
    choice_3 = 0
    choice_2 = 0
    while (True):
        print("\n1. Choose your parameters \n2. Set value for your parameters \n3. Test your parameters\n4. Choose betsize\n5. End program")
        choice = validate_input("int")
        if choice == 1:
            bettingparameters = add_parameters(bettingparameters)
        elif choice == 2:
            if len(bettingparameters) == 0:
                print("There are no parameters to change")
            else:
                bettingparameters = change_parameters(bettingparameters)
                choice_2 = 1
        elif choice == 3:
            if choice_2 == 0:
                print("You need to do step 2")
            else:
                wins, odds = horse_betting_test(bettingparameters, dataframe)
                choice_3 = 1
        elif choice == 4:
            if (choice_3 == 1):
                results(wins,odds)
            else:
                print("You need to do step 3")
        elif choice == 5:
            return

#För att starta programmet, läses data filen in med allt häst info, det skapas även en kolumn med datum och slutligen skickas allt till en
#funktion som är en huvudmeny.
if __name__ == "__main__":
    path = 'C:\\Users\\damia\\Desktop\\Betting\\DVGB06Betting\\'
    bettingcolumns = {}
    betting_data = pd.read_csv(path+'\\Bettingdata2.csv')
    betting_data["Year"] = betting_data["Year"].map(convertdate)
    betting_data["date"] = pd.to_datetime(betting_data[["Year","Month","Day"]])
    HorseBetting(betting_data, bettingcolumns)
