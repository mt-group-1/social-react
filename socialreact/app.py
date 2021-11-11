import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import pandas as pd
from analyzer.data_processing import ModelCreator
from analyzer.predictions import predict_post
from tensorflow import keras
from termcolor import colored


class App:
    def __init__(self, scraper):
        """
        docs
        """
        self.user_name = None
        self.user_input = None
        self.page_name = None
        self.scraper = scraper()

    def start(self):
        print(
            colored(
                (
                    "Start page analysis (s) , Post impact prediction (i) , Help (h) , Quit(q)"
                ),
                "white",
            )
        )

    def user_menu_choice(self):
        def quit():
            print(
                colored(
                    ("thank you for using our application... see you later 👋"),
                    "cyan",
                )
            )
            exit()
        def most_commenter():
            """
            Sub method that get the most commenter user on a given page.
            """
            top = self.scraper.commenters(self.page_name)
            print(
                colored(
                    (top),
                    "cyan",
                )
            )
        def valid_page():
            self.page_name = input("Enter FaceBook Page Name :  > ")
            return self.scraper.page_info(self.page_name)
        
        self.choice = input(" > ")
        if self.choice == "q":
            quit()
        if self.choice == "s":
            if valid_page():
                print(colored(("Found this page  ✔️ "),"cyan", ),self.page_name,)
                print('')
                page_info = ""
                page = self.scraper.page_details
                for key in page:
                    page_info += "{} : {} ".format(str(key), page[key])
                print(page_info, "\n")
                choice = input( "Press (Enter) to continue , (r)e-enter page name > " ).lower()
                
                if choice == "r":
                    self.start()
                    self.user_menu_choice()
                
                # ! validate fetched posts length
                length = self.scraper.fb_page_posts(self.page_name)
                if length < 200:
                    print("The page entered do not have enogh content")
                    print("Which will lead to inaccurate prediction results..")
                    print("-" * 80)
                    print("But we can show you the most common commenter")
                    choice = input("to do that , press ( ENTER ) (q) to quit > ")

                    
                    if choice == "q":
                        quit()
                    
                    most_commenter()
                else:
                    model = ModelCreator(self.page_name)
                    impact = model.page_comments()
                    print(impact)
                    model.keras()
                    X_train, X_test, Y_train, Y_test = model.keras_rp

                    if os.path.isfile("./data/%s/saved_model.pb" % self.page_name):
                            model = keras.models.load_model("./data/%s/" % self.page_name,compile=True)
                            model_score, model_accuracy = model.evaluate(X_train, Y_train, verbose=2)
                            print(model_score, model_accuracy)
                            self.model = model
                    else:
                        model.keras_model()
                        model_score, model_accuracy = model.train_model()
                        print(model_score, model_accuracy)
                        model.save_the_model()
                        self.model = model
                    
                    
                    def after_analysis():
                        print("(e)nter a post to predict impact , (m)ost commenter , (q)uit ")

                        user_input = input(" > ")
                        if user_input.lower() == "e":
                            post_text = input("Type your Post: ")
                            # TODO[]: validate post_text data
                            if len(post_text) > 10 :
                                
                                result = "".join([i for i in post_text if not i.isdigit()])
                                prediction = predict_post(result, self.page_name, self.model)
                                # print(prediction)
                            else:
                                after_analysis()    
                           
                            after_analysis()

                        if user_input.lower() == "m":
                            most_commenter()
                            after_analysis()
                            

                        if user_input.lower() == "q":
                            quit()
           
                    after_analysis()
            else:
                print(colored(("invalid page name..  ❌ "),"cyan",),self.page_name,)
                self.choice = input("Press (Enter) to continue , (q) to Quit  > " ).lower()

                if self.choice == "q":
                    quit()
                else:
                    self.start()
                    self.user_menu_choice()
        if self.choice == "i":
            print("(e)nter a post to predict impact , (m)ost commenter , (q)uit ")
            post_text = input(" : ")
            if self.exists:
                model = self.this_model
            
            predict_post(post_text, self.page_name, model)
        if self.choice == "h":
            print(colored(("Social react provides services to know the impact of a post that you want by entering the letter (i), also you can know the influance of your page by entering the letter (s), if you want to quit just enter the letter (q), Happy to have you here! "),"cyan"))
            self.user_menu_choice()
            

            
