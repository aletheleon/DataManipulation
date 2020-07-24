import csv
import json

def date_cruncher(dirty_date):
    """
    This helper function takes in a raw date string and returns a clean date string in "mm-dd-yyyy" format
    Parameter:
        dirty_date (str): uncleaned date string in "Month Day, Year" format
    Returns:
        cleaned date (str) in "mm-dd-yyyy" format
    Example:
        >>> date_cruncher("September 8, 2018")
        "09-08-2018"
    """
    date_dict = {"jan":"01", "feb":"02", "mar":"03", "apr":"04", "may":"05", "jun":"06", "jul":"07", "aug":"08", "sep":"09", \
                 "oct":"10", "nov":"11", "dec":"12"}
    month, day, year = dirty_date.replace(",", "").split()
    month = date_dict[month[:3].lower()]
    day = f"0{day}" if len(day) < 2 else day
    return f"{month}-{day}-{year}"

def read_and_clean_csv(csv_name):
    """
    Only need show_id, type, title, director, cast, country, date_added,
    release_year, listed_in, and description.

    No rating or duration.
    """
    with open(f'{csv_name}.txt', encoding = 'utf8') as fin:
        reader = csv.reader(fin)
        header = next(reader)
        keys = {key: i for key, i in zip(header, range(len(header)))}
        readerList = [line for line in reader]
        for show in readerList:
            show[keys['show_id']] = int(show[keys['show_id']])
            show[keys['type']] = str(show[keys['type']])
            show[keys['title']] = str(show[keys['title']])
            if str(show[keys['director']]) == '':
                show[keys['director']] = None
            else:
                show[keys['director']] = str(show[keys['director']])
            if str(show[keys['cast']]) == '':
                show[keys['cast']] = None
            else:
                show[keys['cast']] = str(show[keys['cast']])
            if str(show[keys['country']]) == '':
                show[keys['country']] = 'Unknown'
            else:
                show[keys['country']] = str(show[keys['country']])
            if str(show[keys['date_added']]) == '':
                show[keys['date_added']] = None
            else:
                show[keys['date_added']] = date_cruncher(show[keys['date_added']])
            show[keys['release_year']] = int(show[keys['release_year']])
            show[keys['listed_in']] = str(show[keys['listed_in']])
            show[keys['description']] = str(show[keys['description']])
            show.remove(show[keys['duration']])
            show.remove(show[keys['rating']])
    return readerList

def read_and_clean_json(json_name):
    jsondict = json.load(open(f'{json_name}.json', encoding = 'utf8'))
    returnlist = []
    for show_id in jsondict:
        showlist = [int(show_id)]
        show = jsondict[show_id]
        showlist.append(str(show['type']))
        showlist.append(str(show['title']))
        if str(show['director']) == '':
            showlist.append(None)
        else:
            showlist.append(str(show['director']))
        if str(show['cast']) == '':
            showlist.append(None)
        else:
            showlist.append(str(show['cast']))
        if str(show['country']) == '':
            showlist.append('Unknown')
        else:
            showlist.append(str(show['country']))
        if str(show['date_added']) == '':
            showlist.append(None)
        else:
            showlist.append(date_cruncher(show['date_added']))
        showlist.append(int(show['release_year']))
        showlist.append(str(show['listed_in']))
        showlist.append(str(show['description']))
        returnlist.append(showlist)
    return returnlist

def country_appearances(cleaned_list):
    country_dict = {}
    for show in cleaned_list:
        countries = show[5].split(', ')
        for country in countries:
            if country in country_dict.keys():
                country_dict[country] = country_dict[country] + 1
            else:
                country_dict[country] = 1
    return country_dict

def description_appearances(letter, cleaned_list):
    returnlist = []
    for show in cleaned_list:
        description = (show[2], show[9].lower().count(letter.lower()))
        returnlist.append(description)
    returnlist.sort(key = lambda s: (s[1], s[0]), reverse = True)
    return returnlist[:50]

def cast_appearances(actor, cleaned_list):
    returnlist = []
    for show in cleaned_list:
        if show[4] is not None and actor.lower() in show[4].lower():
            returnlist.append((show[3], show[1], show[2]))
    return sorted(returnlist, key = lambda s: s[2], reverse = True)

def added_date(cleaned_list, beginning_year, ending_year, month):
    months = {'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12}
    month_num = months[month.lower()]
    returnlist = []
    for show in cleaned_list:
        if show[6] is not None and int(show[6].split('-')[2]) >= int(beginning_year) and int(show[6].split('-')[2]) <= int(ending_year) and int(show[6].split('-')[0]) == month_num:
            returnlist.append((show[6], show[0], show[2]))
    return sorted(returnlist, key = lambda s: (int(s[0].split('-')[2]), int(s[0].split('-')[1]), int(s[0].split('-')[0]), s[2]))

def bee_script(file_name, output_file):
    returnlist = []
    with open(f"{file_name}.txt", "r") as fin:
        reader = csv.reader(fin, delimiter = "\n")

        with open(f"{output_file}.csv", "w", newline = "") as fout:
            writer = csv.writer(fout)

            linenum = 1
            for line in reader:
                contains_bee = 'YES' if 'bee' in line[0].lower() else 'NO'
                returnlist.append({'line': linenum, 'num_words': len(line[0].split()), 'contains_bee': contains_bee, 'script_line': line[0]})
                writer.writerow([linenum, len(line[0].split()), contains_bee, line[0]])
                linenum += 1
    return returnlist

def write_to_json(file_name, cleaned_list):
    cleaned_list.sort(key = lambda s: s[7], reverse = True)
    returndict = {}
    show_dict_list = []
    for show in cleaned_list:
        if show[6] is not None:
            num_countries = 0 if show[5] is 'Unknown' else len(show[5].split(', '))
            show_dict = {'date_added': show[6], 'title': show[2], 'show_id': show[0], 'director': show[3], 'num_countries': num_countries}
            if str(show[7]) not in returndict.keys():
                returndict[str(show[7])] = [show_dict]
            else:
                returndict[str(show[7])].append(show_dict)

    for showlist in returndict.values():
        showlist.sort(key = lambda s: s['show_id'])

    json.dump(returndict, open(f"{file_name}.json", "w"))
    return returndict
