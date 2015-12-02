import requests
import bs4
import smtplib
import datetime
from twilio.rest import TwilioRestClient
from secrets import *


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
    updates = get_updates(reports, impacts, dates)
    final = format_email(updates)

    print final
    if not final:
        send_email(final)


def get_updates(reports, impacts, dates):
    updates = []
    current_time = datetime.datetime.now().time()
    for i in range(len(reports)):
        date_split = dates[i].split()
        time_split = map(int, date_split[3].split(":"))
        am_or_pm = date_split[4]
        hour = time_split[0] + 12 if (am_or_pm == "PM") else time_split[0]
        # minute = time_split[1]
        if (current_time.hour - hour == 0) and (current_time.minute - minute <= 7):
            updates.append("REPORT: " + reports[i])
            updates.append("IMPACT: " + impacts[i])
            updates.append("DATE: " + dates[i])
    return updates


def format_email(updates):
    final = ""
    #final = "From: " + email_username + "<" +  email_username + ">\n"
    #final += "To: To Person <" + destination_email + ">\n"
    #final += "Subject: Fantasy Football Alert\n"
    updates = map(str, updates)
    for i in range(len(updates)):
        final += updates[i] + '\n'
        if ((i+1) % 3 == 0):
            final += '====================================================\n'
    return final


def send_email(updates):
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.ehlo()
    server.starttls()
    server.login(email_username, email_password)
    server.sendmail(email_username, destination_email, updates)
    server.quit()


def send_text_alert(updates):
    account_sid = "ACXXXXXXXXXXXXXXXXX"
    auth_token = "YYYYYYYYYYYYYYYYYY"
    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(to="+12316851234", from_="+15555555555",
                                        body="Hello there!")


main()
