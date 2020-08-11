# YouTube click prediction

## "Show me your YouTube Home page and I tell you what you will click"

Experimenting with NLP and machine learning.
Based on thumbnail information on your YouTube Home page (signed out), i.e. your
recommendations, predict what video the user will click on next.

First baseline:
Scrape info, store in DB, use titles, train FastText, compute how similar the scraped
titles are to everthing seen AND clicked so far.

Rright now only English and German, only Firefox, only FastText model.

### Dependiencies/Preparation:

```bash
pip3 install pandas numpy matplotlib seaborn sklearn nltk gensim selenium
```

- for german:
```bash
pip3 install HanTa
```
Download file https://github.com/wartaal/HanTa/blob/master/HanTa/morphmodel_ger.pgz

In a python terminal run:
```python
import nltk
ntlk.download()
```

Select the corpora and packages options. Also enter the download path into CONFIG.

Download selenium driver for FF for you version:
https://github.com/mozilla/geckodriver/releases

Enter the other data in CONFIG.

### Run
 Call
 ```bash
 ./main
 ```

Click YTScrape, choose title from list and double click (or click button).

### TODO:
- Make notebook to visualize your YouTube "word bubble"
- Incorporate views, clicks, upload time
- Try soft cosine similarity
- Don't use average of clicked vids. - Make robust against "outlier clicks"
- don't use selenium. Use JS mokey script in "normal" browser.
- Fix issues:
  * speed everything up (scraping, browser and GUI startup)
  * Frequent very bad language guesses by nltk
  * Bad lemmatization
  * Character problems when inserting in tkinter listbox
  * Covid section sometimes has different css selector
  * Upload time (e.g. Streamed x y ago) in different CSS element sometimes.
