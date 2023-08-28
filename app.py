import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns
st.sidebar.title("whatsapp chat Analyzer")
# to upload web chat file
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    # file is stream of byte data need to convert into string
    data = bytes_data.decode("utf-8")

    df = preprocessor.preprocess(data)  # provide data to preprocessor function


    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"overall")
    selected_user=st.sidebar.selectbox("Show Analysiswrt",user_list)
    if st.sidebar.button("Show analysis"):

        # Stats Area
        st.title("Top Statistics")
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        # monthly timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        fig.set_size_inches(10, 6)
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)

        fig, ax = plt.subplots()
        fig.set_size_inches(10, 6)
        ax.plot(daily_timeline['date'], daily_timeline['count'], color='blue')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title('Activity Map')
        col1, col2 = st.columns(2)

        with col1:
            st.title("Most Busy Day")
            activity_map = helper.week_activity_map(selected_user, df)

            fig, ax = plt.subplots()
            fig.set_size_inches(10, 6)
            ax.bar(activity_map['day'], activity_map['count'], color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.title("Most busy Month")
            month_activity_map = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            fig.set_size_inches(10, 6)
            ax.bar(month_activity_map['month'], month_activity_map['count'], color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        st.title("Weekly Activity Map")
        user_heatmap=helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots()
        ax=sns.heatmap(user_heatmap)
        st.pyplot(fig)






        # finding most active user in group
        if selected_user=='overall':
            st.title("Most Active users")
            x,new_df = helper.most_active(df)
            fig, ax=plt.subplots()
            col1, col2=st.columns(2)
            with col1:
                ax.bar(x.index, x.values,color='red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)


            # wordcloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax=plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)


        # most common words'
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1]) #barh horizontal bar chart
        st.title('Most Common Words')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #emoji analysis
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title( " emoji analysis ")
        col1,col2 = st.columns(2)
        with col1:
           st.dataframe(emoji_df)
        with col2:
            fig,ax=plt.subplots()
            ax.pie(emoji_df["Count"].head(), labels=emoji_df["Emoji"].head(),autopct="%0.2f")
            st.pyplot(fig)












