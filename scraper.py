import requests
import csv
from itertools import zip_longest
from bs4 import BeautifulSoup

dates = ["2020-03-13--2020-03-20","2020-03-20--2020-03-27", "2020-03-27--2020-04-03",
"2020-04-03--2020-04-10", "2020-04-10--2020-04-17", "2020-04-17--2020-04-24",
"2020-04-24--2020-05-01", "2020-05-01--2020-05-08", "2020-05-08--2020-05-15",
"2020-05-15--2020-05-22", "2020-05-22--2020-05-29", "2020-05-29--2020-06-05",
"2020-06-05--2020-06-12", "2020-06-12--2020-06-19"]
all_data = []

for d in dates:
    url = 'https://spotifycharts.com/regional/us/weekly/' + d
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    tb = soup.find('table', class_='chart-table')
    songs = []
    streams = []
    rows = tb.find_all('tr')[1:11] # first 10 songs

    for row in rows:
        for s in row.find_all('td', 'chart-table-track'):
            songs.append(s.find('strong').get_text())
        for st in row.find_all('td', 'chart-table-streams'):
            streams.append(st.get_text())
    all_data.append(songs)
    all_data.append(streams)


export_data = zip_longest(*all_data, fillvalue = '')
dupl_dates = []
for i in dates:
    dupl_dates.extend([i, i])

with open("output.csv","w",newline="") as f:
    cw = csv.writer(f)
    cw.writerow((dupl_dates))
    cw.writerows(export_data)
