import webbrowser, pywhatkit,time, random

def OpenPage(URL):
    webbrowser.open(URL)

def VidOpen(Name):
    print("Opening...")
    time.sleep(3)
    pywhatkit.open(Name)

def Game_Madlib(Adjective,Verb,Place):
    print("The",Adjective,Verb,"On",Place)

def Game_Story(UserName):
 print(f"""Once upon a time there was a powerful orb that could change what ever the holder wants and a villian
   called Shreiker wants it. in the realm of the orb there is only one person who does not agree to give the power to Shreiker and the name of the 
    person who told it is {UserName}. He cahnged the orb to his control and then destroyed Shreiker.""")