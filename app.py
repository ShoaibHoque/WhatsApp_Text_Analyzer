import streamlit as st
import preprocess
import re
import stats
import matplotlib.pyplot as plt
import numpy as np

try:
    st.sidebar.title('WhatsApp Chat Analyzer by Shoaib Hoque')

    # upload file
    uploaded_file = st.sidebar.file_uploader("Choose a file")

    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        data = bytes_data.decode("utf-8")

        # sending file to preprocess
        df = preprocess.preprocess(data)

        # unique user
        user_list = df['user'].unique().tolist()

        # remove group notification
        #user_list.remove('Group Notification')

        user_list.sort()

        user_list.insert(0, 'Overall')

        selected_user = st.sidebar.selectbox(
            "Show analysis with respect to", user_list
        )

        st.title("Shoaib's WhatsApp chat analysis for "+ selected_user)

        if st.sidebar.button("Show Analysis"):
            num_messages, num_words, media_omitted, links = stats.fetchstats(selected_user, df)

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.header("Total Messages")
                st.title(num_messages)
            
            with col2:
                st.header("Total No. of Words")
                st.title(num_words)
            
            with col3:
                st.header("Media Shared")
                st.title(links)

            with col4:
                st.header("Total Links Shared")
                st.title(links)
            
            # find the busiest user in the group
            if selected_user == "Overall":

                st.title("Most Busy Users")
                busycount, newdf = stats.fetchbusyuser(df)
                fig, ax = plt.subplots()
                col1, col2 = st.columns(2)

                with col1:
                    ax.bar(busycount.index, busycount.values, color = 'pink')
                    plt.xticks(rotation = 'vertical')
                    st.pyplot(fig)

                with col2:
                    st.dataframe(newdf)
            
            # Word Cloud
            st.title("Word Cloud")
            df_img = stats.createwordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_img)
            st.pyplot(fig)

            # most common word in chat

            most_common_df = stats.getcommonwords(selected_user, df)
            fig, ax = plt.subplots()
            ax.barh(most_common_df[0], most_common_df[1])
            plt.xticks(rotation = 'vertical')
            st.title("Most Common Words")
            st.pyplot(fig)

            # timeline
            st.title("Timeline")
            time = stats.monthtimeline(selected_user, df)
            fig, ax = plt.subplots()
            ax.plot(time['Time'], time['Message'], color = 'green')
            plt.xticks(rotation = 'vertical')
            plt.tight_layout()
            st.pyplot(fig)

            # Activity Maps
            st.title("Activity Maps")
            col1, col2 = st.columns(2)

            with col1:
                st.header("Most Busy Day")

                busy_day = stats.weekactivitymap(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_day.index, busy_day.values, color = 'purple')
                plt.xticks(rotation = 'vertical')
                plt.tight_layout()
                st.pyplot(fig)
                
            with col2:

                st.header('Most Busy Month')
                busy_month = stats.monthactivitymap(selected_user, df)

                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values, color = 'red')
                plt.xticks(rotation = 'vertical')
                plt.tight_layout()
                st.pyplot(fig)

            emoji_df = stats.getemojistats(selected_user, df)
            emoji_df.columns = ['Emoji', 'Count']

            st.title("Emoji Analysis")

            col1, col2 = st.columns(2)

            with col1:
                st.dataframe(emoji_df)
            with col2:
                emojicount = list(emoji_df['Count'])
                perlist = list(emoji_df['Count'])
                perlist = [(i/sum(emojicount))*100 for i in emojicount]
                emoji_df['Percentage use'] = np.array(perlist)
                st.dataframe(emoji_df)

except:
    pass 