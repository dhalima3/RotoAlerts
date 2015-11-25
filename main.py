import requests, bs4

def main():
    res = requests.get('http://www.rotoworld.com/')
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    reports = []
    impacts = []
    final = []
    for report in soup.findAll(attrs={'class' : 'report'}):
        reports.append(report.contents[1].getText())
    for impact in soup.findAll(attrs={'class' : 'impact'}):
        impacts.append(impact.contents[0].strip())

    # roto stuff on the first entry that we don't need
    impacts.pop(0)
    for i in range(len(reports)):
        final.append("REPORT:")
        final.append(reports[i])
        final.append("\n")
        final.append("IMPACT:")
        final.append(impacts[i])



main()
