import streamlit as st
import pandas as pd
import plotly.express as px

#налаштування сторінки
st.set_page_config(layout="wide", page_title="Аналіз VHI Даних")

#завантаження данних
@st.cache_data
def load_data():
    #завантажуємо файл данних
    df = pd.read_csv('final_vhi_data.csv')
    
    #видаляємо зайві пробіли в назвах колонок якщо вони є
    df.columns = df.columns.str.strip()
    return df

try:
    df_raw = load_data()
except FileNotFoundError:
    st.error("файл 'final_vhi_data.csv' не знайдено")
    st.stop()

#логіка скидання фільтрів
def reset_filters():
    st.session_state.year_range = (int(df_raw['Year'].min()), int(df_raw['Year'].max()))
    st.session_state.week_range = (1, 52)
    st.session_state.region = df_raw['Province_Name'].unique()[0]
    st.session_state.index_type = 'VHI'
    st.session_state.sort_asc = False
    st.session_state.sort_desc = False

#ініціалізація стану
if 'year_range' not in st.session_state:
    reset_filters()

#інтерфейс
col1, col2 = st.columns([1, 3])

with col1:
    st.header("Налаштування")
    
    #dropdown для вибору індексу
    index_choice = st.selectbox("Оберіть показник", ['VCI', 'TCI', 'VHI'], key='index_type')
    
    #dropdown для вибору області
    region_choice = st.selectbox("Оберіть область", df_raw['Province_Name'].unique(), key='region')
    
    #slider для років
    min_year = int(df_raw['Year'].min())
    max_year = int(df_raw['Year'].max())
    year_range = st.slider("Інтервал років", min_year, max_year, key='year_range')
    
    #slider для тижнів
    week_range = st.slider("Інтервал тижнів", 1, 52, key='week_range')
    
    #checkboxes для сортування
    st.subheader("Сортування")
    c1, c2 = st.columns(2)
    with c1:
        sort_asc = st.checkbox("Зростання", key='sort_asc')
    with c2:
        sort_desc = st.checkbox("Спадання", key='sort_desc')
    
    if sort_asc and sort_desc:
        st.warning("Оберіть щось одне")

    #иutton для скидання
    st.button("Скинути фільтри", on_click=reset_filters)

#фільтрація
df_filtered = df_raw[
    (df_raw['Province_Name'] == region_choice) &
    (df_raw['Year'] >= year_range[0]) & (df_raw['Year'] <= year_range[1]) &
    (df_raw['Week'] >= week_range[0]) & (df_raw['Week'] <= week_range[1])
]

#обробка сортування
if sort_asc and not sort_desc:
    df_filtered = df_filtered.sort_values(by=index_choice, ascending=True)
elif sort_desc and not sort_asc:
    df_filtered = df_filtered.sort_values(by=index_choice, ascending=False)

#відображення
with col2:
    tab1, tab2, tab3 = st.tabs(["Таблиця", "Часовий ряд", "Порівняння областей"])
    
    with tab1:
        st.dataframe(df_filtered, use_container_width=True)
    
    with tab2:
        st.subheader(f"Графік {index_choice} для області {region_choice}")
        # Створюємо графік 
        fig1 = px.line(df_filtered, x='Year', y=index_choice, color='Week',
                        markers=True, title=f"Динаміка {index_choice} по тижнях")
        st.plotly_chart(fig1, use_container_width=True)
        
    with tab3:
        st.subheader(f"Порівняння {index_choice} з іншими областями")
        #фільтруємо дані для всіх областей за той самий період
        df_all_regions = df_raw[
            (df_raw['Year'] >= year_range[0]) & (df_raw['Year'] <= year_range[1]) &
            (df_raw['Week'] >= week_range[0]) & (df_raw['Week'] <= week_range[1])
        ]
        #рахуємо середнє значення для кожної області для порівняння
        df_compare = df_all_regions.groupby('Province_Name')[index_choice].mean().reset_index()
        
        fig2 = px.bar(df_compare, x='Province_Name', y=index_choice, 
                        color='Province_Name', title=f"Середній {index_choice} за обраний період")
        st.plotly_chart(fig2, use_container_width=True)