from analyzer.predictions import predict_post
from analyzer.data_processing import get_data
from fetch_posts.functions import validate_page
def get_user_input():
    print("Welcome To SocialReact.")
    user_input = input("To analyze facebook page page enter (p), to predict post impact on the given page enter (i), to quit enter (q) > ")
    
    if user_input == 'q':
        exit()
    elif user_input == 'p':
        fb_page_name = input("Enter Facebook page Name > ")
        result = validate_page(fb_page_name)
        print(result)
        
        if result : 
            get_data(fb_page_name)
        else:
            print("Invalid page name")
            get_user_input()

    elif user_input == 'i':
        post_= input("Enter a post you want tp predict > ")

        post_result=check_post_words(post_)

        if post_result:
            predict_post(post_result)
        else:
            print("Your post contains invalid english words")
   
# def check_page_info(page_name):
#     """
#     This function uses a dictonary that detect if the page name has a valid english name or not 

#     Args:
#         page_name: String

#     Returns:
#         Boolean
#     """
#     pages = ['Renad','shahed','majed']
    
#     if page_name in pages:
#         return True
#     else:
#         return False

def check_post_words(post_):
    """
    This function is resposiable for checking the post given if its an english valid or invalid

    Args:
        post_: String
    
    Returns:
        Boolean,True if the page name is valid, False if the post is invalid
    """
    test = "This text for testing"
    if post_ in test:
        return True
    else:
        return False
# get_user_input()