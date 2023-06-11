from generator_csv import *
import streamlit as st

if __name__ == "__main__":
    start_city = st.text_input('Откуда', 'Москва')
    end_city = st.text_input('Куда', 'Санкт-Петербург')
    with st.spinner('Идет парсинг, подождите...'):
        generate_csv(False, start_city, end_city)
    st.success('Done!')
    
    st.subheader('Посмотрим, что получилось')

    df_to_show = pd.read_csv(start_city + '_' + end_city +'.csv')

    fig = plot_graph(start_city + '_' + end_city +'.csv')

    st.dataframe(df_to_show)

    st.pyplot(fig, use_container_width = False)
