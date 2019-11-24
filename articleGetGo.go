package main

import (
	"encoding/csv"
	"encoding/xml"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"regexp"
	"sync"
	"time"
)

type RTItems struct {
	XMLName xml.Name `xml:"rss"`
	RTItems []RTItem `xml:"channel>item"`
}

type RTItem struct {
	Title string `xml:"title"`
}

type GUARDIANItems struct {
	XMLName       xml.Name       `xml:"urlset"`
	GUARDIANItems []GUARDIANItem `xml:"url"`
}
type GUARDIANItem struct {
	Title string `xml:"loc"`
}

// For CNN and BBC
type Items struct {
	XMLName xml.Name `xml:"rss"`
	Items   []Item   `xml:"channel>item"`
}
type Item struct {
	XMLName     xml.Name `xml:"item"`
	Title       string   `xml:"title"`
	Description string   `xml:"description"`
}

// RT and Guardian need their own structs
// and parsing, namespaces involved for Guardian

func getPage(feedUrl string, section string, siteName string) {
	res, err := http.Get(feedUrl)
	if err != nil {
		log.Fatal(err)
	}

	wholeXML, err := ioutil.ReadAll(res.Body)
	if err != nil {
		log.Fatal("Error putting file into buffer\n")
	}
	if siteName == "BBC" {
		var BBCItemsStruct Items
		xml.Unmarshal(wholeXML, &BBCItemsStruct)
		writeCSV("BBC", section, BBCItemsStruct)
		fmt.Printf("[BBC] - %s\n", section)

	} else if siteName == "CNN" {
		var CNNItemsStruct Items
		xml.Unmarshal(wholeXML, &CNNItemsStruct)
		writeCSV("CNN", section, CNNItemsStruct)
		fmt.Printf("[CNN] - %s\n", section)

	} else if siteName == "RT" {
		var RTItemsStruct RTItems
		xml.Unmarshal(wholeXML, &RTItemsStruct)
		writeRTCSV("RT", section, RTItemsStruct)
		fmt.Printf("[RT] - %s\n", section)

	} else if siteName == "GUARDIAN" {
		var GUARDIANItemsStruct GUARDIANItems
		xml.Unmarshal(wholeXML, &GUARDIANItemsStruct)
		fmt.Printf("Unmarshalled: %s\n", GUARDIANItemsStruct)
		writeGUARDIANCSV("GUARDIAN", section, GUARDIANItemsStruct)
	}
}

func writeGUARDIANCSV(siteName string, section string, correctStruct GUARDIANItems) {
	dontWrite := false
	writeTo := fmt.Sprintf("%s.csv", siteName)
	currTime := time.Now()
	timeString := fmt.Sprintf("%d/%d/%d", currTime.Day(), currTime.Month(), currTime.Year())

	csvFile, err := os.OpenFile(writeTo, os.O_APPEND|os.O_CREATE|os.O_WRONLY, os.ModeAppend)
	defer csvFile.Close()
	if err != nil {
		log.Fatal(err)
	}
	csvWriter := csv.NewWriter(csvFile)
	defer csvWriter.Flush()

	for i := 0; i < len(correctStruct.GUARDIANItems); i++ {
		if len(correctStruct.GUARDIANItems[i].Title) < 1 {
			dontWrite = true
		}

		if !dontWrite {
			// regexMatch := regexp.MustCompile(`[<](.)+[>]`)
			// descString := regexMatch.ReplaceAllString(correctStruct[i].Description, "")
			descString := "eee"
			if len(descString) < 1 {
				res := []string{timeString, section, correctStruct.GUARDIANItems[i].Title, "nothing"}
				err := csvWriter.Write(res)

				if err != nil {
					log.Fatal("Can't write to file", err)
				}
			} else {
				res := []string{timeString, section, correctStruct.GUARDIANItems[i].Title, descString}
				err := csvWriter.Write(res)
				if err != nil {
					log.Fatal("Can't write to file", err)
				}

			}
		}
	}
}

func writeCSV(siteName string, section string, correctStruct Items) {
	dontWrite := false
	writeTo := fmt.Sprintf("%s.csv", siteName)
	currTime := time.Now()
	timeString := fmt.Sprintf("%d/%d/%d", currTime.Day(), currTime.Month(), currTime.Year())

	csvFile, err := os.OpenFile(writeTo, os.O_APPEND|os.O_CREATE|os.O_WRONLY, os.ModeAppend)
	defer csvFile.Close()
	if err != nil {
		log.Fatal(err)
	}
	csvWriter := csv.NewWriter(csvFile)
	defer csvWriter.Flush()

	for i := 0; i < len(correctStruct.Items); i++ {
		if len(correctStruct.Items[i].Title) < 1 {
			dontWrite = true
		}

		if !dontWrite {
			regexMatch := regexp.MustCompile(`[<](.)+[>]`)
			descString := regexMatch.ReplaceAllString(correctStruct.Items[i].Description, "")
			if len(descString) < 1 {
				res := []string{timeString, section, correctStruct.Items[i].Title, "nothing"}
				err := csvWriter.Write(res)

				if err != nil {
					log.Fatal("Can't write to file", err)
				}
			} else {
				res := []string{timeString, section, correctStruct.Items[i].Title, descString}
				err := csvWriter.Write(res)
				if err != nil {
					log.Fatal("Can't write to file", err)
				}

			}
		}
	}
}

func writeRTCSV(siteName string, section string, correctStruct RTItems) {
	dontWrite := false
	writeTo := fmt.Sprintf("%s.csv", siteName)
	currTime := time.Now()
	timeString := fmt.Sprintf("%d/%d/%d", currTime.Day(), currTime.Month(), currTime.Year())

	csvFile, err := os.OpenFile(writeTo, os.O_APPEND|os.O_CREATE|os.O_WRONLY, os.ModeAppend)
	defer csvFile.Close()
	if err != nil {
		log.Fatal(err)
	}
	csvWriter := csv.NewWriter(csvFile)
	defer csvWriter.Flush()

	for i := 0; i < len(correctStruct.RTItems); i++ {
		if len(correctStruct.RTItems[i].Title) < 1 {
			dontWrite = true
		}

		if !dontWrite {
			// regexMatch := regexp.MustCompile(`[<](.)+[>]`)
			// descString := regexMatch.ReplaceAllString(correctStruct.RTItems[i].Description, "")
			descString := "e"
			if len(descString) < 1 {
				res := []string{timeString, section, correctStruct.RTItems[i].Title, descString}
				err := csvWriter.Write(res)

				if err != nil {
					log.Fatal("Can't write to file", err)
				}
			} else {
				res := []string{timeString, section, correctStruct.RTItems[i].Title, "e"}
				err := csvWriter.Write(res)
				if err != nil {
					log.Fatal("Can't write to file", err)
				}

			}
		}
	}
}

func scrapeBBC(id int, waitG *sync.WaitGroup) {
	BBCList := []string{"world", "uk", "business", "politics", "health",
		"education", "science_and_environment", "technology", "entertainment_and_arts",
		"world/africa", "world/asia", "world/europe", "world/latin_america", "world/middle_east",
		"world/us_and_canada", "england", "northern_ireland", "scotland", "wales"}

	for _, dir := range BBCList {
		currUrl := fmt.Sprintf("http://feeds.bbci.co.uk/news/%s/rss.xml", dir)
		getPage(currUrl, dir, "BBC")
	}
	waitG.Done()
}

func scrapeCNN(id int, waitG *sync.WaitGroup) {
	CNNList := []string{"edition", "edition_world", "edition_africa", "edition_americas",
		"edition_asia", "edition_europe", "edition_meast", "edition_us", "money_news_international",
		"edition_technology", "edition_space", "edition_entertainment", "edition_sport",
		"edition_football", "edition_golf", "edition_motorsport", "edition_tennis"}

	for _, dir := range CNNList {
		currUrl := fmt.Sprintf("http://rss.cnn.com/rss/%s.rss", dir)
		getPage(currUrl, dir, "CNN")
	}
	waitG.Done()
}

// func scrapeGuardian(id int, waitG *sync.WaitGroup) {
func scrapeGuardian() {

	currUrl := "https://www.theguardian.com/sitemaps/news.xml"
	getPage(currUrl, "guardian", "GUARDIAN")

	// waitG.Done()
}

func scrapeRT(id int, waitG *sync.WaitGroup) {
	RTList := []string{"news", "uk", "usa", "sport", "russia", "business"}

	for _, dir := range RTList {
		currUrl := fmt.Sprintf("https://www.rt.com/rss/%s", dir)
		getPage(currUrl, dir, "RT")
	}
	waitG.Done()
}

func main() {
	var waitG sync.WaitGroup
	waitG.Add(1)
	go scrapeBBC(1, &waitG)
	waitG.Add(1)
	go scrapeCNN(1, &waitG)

	// scrapeGuardian()

	// waitG.Add(1)
	// go scrapeRT(1, &waitG)
	waitG.Wait()
	fmt.Printf("\nDone!\n")

	// getPage("https://iamcathal.github.io")
}
