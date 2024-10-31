from urlextract import URLExtract
import pandas as pd
from collections import Counter
from wordcloud import WordCloud
import emoji

extract = URLExtract()

def fetchstats(selected_user, df):

    # if the selected user is a specific user, then make changes in dataframe else do not change
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    num_messages = df.shape[0]
    words = []

    for message in df['Message']:
        words.extend(message.split())

    # Counting the number of media files shared
    mediaommitted = df[df['Message'] == '<Media omitted>']

    # Number of links shared

    links = []
    for message in df['Message']:
        links.extend(extract.find_urls(message))
    
    return num_messages, len(words), mediaommitted.shape[0], len(links)


# Most busy users (group level)

def fetchbusyuser(df):
    df = df[df['user'] != 'Group Notification']
    count = df['user'].value_counts().head()

    newdf = pd.DataFrame((df['user'].value_counts()/df.shape[0])*100)
    return count, newdf

def createwordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')

    # Use .str.cat to concatenate all messages into a single string
    df_wc = wc.generate(df['Message'].str.cat(sep=" "))

    return df_wc

# Most common words

def getcommonwords(selected_user, df):
    # getting stop words
    with open('stop_words_english.txt', 'r', encoding='utf-8') as file:
        stopwords = file.read().split('\n')

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    temp = df[(df['user'] != 'Group Notification') & (df['user'] != '<Media omitted>')]

    words = []

    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stopwords:
                words.append(word)
    
    mostcommon = pd.DataFrame(Counter(words).most_common(20))
    return mostcommon


def getemojistats(selected_user, df):
    if selected_user != "Overall":
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    
    emojidf = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emojidf


def monthtimeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    temp = df.groupby(['Month', 'Day', 'Day_Name']).count()['Message'].reset_index()

    time = []
    for i in range(temp.shape[0]):
        time.append(str(temp['Day'][i]) + "-" + str(temp['Month'][i]))

    temp['Time'] = time
    return temp


def monthactivitymap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['Month'].value_counts()

def weekactivitymap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['Day_Name'].value_counts()