
from termcolor import colored

def welcome_msg():
    s_r = """
   _____            _       __   ____                  __ 
  / ___/____  _____(_)___ _/ /  / __ \___  ____ ______/ /_
  \__ \/ __ \/ ___/ / __ `/ /  / /_/ / _ \/ __ `/ ___/ __/
 ___/ / /_/ / /__/ / /_/ / /  / _, _/  __/ /_/ / /__/ /_  
/____/\____/\___/_/\__,_/_/  /_/ |_|\___/\__,_/\___/\__/ 
    """
    print(s_r)
    print("Welcome social react")
    print("Where you can analyize any facebook page posts")
    print("======================================================================")
    print("Start page analysis (s) , Post impact prediction (i) , Help (h) , Quit(q)")


msg = """
   _____            _       __   ____                  __ 
  / ___/____  _____(_)___ _/ /  / __ \___  ____ ______/ /_
  \__ \/ __ \/ ___/ / __ `/ /  / /_/ / _ \/ __ `/ ___/ __/
 ___/ / /_/ / /__/ / /_/ / /  / _, _/  __/ /_/ / /__/ /_  
/____/\____/\___/_/\__,_/_/  /_/ |_|\___/\__,_/\___/\__/ 
    
Welcome social react
Where you can analyize any facebook page posts
======================================================================
Start page analysis (s) , Post impact prediction (i) , Help (h) , Quit(q)
"""


def start():
    print(
        "Start page analysis (s) , Post impact prediction (i) , Help (h) , Quit(q)"
    )

def quit_():
    print(
    "thank you for using our application... see you later 👋"
    )

def quit_program():
    exit()

welcome_msg()
start()
quit_()
# quit_program()