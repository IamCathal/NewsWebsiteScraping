# News Article Scraper

I wrote this script as a means of automatically collecting my own dataset of article titles and their subjects from a handful of different news outlets.

### Where does the script get it's articles from?

The script takes all articles from the RSS feeds of the Guardian, BBC, RT and CNN. The reason it takes articles from the RSS feeds as it's much simpler to parse the XML format instead of the jumbled up and often-times confusing HTML format. I originally scraped articles from their regular HTML format using beautiful soup in python but the slightest of changes to the website formats messed it up and the logic behind the extracting of information was quite convoluted.

### Usage
No external dependencies are required so you can go right ahead and run the scripts.
#### Go
`go run articleGet.go`

#### Python
`python articleGet.py`

### Go vs Python

I initially wrote this script in python because it was the most straight forward way of doing it at the time. However more recently having started to pick up go I've been curious as to how much faster it can do the same task. Go is a compiled language so it would have an inherant advantage but I just wanted to rub it in. I timed the execution of the scripts and heres the averages of the time taken to run the script on both python and go.

Go | Python
------------ | -------------
1.2s | 12.8s

So, yeah. ❤️ Go ❤️

### What is the point of this?

After a few months when I have a few thousand articles from every category I'll analyse the patterns and trends in topics and phrases etc.

### Contributing

In the unlikely event you'd want to contribute to this project and perhaps extend it's funtionality, fix a bug or get rid of some whitespace go ahead and make a PR and I'd be glad to review it.
