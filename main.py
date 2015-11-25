import requests, bs4

def main():
    res = requests.get('http://www.rotoworld.com/')
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    reports = []
    impacts = []
    for report in soup.findAll(attrs={'class' : 'report'}):
        reports.append(report.contents[1].getText())
    for impact in soup.findAll(attrs={'class' : 'impact'}):
        impacts.append(impact.contents[0].strip())


main()
