import requests
import bs4


def main():
    res = requests.get('http://www.rotoworld.com/')
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    reports = []
    impacts = []
    dates = []
    final = []
    for date in soup.findAll(attrs={'class': 'date'}):
        # to get rid of dates we don't care about
        if '-' in date.contents[0]:
            dates.append(date.contents[0])
    for report in soup.findAll(attrs={'class': 'report'}):
        reports.append(report.contents[1].getText())
    for impact in soup.findAll(attrs={'class': 'impact'}):
        impacts.append(impact.contents[0].strip())

    # roto stuff on the first entry that we don't need
    impacts.pop(0)
    for i in range(len(reports)):
        final.append("REPORT:")
        final.append(reports[i])
        final.append("IMPACT:")
        final.append(impacts[i])
        final.append("DATE:")
        final.append(dates[i])


main()
