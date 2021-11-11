import os

from analyzer import com_classfiction
from analyzer.com_classfiction import classify_comments
from keras.metrics import accuracy

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import pandas as pd
from analyzer.data_processing import ModelCreator
from analyzer.predictions import predict_post_
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
                    "Start page analysis (s) , Options (o) , Help (h) , Quit(q)"
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
                print('')
     
                
                
                
                
                choice = input( "Press (Enter) to continue , (r)e-enter page name > " ).lower()
                
                if choice == "r":
                    self.start()
                    self.user_menu_choice()
                
                
                classify_comments("./data/%s/comments.csv" % self.page_name, self.page_name)
                
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
                    print('')
                    print("\u001b[34m1\u001b[37m  (Fast)   \u001b[34m2\u001b[37m  (Slow)   ")
                    print("-------------------------")
                    print('')
                    accuracy_levl = input("Select prediction accuracy mode (\u001b[34m1\u001b[37m) OR (\u001b[34m2\u001b[37m) > ").lower()
                    
                    if accuracy_levl == '1':
                        from analyzer.analyzer import load_data
                        accuracy = load_data('./data/%s/classified_comments.txt ' % self.page_name)
                        print('')
                        print('The prediction accuracy for this page will be %.2f ' % accuracy)
                        print('')
                    elif accuracy_levl == '2':
                        model = ModelCreator(self.page_name)
                        impact = model.page_comments()
                        print("")
                        print(impact)
                        print("")
                        model.keras()
                        self.tokenizer = model.tokenizer
                        self.predict = model.predict_post
                        
                        X_train, X_test, Y_train, Y_test = model.keras_rp
                    
                        if os.path.isfile("./data/%s/saved_model.pb" % self.page_name):
                                model = keras.models.load_model("./data/%s/" % self.page_name)
                                model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])
                                model.evaluate(X_train, Y_train, verbose=2)
                                
                                print("")
                                self.model = model
                        else:
                            model.keras_model()
                            model.train_model()
                            model.save_the_model()
                            self.model = model
                    

                    def after_analysis():
                        print("(e)nter a post to predict impact , (m)ost commenter , (q)uit ")

                        user_input = input(" > ")
                        if user_input.lower() == "e":
                            post_text = input("Type your post here : ")
                            # TODO[]: validate post_text data
                            if len(post_text) > 10 :
                                from nltk.sentiment.vader import \
                                    SentimentIntensityAnalyzer
                                sid = SentimentIntensityAnalyzer()
                                results= sid.polarity_scores(post_text)
                                impact = ''
                                if results["compound"] >= 0.02:
                                    impact = 'This post will effect  \u001b[32mPositivly\u001b[37m in %s ' % self.page_name
                                elif results["compound"] <= -0.02:
                                    impact = 'This post will effect \u001b[31mNegativly\u001b[37m in %s ' % self.page_name
                                else:
                                    impact = 'This post will not have major effect in %s ' % self.page_name
                                
                                print(impact)
                            else:
                                print('')
                                print('Please retype a post with more meaning full sentences .')
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
        if self.choice == "o":
            
            self.page_name = input('Enter FB page name > ').lower()

            classify_comments("./data/%s/comments.csv" % self.page_name, self.page_name)

            after_analysis()
        
        if self.choice == "h":
            # TODO[]: pronpt the user for help
            pass
