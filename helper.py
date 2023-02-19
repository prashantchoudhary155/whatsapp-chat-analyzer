import urlextract
extract= urlextract.URLExtract()
import pandas as pd
from collections import Counter
import emoji

def fetch_stats(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['users']==selected_user]
    num_messages=df.shape[0]
    words=[]
    links=[]
    for message in df['messages']:
        words.extend(message.split())
        links.extend(extract.find_urls(message))
    num_media_messages=df[df['messages'] == '<Media omitted>\n'].shape[0]

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x=df['users'].value_counts().head()
    df= round((df['users'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','users':'percent'})
    return x,df

def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df=df[df['users']==selected_user]

    f = open('hinglish.txt')
    stop_words = f.read()

    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>\n']
    words=[]
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return pd.DataFrame(Counter(words).most_common(20))

def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def week_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

def activity_heatmap(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='messages', aggfunc='count').fillna(0)

    return user_heatmap