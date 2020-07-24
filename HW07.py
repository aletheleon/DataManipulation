import numpy as np
import pandas as pd
from pprint import pprint

def numpy_data_loader(file_name):
    return_data = np.loadtxt(file_name, unpack=True, delimiter=",", encoding="utf8", skiprows=1, dtype= str)
    return (return_data[0].astype("int"),
        return_data[1],
        return_data[2].astype("int"),
        return_data[3].astype("int"),
        return_data[4],
        return_data[5],
        return_data[6].astype("int"),
        return_data[7],
        return_data[8].astype("int"),
        return_data[9].astype("int"),
        return_data[10].astype("int"),
        return_data[11].astype("int"),
        return_data[12].astype("int"),
        return_data[13].astype("int"),
        return_data[14].astype("float"),)

# pprint(numpy_data_loader("steam.csv"))
# print(type(numpy_data_loader("steam.csv")))
# appid, name, release_year, english, developer, platforms, required_age, genres, achievements, postive_ratings, negative_ratings, average_playtime, owners_lb, owners_ub, price = numpy_data_loader("steam.csv")
#pprint(appid)

def age_checker(name, required_age, age):
    return name[required_age <= age]

def eligible_purchases(name, price, conversion, budget):
    return name[budget >= conversion * price]

def probability_of_purchasing(name, positive_ratings, negative_ratings, average_playtime):
    game_probability = np.full(name.shape, 0.5, dtype=float)
    game_rating = positive_ratings / (positive_ratings + negative_ratings)
    game_probability = np.where(game_rating >= 0.9, game_probability + 0.3,
                                np.where(game_rating >= 0.8, game_probability + 0.2, game_probability - 0.25))
    game_probability = np.where(average_playtime >= 100, game_probability + 0.2,
                                np.where(average_playtime >= 95, game_probability + 0.1, game_probability - 0.25))
    return name[game_probability >= 0.75]

def pandas_data_loader(file_name):
    return pd.read_csv(file_name, delimiter=",", index_col=0)

def add_free(df):
    df['free'] = np.where(df['price'] == 0, True, False)
    df['english'] = np.where(df['english'] == 0, False, True)
    return df

def add_positive_percent(df):
    df['positive_percent'] = round(df['positive_ratings'] * 1.0 / (df['positive_ratings'] + df['negative_ratings']) * 100, 2)
    return df

def add_sales_revenue(df):
    df['sales_revenue'] = round((df['owners_ub'] + df['owners_lb'])/2 * df['price'], 2)
    return df

def sales_revenue_for_genre(df, genre):
    genre_games = df[df['genres'].str.contains(genre.lower(), case=False)]
    return round(genre_games['sales_revenue'].sum(), 2)

def operating_systems(df):
    windows = [1 if 'windows' in game else 0 for game in df['platforms']]
    mac = [1 if 'mac' in game else 0 for game in df['platforms']]
    linux = [1 if 'linux' in game else 0 for game in df['platforms']]
    return pd.DataFrame(zip(windows,mac,linux), index=df.index, columns=['windows','mac','linux'])

def add_num_operating_systems(df):
    df['num_operating_systems'] = df['windows'] + df['mac'] + df['linux']
    df.loc["total_games"] = df.sum()
    return df

def unique_developers(df):
    developers = set()
    for game in df['developer']:
        for developer in game.split(';'):
            developers.add(developer)
    return pd.Series([dev_id for dev_id in range(1, len(developers) + 1)], index=sorted(developers))

def aggregated_max_price(df, group):
    english_df = df[df['english'].to_numpy().astype(bool)]
    return english_df.groupby(group)['price'].max().sort_values(ascending=False)

def release_year_stats(df, is_free):
    df_filtered = df[df['price'] == 0] if is_free else df[df['price'] > 0]
    df_mean = round(df_filtered.groupby('release_year')[['achievements','positive_percent']].mean(), 2).rename(columns={'achievements':'avg_achievements','positive_percent':'avg_positive_percent'})
    df_count = df_filtered.groupby('release_year')['release_year'].count()
    return df_mean.join(df_count).rename(columns={'release_year':'num_games'})

def write_to_excel(file_name, dfs, sheet_names):
    writer = pd.ExcelWriter(file_name)
    for df, sheet in zip(dfs, sheet_names):
        df.to_excel(writer, sheet_name=sheet)
    writer.save()

''' Bonus Functions '''
"""
Write a function that returns the years that had the most game releases. To
solve this, make sure to compute the frequency. Show only the top years as given
by parameter years and make sure the years are sorted in order of frequency.
This function has a one-line maximum.

This function is a good application of histogramming and would be practical for
deciding which years were the best for computer gaming.

Test:
bonus_function_1(pandas_data_loader('steam.csv'), 3)

Answer:
2016    33
2017    31
2015    25
Name: release_year, dtype: int64
"""
def bonus_function_1(df, years):
    return df['release_year'].value_counts().head(years)


"""
Write a function that returns only the games that work on your gaming platform.
The gaming platform is passed in as a string. You can assume it will be a valid
platform. This function has a one-line maximum.

This function would be practical for a gamer looking to filter games by the ones
applicable to him.

Test:
bonus_function_2(pandas_data_loader('steam.csv'), 'linux')

Answer:
                                                    name  release_year  english  ... owners_lb owners_ub  price
appid                                                                            ...
2                             Awesomenauts - the 2D moba          2012        1  ...   2000000   5000000   0.00
11     STAR WARS™ Knights of the Old Republic™ II - T...          2012        1  ...   2000000   5000000   7.19
14                      Beatbuddy: Tale of the Guardians          2013        1  ...    200000    500000   6.99
16                        World of Guns: Gun Disassembly          2014        1  ...   2000000   5000000   0.00
17                 Grim Legends 2: Song of the Dark Swan          2015        1  ...    100000    200000   6.99
21                           Micro Machines World Series          2017        1  ...     20000     50000  24.99
26                                    Age of Wonders III          2014        1  ...    500000   1000000  22.99
32                              Sir You Are Being Hunted          2014        1  ...    500000   1000000  14.99
33                            The Pirate: Caribbean Hunt          2016        1  ...    500000   1000000   0.00
38                                   X3: Terran Conflict          2008        1  ...    500000   1000000  15.99
39                                          Nuclear Dawn          2011        1  ...    200000    500000   6.99
42                                            Gemini Rue          2011        1  ...    200000    500000   6.99
45                                   RUNNING WITH RIFLES          2015        1  ...    200000    500000  10.99
46                                               Silence          2016        1  ...    100000    200000  16.99
47                                           Sepia Tears          2016        1  ...    100000    200000   0.00
59                                         Space Farmers          2014        1  ...    200000    500000   7.19
61                                            Spellsworn          2018        1  ...    100000    200000   0.00
65               Princess Remedy 2: In A Heap of Trouble          2016        1  ...         0     20000   3.99
67              Spinnortality | cyberpunk management sim          2019        1  ...         0     20000   9.99
72                  The Secret of Tremendous Corporation          2015        1  ...    100000    200000   0.00
78                           RIVE: Wreck Hack Die Retry!          2016        1  ...    200000    500000  10.99
83                                 Cheaters Blackjack 21          2016        1  ...         0     20000   2.79
89                                  Zombie Panic! Source          2008        1  ...    500000   1000000   0.00
91                                       Planet Centauri          2016        1  ...     50000    100000  11.99
92                                          Risk of Rain          2013        1  ...   1000000   2000000   6.99
95                                     Hearts of Iron IV          2016        1  ...   1000000   2000000  34.99
98                                      Empire TV Tycoon          2015        1  ...     50000    100000   6.99
100                                            Angeldust          2016        1  ...    200000    500000   0.00
102                                           Tannenberg          2017        1  ...    100000    200000  15.49
109             Sid Meier's Civilization®: Beyond Earth™          2014        1  ...   1000000   2000000  29.99
113                                   Age of Conquest IV          2016        1  ...    200000    500000   0.00
116              The Infectious Madness of Doctor Dekker          2017        1  ...     20000     50000   6.99
117                     Interplanetary: Enhanced Edition          2017        1  ...     50000    100000  10.99
121                                       The Masterplan          2015        1  ...     50000    100000  14.99
122                                 Kerbal Space Program          2015        1  ...   2000000   5000000  29.99
124                                    A Virus Named TOM          2012        1  ...    200000    500000   6.99
125                      Rocketbirds: Hardboiled Chicken          2012        1  ...    200000    500000   3.99
138                                  Oh...Sir! Prototype          2015        1  ...    100000    200000   0.00
140                                           >observer_          2017        1  ...    200000    500000  22.99
142                                     Your Friend Hana          2017        1  ...     50000    100000   0.79
145                                        NEO Scavenger          2014        1  ...    100000    200000  11.39
151                                            Gone Home          2013        1  ...    500000   1000000  10.99
152                                           Imagine Me          2014        1  ...     50000    100000   1.99
156                              Shootout on Cash Island          2018        1  ...         0     20000   2.09
158                                       Bloody Glimpse          2017        1  ...         0     20000   3.99
163                                     Blueberry Garden          2009        1  ...     20000     50000   3.99
166                                             Oil Rush          2012        1  ...    200000    500000   5.59
167                                        Dynamite Jack          2012        1  ...    100000    200000   7.19
168                                             Gateways          2012        1  ...     50000    100000   3.99
174                                         Pixel Hunter          2014        1  ...     20000     50000   1.99
176                                              Quintet          2015        1  ...    100000    200000   0.00
177    Challenge of the Five Realms: Spellbound in th...          2015        1  ...         0     20000   4.99
181                                      Unearned Bounty          2018        1  ...    100000    200000   0.00
184    Battle for Blood - Epic battles within 30 seco...          2015        1  ...    100000    200000   0.00
187                                             Tiltagon          2016        1  ...     20000     50000   1.99
197                                                 Naev          2017        1  ...     50000    100000   0.00

[56 rows x 14 columns]
"""
def bonus_function_2(df, platform):
    return df[[True if platform in game else False for game in df['platforms']]]


"""
Write a function that returns the average playtime for each year. This needs to
be calculated by using a groupby function. This function has a one-line maximum.

This function would be practical for formulating considerations for the most
popular years for gaming.

Test:
bonus_function_3(pandas_data_loader('steam.csv'))

Answer:
release_year
2006                474.000000
2007                 90.000000
2008                458.333333
2009                288.375000
2010                 67.666667
2011                615.600000
2012                342.562500
2013               7671.230769
2014                463.200000
2015               5113.040000
2016                565.696970
2017                264.354839
2018                778.681818
2019               2003.166667
"""
def bonus_function_3(df):
    return df.groupby('release_year').aggregate({'average_playtime':'mean'})

def test_cases():

    data = numpy_data_loader('steam.csv')
    ''' you can test print each array if you wish '''
    appid, name, release_year, english, developer, platforms, required_age, genres, achievements, positive_ratings, negative_ratings, average_playtime, owners_lb, owners_ub, price = \
    data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[12], data[13], data[14]

    name1 = np.array(['Wolfenstein II: The New Colossus', 'Devil May Cry 5', '>observer_', 'Ultimate Fishing Simulator'])
    required_age1 = np.array([18, 18, 16, 0])
    age_checker(name1, required_age1, 17)

    name2 = np.array(['Microsoft Flight Simulator X: Steam Edition', 'Ultimate Fishing Simulator', 'Far Cry - Primal'])
    price2 = np.array([19.99, 14.99, 41.99])
    purchases = eligible_purchases(name2, price2, 1.23, 50)

    name3 = np.array(['Manhunt', 'Crystalline', 'Pro Cycling Manager 2017'])
    positive_ratings3 = np.array([816, 771, 194])
    negative_ratings3 = np.array([433, 23, 106])
    average_playtime3 = np.array([99, 982, 999])
    prob = probability_of_purchasing(name3, positive_ratings3, negative_ratings3, average_playtime3)

    df = pandas_data_loader('steam.csv')
    df = add_free(df)
    df = add_positive_percent(df)
    df = add_sales_revenue(df)
    genre_sales = sales_revenue_for_genre(df, 'aCtIoN')
    os_df = operating_systems(df)
    os_df = add_num_operating_systems(os_df)
    ud_df = unique_developers(df)
    mp_df = aggregated_max_price(df, 'release_year')
    years_df = release_year_stats(df, True)
    write_to_excel('steam_data.xlsx', [df, os_df, ud_df, years_df], ['steam', 'operating_systems', 'unique_developers', 'release_year_stats'])

if __name__ == '__main__':
    test_cases()
