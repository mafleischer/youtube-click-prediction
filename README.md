# YouTube click prediction

## "Show me your YouTube Home page and I tell you what you will click"

Experimenting with NLP and machine learning.
Based on thumbnail information on your YouTube Home page (signed out), i.e. your
recommendations, predict what video the user will click on next.

First baseline:
Scrape info, store in DB, use titles, train FastText, compute how similar the scraped
titles are to everthing seen AND clicked so far.

- Dependiencies/Preparation:

pip3 install pandas numpy matplotlib seaborn sklearn nltk gensim selenium

In a python terminal run:
import nltk
ntlk.download()

Select the corpora and packages options. Also enter the download path into CONFIG.


- for german:
pip3 install HanTa
Download file https://github.com/wartaal/HanTa/blob/master/HanTa/morphmodel_ger.pgz

### Run
 Call ./main

# TODO:
- Make notebook to visualize your YouTube "word bubble"
- Incorporate views, clicks, upload time
- Fix issues:
  * Frequent very bad language guesses by nltk
  * Bad lemmatization
  * Character problems when inserting in tkinter listbox
  * Covid section sometimes has different css selector
  * Upload time (e.g. Streamed x y ago) in different CSS element sometimes.