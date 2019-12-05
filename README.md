# financial-feed-summarizer

https://seekingalpha.com/market-news  
https://www.bloomberg.com  
https://www.ft.com  
https://www.investing.com  
https://www.marketwatch.com/latest-news  


#### Challenge
Public sentiment is driving news sources. Especially news headlines/content that polarizes leave a mass amount of comments from readers. Currently there are teams that review content based on hateful comments. However, currently sentiment scores are not used to determine if news comments are almost in line with guidelines.  

#### Solution
Create a sentiment score to analyse news comments.  

#### Approach
* Get comments from public news site/twitter, which are reactions to current news events
* Create a sentiment score based on that comment and rank the comments from hateful to nice
* Calculate a sentiment score for the news topic and predict the score for new news headlines  

#### Data set description  
 News feeds, APIs or social media
