import os

from analyzer import com_classfiction
from analyzer.com_classfiction import classify_comments
from keras.metrics import accuracy

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import pandas as pd
from analyzer.data_processing import ModelCreator
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
        print("Start page analysis (s) , Options (o) , Help (h) , Quit(q)")

    def quit_(self):
        print("thank you for using our application... see you later")
        exit() 
    
    def valid_page(self):
        print('Enter FaceBook Page Name :  ')
        self.page_name = input(" > ")
        return self.scraper.page_info(self.page_name)        
    
 
    def user_menu_choice(self):
        inpts = ['q','s','o','h']
        self.choice = input(" > ")
        if self.choice in inpts:
                
            if self.choice == "q":
                self.quit_()
            if self.choice == "s":
                if self.valid_page():
                    print('Found this page {}'.format(self.page_name))
                    print('')
                    print('Press (Enter) to continue , (r)e-enter page name')
                    choice = input( " > " ).lower()
                    
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
                        print('to do that , press ( ENTER ) (q) to quit')
                        choice = input(" > ")
                        
                        if choice == "q":
                            self.quit_()
                        
                        top = self.scraper.commenters(self.page_name)
                        print(
                            colored(
                                (top),
                                "cyan",
                            )
                        )
                        self.user_menu_choice()
                    else:
                        print('')
                        print("\u001b[34m1\u001b[37m  (Fast)   \u001b[34m2\u001b[37m  (Slow)   ")
                        print("-------------------------")
                        print('')
                        print('Select prediction accuracy mode (\u001b[34m1\u001b[37m) OR (\u001b[34m2\u001b[37m)')
                        accuracy_levl = input(" > ").lower()
                        
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
                                self.most_commenter()
                                after_analysis()
                                

                            if user_input.lower() == "q":
                                quit()
            
                        after_analysis()
                
                else:
                    print("invalid page name..",self.page_name)
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
        else:
            print('invalid input .. chose from the options below')
            self.start()
            self.user_menu_choice()
