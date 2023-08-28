from urlextract import  URLExtract
extract=URLExtract()
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import  emoji
import collections
def fetch_stats(selected_user,df):
    if selected_user!='overall':
        df = df[df['user'] == selected_user]
    #fetch number of messages
    num_messages = df.shape[0]
    # no of words
    # count words
    words = []
    for msg in df['message']:
        words.extend(msg.split())
    # fetch number of media messages
    num_media_msg = df[df['message'] == "<Media omitted>"].shape[0]

    #fetch number of shared links
    links=[]
    for msg in df['message']:
        links.extend(extract.find_urls(msg))
    return num_messages, len(words), num_media_msg,len(links)

def most_active(df):
    x = df['user'].value_counts().head()
    # find percentage each user seng how much msgs
    df= round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
    columns={'index': 'name', 'user': 'percentage'})
    return x,df

def create_wordcloud(selected_user,df):
    f = open('stop_words.txt', 'r')
    stop_words = f.read()
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    # remove group-notification ,media omited and stop words
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']

    # to check stop_words
    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" ")) #create world count on df column
    return df_wc

def most_common_words(selected_user,df):
    f=open('stop_words.txt','r')
    stop_words=f.read()
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    #remove group-notification ,media omited and stop words
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>']
    words = []
    for msg in temp['message']:
        for word in msg.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df=pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

# emoji
def emoji_helper(selected_user,df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    get_emojis_1str = lambda word_list: collections.Counter(
        [match["emoji"] for word in word_list for match in emoji.emoji_list(word)])

    emojis_count = get_emojis_1str(df['message'])
    emoji_df = pd.DataFrame(list(emojis_count.items()), columns=["Emoji", "Count"])
    emoji_df = emoji_df.sort_values(by="Count", ascending=False)
    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    daily_counts = df['only_date'].value_counts().sort_index().reset_index()
    daily_counts.columns = ['date', 'count']

    return daily_counts

def week_activity_map(selected_user,df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    activity_counts = df['day_name'].value_counts().reset_index()
    activity_counts.columns = ['day', 'count']

    return activity_counts

def month_activity_map(selected_user,df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    month_counts = df['month'].value_counts().reset_index()
    month_counts.columns = ['month', 'count']
    return month_counts

def activity_heatmap(selected_user,df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]
    user_heatmap=df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap


