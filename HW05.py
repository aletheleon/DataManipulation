import re, requests, json
from pprint import pprint
from bs4 import BeautifulSoup

''' Please input your unique API key from OpenWeatherMap as a string into the global API_KEY variable '''
API_KEY = "eb0dae546a500c53503a4ae681c9c4a1"

def country_statistics(country):
    country_data = requests.get(f"https://restcountries.eu/rest/v2/name/{country}?fullText=true")
    if country_data.status_code is 200:
        country_data = country_data.json()[0]
        country_dict = {}
        country_dict['country'] = country_data['name']
        country_dict['capital'] = country_data['capital']
        country_dict['population'] = country_data['population']
        country_dict['coordinates'] = country_data['latlng']
        country_dict['timezone'] = country_data['timezones']
        country_dict['currency'] = country_data['currencies']
        country_dict['borders'] = country_data['borders']
        # pprint(country_dict)
        return(country_dict)
    else:
        return f'{country} is not a valid listed country from the API.'

def bordering_countries(country = "Japan"):
    country_data = requests.get(f"https://restcountries.eu/rest/v2/name/{country}?fullText=true")
    if country_data.status_code is 200:
        country_data = country_data.json()[0]
        border_countries = country_data['borders']
        if len(border_countries) is 0:
            return []

        borders_url = "https://restcountries.eu/rest/v2/alpha?codes="
        for code in border_countries:
            borders_url += code + ";"

        borders_data = requests.get(borders_url)
        border_countries = []
        for border in borders_data.json():
            border_countries.append(border['name'])

        # pprint(border_countries)
        return border_countries
    else:
        return f'{country} is not a valid listed country from the API.'

def weather_watcher(country, max_humidity):
    country_data = requests.get(f"https://restcountries.eu/rest/v2/name/{country}?fullText=true")
    if country_data.status_code is 200:
        country_data = country_data.json()[0]
        capital = country_data['capital']
        capital_data = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={capital}&appid={API_KEY}")
        if capital_data.status_code is 200:
            capital_data = capital_data.json()
            description = capital_data['weather'][0]['description']
            avg_temp = round((capital_data['main']['temp_max'] + capital_data['main']['temp_min']) / 2, 2)
            humidity = capital_data['main']['humidity']
            # pprint(capital_data)
            return (humidity <= max_humidity, f'The current forecast for {capital} is {description} with an average temperature of {avg_temp} Kelvin and humidity of {humidity}%.')
        else:
            return f'{country}\'s {capital} is not a valid listed capital from the API.'
    else:
        return f'{country} is not a valid listed country from the API.'

def most_visited_raw_list(file_name):
    return_list = []
    soup = BeautifulSoup(open(f'{file_name}.html', encoding='utf8'), 'html.parser')
    table = soup.find('table')
    header = table.find('tr').findAll('th')
    header_list = []
    for item in header:
        header_list.append(re.sub(r"[\n]|(\[\d\])", "", item.text))
    return_list.append(header_list)
    rows = table.findAll('tr')
    for row in rows:
        datas = row.findAll('td')
        if len(datas) > 0:
            data_list = []
            for data in datas:
                arrow_alt = ""
                if data.find('img') and len(data.img['alt']) > 1:
                    arrow_alt = data.img['alt'] + " "
                data_list.append(arrow_alt + re.search(r"[^ \xa0].*", data.text).group())
            return_list.append(data_list)
    # pprint(return_list)
    return return_list

def most_visited_cleaned_list(raw_list):
    for row in raw_list[1:]:
        row[0] = int(row[0])
        row[2] = int(float(re.match(r"[\d.]+", row[2]).group()) * 1000000)
        row[3] = int(float(re.match(r"[\d.]+", row[3]).group()) * 1000000)
        if 'Increase' in row[4]:
            row[4] = float(re.sub('Increase ', '', row[4]))
        elif 'Decrease' in row[4]:
            row[4] = float(re.sub('Decrease ', '-', row[4]))
        if 'Increase' in row[5]:
            row[5] = float(re.sub('Increase ', '', row[5]))
        elif 'Decrease' in row[5]:
            row[5] = float(re.sub('Decrease ', '-', row[5]))
    # pprint(raw_list)
    return raw_list

def receipt_list(file_name):
    return_list = []
    soup = BeautifulSoup(open(f'{file_name}.html', encoding='utf8'), 'html.parser')
    tables = soup.findAll('table')
    receipts_table = tables[6]
    header_list = []
    count = 0
    for item in receipts_table.find('tr').findAll('th'):
        print(str(item).strip('\xa0').strip('/t'))
        break
        ''' WHY DOESN'T THIS WORK '''
        temp = re.search(r"<th>(.+?)</th>", str(item).strip(), re.DOTALL).group()
        print(temp)
        if count in (0,1,3):
            temp = re.sub(r"<br/>|<p>", " ", str(item))
            temp = re.sub(r"((<.+?>)|(</.+?>))|\n|(\[\d\])", "", temp)
            temp = re.sub("  ", " ", temp)
            header_list.append(temp)
        count += 1
    return_list.append(header_list)
    for row in receipts_table.findAll('tr')[1:]:
        data_list = []
        count = 0
        for data in row.findAll('td'):
            if count is 0:
                data_list.append(int(data.text.strip()))
            elif count is 1:
                data_list.append(data.text.strip())
            elif count is 3:
                data_list.append(float(data.text.strip()))
            count += 1
        return_list.append(data_list)
    # pprint(return_list)
    return return_list

def expenditure_per_arrival(most_visited_list, expenditure_list, country):
    # if any(country in c_line for c_line in most_visited_list) and any(country in c_line for c_line in expenditure_list):
    arrivals = None
    for c_line in most_visited_list:
        if country in c_line[1]:
            arrivals = c_line[3]
    expenditure = None
    for c_line in expenditure_list:
        if country in c_line[1]:
            expenditure = c_line[2]
    if arrivals is not None and expenditure is not None:
        return int(round((expenditure * 1000000000) / arrivals, 0))
    else:
        return -1

def test_cases():
    country_stats = country_statistics('China')
    border_countries = bordering_countries('Japan')
    weather = weather_watcher('Japan', 55)
    raw_data = most_visited_raw_list('wiki_tourism')
    cleaned_data = most_visited_cleaned_list(raw_data)
    receipts = receipt_list('wiki_tourism')
    expenditures = expenditure_per_arrival(cleaned_data, receipts, 'Spain')

if __name__ == '__main__':
    test_cases()
