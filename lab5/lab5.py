import streamlit as st
import pandas as pd
import plotly.express as px

# Налаштування сторінки
st.set_page_config(layout="wide", page_title="Аналіз VHI Даних")

# --- ЗАВАНТАЖЕННЯ ДАНИХ ---
@st.cache_data
def load_data():
    # Завантажуємо твій файл
    # Переконайся, що файл лежить в тій же папці, що і цей скрипт
    df = pd.read_csv('final_vhi_data.csv')
    
    # Видаляємо зайві пробіли в назвах колонок, якщо вони є
    df.columns = df.columns.str.strip()
    return df

try:
    df_raw = load_data()
except FileNotFoundError:
    st.error("Файл 'final_vhi_data.csv' не знайдено! Поклади його в папку з кодом.")
    st.stop()

# --- ЛОГІКА СКИДАННЯ ФІЛЬТРІВ ---
def reset_filters():
    st.session_state.year_range = (int(df_raw['Year'].min()), int(df_raw['Year'].max()))
    st.session_state.week_range = (1, 52)
    st.session_state.region = df_raw['Province_Name'].unique()[0]
    st.session_state.index_type = 'VHI'
    st.session_state.sort_asc = False
    st.session_state.sort_desc = False

# Ініціалізація стану, якщо треба
if 'year_range' not in st.session_state:
    reset_filters()

# --- ІНТЕРФЕЙС (COLUMNS) ---
col1, col2 = st.columns([1, 3])

with col1:
    st.header("Налаштування")
    
    # 1. Dropdown для вибору індексу
    index_choice = st.selectbox("Оберіть показник", ['VCI', 'TCI', 'VHI'], key='index_type')
    
    # 2. Dropdown для вибору області
    region_choice = st.selectbox("Оберіть область", df_raw['Province_Name'].unique(), key='region')
    
    # 3. Slider для років (автоматично від мін до макс у файлі)
    min_year = int(df_raw['Year'].min())
    max_year = int(df_raw['Year'].max())
    year_range = st.slider("Інтервал років", min_year, max_year, key='year_range')
    
    # 4. Slider для тижнів
    week_range = st.slider("Інтервал тижнів", 1, 52, key='week_range')
    
    # 5. Checkboxes для сортування
    st.subheader("Сортування")
    c1, c2 = st.columns(2)
    with c1:
        sort_asc = st.checkbox("Зростання", key='sort_asc')
    with c2:
        sort_desc = st.checkbox("Спадання", key='sort_desc')
    
    if sort_asc and sort_desc:
        st.warning("⚠️ Оберіть щось одне")

    # 6. Button для скидання
    st.button("Скинути фільтри", on_click=reset_filters)

# --- ФІЛЬТРАЦІЯ ---
df_filtered = df_raw[
    (df_raw['Province_Name'] == region_choice) &
    (df_raw['Year'] >= year_range[0]) & (df_raw['Year'] <= year_range[1]) &
    (df_raw['Week'] >= week_range[0]) & (df_raw['Week'] <= week_range[1])
]

# Обробка сортування
if sort_asc and not sort_desc:
    df_filtered = df_filtered.sort_values(by=index_choice, ascending=True)
elif sort_desc and not sort_asc:
    df_filtered = df_filtered.sort_values(by=index_choice, ascending=False)

# --- ВІДОБРАЖЕННЯ (TABS) ---
with col2:
    tab1, tab2, tab3 = st.tabs(["Таблиця", "Часовий ряд", "Порівняння областей"])
    
    with tab1:
        st.dataframe(df_filtered, use_container_width=True)
    
    with tab2:
        st.subheader(f"Графік {index_choice} для області {region_choice}")
        # Створюємо графік (X - це комбінація року та тижня для лінійності)
        fig1 = px.line(df_filtered, x='Year', y=index_choice, color='Week',
                       markers=True, title=f"Динаміка {index_choice} по тижнях")
        st.plotly_chart(fig1, use_container_width=True)
        
    with tab3:
        st.subheader(f"Порівняння {index_choice} з іншими областями")
        # Фільтруємо дані для всіх областей за той самий період
        df_all_regions = df_raw[
            (df_raw['Year'] >= year_range[0]) & (df_raw['Year'] <= year_range[1]) &
            (df_raw['Week'] >= week_range[0]) & (df_raw['Week'] <= week_range[1])
        ]
        # Рахуємо середнє значення для кожної області для порівняння
        df_compare = df_all_regions.groupby('Province_Name')[index_choice].mean().reset_index()
        
        fig2 = px.bar(df_compare, x='Province_Name', y=index_choice, 
                      color='Province_Name', title=f"Середній {index_choice} за обраний період")
        st.plotly_chart(fig2, use_container_width=True)