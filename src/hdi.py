import numpy as np
import pandas as pd
import seaborn as sns; sns.set()
import matplotlib.pyplot as plt
from pandas.plotting import autocorrelation_plot
from matplotlib import pyplot


def clean(df):
    numeric = ['1990', '1991', '1992', '1993', '1994', '1995', '1996', '1997', '1998', '1999', '2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008',
    '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    # turn string numbers into numeric values
    for i in numeric:
        df[i] = pd.to_numeric(data[i])
    # strip superfluous spaces from names under "Country" column
    for i in data['Country']:
        df['Country'].replace(i, i.strip(), inplace=True)
    df.sort_values(by=['HDI Rank (2015)'], inplace=True)
    return df

def heat_plot(df):
    pyplot.matshow(data.loc[:, '1990':'2015'], interpolation=None, aspect='auto')
    pyplot.show()

def make_dataframes(df):
    # Define regions
    north_america = ['Canada', 'United States']
    latin_america_caribbean = ['Antigua and Barbuda', 'Argentina', 'Bahamas', 'Barbados', 'Belize', 'Bolivia (Plurinational State of)','Brazil','Chile','Colombia','Costa Rica', 'Cuba', 'Dominica', 'Dominican Republic', 'Ecuador', 'El Salvador', 'Grenada', 'Guatemala', 'Guyana', 'Haiti', 'Honduras',
    'Jamaica', 'Mexico', 'Nicaragua', 'Panama', 'Paraguay', 'Peru', 'Saint Kitts and Nevis', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Suriname', 'Trinidad and Tobago', 'Uruguay','Venezuela (Bolivarian Republic of)']
    africa = ['Angola','Benin','Botswana','Burkina Faso','Burundi','Cabo Verde','Cameroon','Central African Republic','Chad','Comoros','Congo','Congo (Democratic Republic of the)',"CÙte d'Ivoire",'Djibouti','Equatorial Guinea','Eritrea','Ethiopia','Gabon','Gambia','Ghana','Guinea','Guinea-Bissau','Kenya','Lesotho',
    'Liberia','Madagascar','Malawi','Mali','Mauritania','Mozambique','Namibia','Niger','Nigeria','Rwanda','Sao Tome and Principe','Senegal','Sierra Leone','South Africa', 'South Sudan','Sudan','Swaziland','Tanzania (United Republic of)','Togo','Uganda','Zambia','Zimbabwe']
    mena = ['Algeria','Bahrain','Egypt','Iran (Islamic Republic of)','Iraq','Israel','Jordan','Kuwait','Lebanon','Libya','Morocco','Oman','Palestine, State of','Qatar','Saudi Arabia','Syrian Arab Republic','Tunisia','Turkey','United Arab Emirates','Yemen']
    apac = ['Australia','Azerbaijan','Bangladesh','Bhutan','Brunei Darussalam','Cambodia','China','Fiji','Hong Kong, China (SAR)','India','Indonesia','Japan','Kiribati','Korea (Republic of)',"Lao People's Democratic Republic",'Malaysia','Maldives','Mauritius','Micronesia (Federated States of)','Mongolia','Myanmar','Nepal','New Zealand','Pakistan',
    'Palau','Papua New Guinea','Philippines','Samoa','Seychelles','Singapore','Solomon Islands','Sri Lanka','Thailand', 'Timor-Leste','Tonga','Vanuatu','Viet Nam']
    ee_ca = ['Afghanistan','Albania','Armenia','Austria','Belarus','Bosnia and Herzegovina','Bulgaria','Croatia','Czech Republic','Estonia','Georgia','Hungary','Kazakhstan','Kyrgyzstan','Latvia','Lithuania','Moldova (Republic of)','Poland','Romania','Russian Federation','Serbia','Slovakia','Slovenia','Tajikistan',
    'The former Yugoslav Republic of Macedonia','Ukraine','Uzbekistan']
    w_europe = ['Belgium','Andorra','Cyprus','Denmark','Finland','France','Germany','Greece','Iceland','Ireland','Italy','Liechtenstein','Luxembourg','Malta','Montenegro','Netherlands','Norway','Portugal','Spain','Sweden','Switzerland','United Kingdom']

    # Create region disaggregated dataframes
    df_north_america = data.loc[data['Country'].isin(north_america)]
    df_latin_america = data.loc[data['Country'].isin(latin_america_caribbean)]
    df_africa = data.loc[data['Country'].isin(africa)]
    df_mena = data.loc[data['Country'].isin(mena)]
    df_asia_pac = data.loc[data['Country'].isin(apac)]
    df_e_europe_c_asia = data.loc[data['Country'].isin(ee_ca)]
    df_europe = data.loc[data['Country'].isin(w_europe)]
    return df_north_america, df_latin_america, df_africa, df_mena, df_asia_pac, df_e_europe_c_asia, df_europe


def make_csv(df_list):
    # export csv files for the cleaned full and region disaggregated datasets
    for i in df_list:
        i.to_csv('hdi_repo/src/{}.csv'.format(i), index=False)


def plot_trends(df_list):
    fig, ax = plt.subplots(figsize=(15, 10))
    color_lst = ["black","darkgrey","steelblue","slategrey","skyblue","seagreen","darkseagreen","darkolivegreen"]
    plt.xticks(rotation=30)
    yticks = np.linspace(0, 1, 11)
    ax.set_yticks(yticks)
    ax.set_xlabel('Year',fontsize=15);
    ax.set_ylabel('Average HDI score',fontsize=15)
    ax.set_title("Global HDI Trend: 1990-2015", fontsize=20)
    ax.legend(handles=ax.lines, labels=["World","North America","Western Europe","Eastern Europe and Central Asia","Latin America and Caribbean","Asia Pacific","Africa"])
    for idx, i in enumerate(df_list):
        df_trend = i.loc[:, '1990':'2015']
        X_trend = df_trend.columns
        y_trend_lst = []
        for x in X_trend:
            year_mean = np.mean(df_trend[x])
            y_trend_lst.append(round(year_mean, 3))
        y_trend = np.array(y_trend_lst)
        color = color_lst[idx]
        if idx == 0:
            sns.lineplot(x = X_trend, y = y_trend, linewidth=15, color="black")
        else:
            sns.pointplot(x = X_trend, y = y_trend, linewidth=3, color=color)
    plt.show()


describe_data(df):
    df_describe = df.loc[:, '1990':'2015']
    cols = df_describe.columns()
    for i in cols:
        df[i].describe()

explore_variance(df):
    df_variance = data.loc[:, 'Country':]
    df_variance['variance'] = round(df_variance.var(axis=1), 4)
    df_var = df_variance.sort_values(by='variance', axis=0, ascending=True)
    df_var.reset_index(inplace=False, drop=True)
    for idx, i in enumerate(df_var['Country']):
        print(i, "variance: ", df_var['variance'][idx])


if __name__ == "__main__":

    data = pd.read_csv('hdi_repo/src/human_development_index_HDI.csv', encoding='ISO-8859-1')
    df = clean(data)
    df_north_america, df_latin_america, df_africa, df_mena, df_asia_pac, df_e_europe_c_asia, df_europe = make_dataframes(df)
    df_list = [df, df_north_america, df_latin_america, df_africa, df_mena, df_asia_pac, df_e_europe_c_asia, df_europe]
    trends = plot_trends(df_list)
    # make_csv(df_list)
    # heat_map(df)
    # plot_trends(df_list)
    # describe_data(df)
    # explore_variance(df)
