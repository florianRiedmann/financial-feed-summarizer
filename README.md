# financial-feed-summarizer

#### Challenge
Publishers share information about company activities ad-hoc, such as insider trades, company earnings or institutional investments. (see google search: “AAPL price target” For news publishers it is often about the speed/reliability of publishing such standartized news. Often the information between two published articles is similar. NLP has progressed in the past years and algorithms can identify similarities within texts automatically and summarize, reshape and create text for informational purposes. The goal of this project is to generate “unique” text ad-hoc for company events such as insider trades, company earnings etc. by using several financial data sources as input.  

#### Solution
 Solution
Create a solution that captures text from many different rss feeds and generates short summaries that is publishable.  

#### Approach

* Crawl several financial feeds
* Determine similar texts and select the most important information
* Merge text based on rules and generate readable “new” text
* Use “Readability Algorithms” to determine readability -> Text has to be readable to person

#### Data set description  
Financial news sites are publishing via an rss feed current happenings. These feeds provide a practical approach to scrape and match news and generate publishable text.
