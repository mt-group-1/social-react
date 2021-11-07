# Software Requirements
## Vision
We are aiming to create an analizer for facebook pages becouse there is no free user friendly service that provide facebook page owner with a sentement analysis and predict if a given post would have a positive or negative impact on his page.

## Scope (In/Out)
+ IN
    - `SocialReact` will provide the user a service to enter facebook page name the he want to analize it 
    - `SocialReact` will reports the user that the page name entered is avilable or not 
    - `SocialReact` will provide the user another service to write a post to see if it have positive or negative impact 
+ OUT 
    - `SocialReact` will not provide this service for not English pages 

### Minimum Viable Product vs Stretch
+ Minimum Viable Product 
    - Entering facebook page name and analize it 
    - Entering a post to predicte the impact of the post in that page  
+ Stretch
    - Positive or negative impact for a specific user on a page 
    - provide a link to view visualize data 

## Functional Requirements
1. A user can enter facebook page name and get there analysis for that page 
2. A user can informed whether or not the page avilable or not 
3. A user can enter a post and get a predection for the impact of the post .

**Data flow :**
![df](https://media.discordapp.net/attachments/860864369586601999/906908043915198545/wf.JPG?width=984&height=670)
## Non-Functional Requirements

1. **Testability**: most program function covered in testing for different scenarios ,so each input cases from the user handled in test case  
2. **Usability** : the service was simple and easy to use ,so that the user when the user start using the program he will have a clear and specefic prompt messages and results
