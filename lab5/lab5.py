import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# налаштування сторінки (робимо її широкою)
st.set_page_config(layout="wide")

# завантаження даних (заміни 'data.csv' на свій файл з лаби 2)
@st.cache_data
def load_data():
    # тут має бути твій шлях до файлу
    df = pd.read_csv('vhi_data.csv') 
    return df

df = load_data()

# мапа областей (приклад, додай свої або витягни з df)
provinces = {
    1: "Вінницька", 2: "Волинська", 3: "Дніпропетровська", 4: "Донецька", 5: "Житомирська",
    # ... додай решту
}

# заголовок додатка
st.title("Аналіз індексів VCI, TCI, VHI по областях України")

# створення двох колонок: ліва для фільтрів, права для графіків
col1, col2 = st.columns([1, 3])

with col1:
    st.header("Налаштування фільтрів")
    
    # функція для скидання (використовуємо session_state)
    if st.button("Скинути всі фільтри"):
        st.rerun()

    # 1. dropdown для вибору індексу
    index_choice = st.selectbox("Оберіть часовий ряд:", ["VCI", "TCI", "VHI"])
    
    # 2. dropdown для вибору області
    province_id = st.selectbox("Оберіть область:", options=list(provinces.keys()), 
                               format_func=lambda x: provinces[x])
    
    # 3. slider для інтервалу тижнів
    week_range = st.slider("Інтервал тижнів:", 1, 52, (1, 52))
    
    # 4. slider для інтервалу років
    min_year = int(df['Year'].min())
    max_year = int(df['Year'].max())
    year_range = st.slider("Інтервал років:", min_year, max_year, (min_year, max_year))

    # чекбокси для сортування
    st.subheader("Сортування таблиці")
    sort_asc = st.checkbox("За зростанням")
    sort_desc = st.checkbox("За спаданням")

    # логіка реакції на два увімкнені чекбокси
    if sort_asc and sort_desc:
        st.warning("Обрано обидва типи сортування. Буде застосовано сортування за зростанням.")

# фільтрація даних
filtered_df = df[
    (df['Province_ID'] == province_id) &
    (df['Year'].between(year_range[0], year_range[1])) &
    (df['Week'].between(week_range[0], week_range[1]))
]

# логіка сортування
if sort_asc:
    filtered_df = filtered_df.sort_values(by=index_choice, ascending=True)
elif sort_desc:
    filtered_df = filtered_df.sort_values(by=index_choice, ascending=False)

with col2:
    # створення вкладок
    tab_table, tab_plot, tab_compare = st.tabs(["📊 Таблиця даних", "📈 Графік", "🌍 Порівняння областей"])

    with tab_table:
        st.subheader(f"Дані для області: {provinces[province_id]}")
        st.dataframe(filtered_df, use_container_width=True)

    with tab_plot:
        st.subheader(f"Динаміка {index_choice}")
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(filtered_df['Year'].astype(str) + "-" + filtered_df['Week'].astype(str), 
                filtered_df[index_choice], marker='o', linestyle='-', color='purple')
        ax.set_xlabel("Час (Рік-Тиждень)")
        ax.set_ylabel(index_choice)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with tab_compare:
        st.subheader(f"Порівняння {index_choice} з іншими областями")
        
        # дані для порівняння (всі області за той самий період)
        compare_df = df[
            (df['Year'].between(year_range[0], year_range[1])) &
            (df['Week'].between(week_range[0], week_range[1]))
        ]
        
        # групуємо по роках для наочності порівняння
        pivot_df = compare_df.groupby(['Year', 'Province_ID'])[index_choice].mean().unstack()
        
        fig2, ax2 = plt.subplots(figsize=(10, 5))
        # малюємо обрану область жирною лінією
        ax2.plot(pivot_df.index, pivot_df[province_id], label=f"{provinces[province_id]} (Обрана)", 
                 linewidth=4, color='red', marker='s')
        
        # малюємо інші області тонкими лініями
        for col in pivot_df.columns:
            if col != province_id:
                ax2.plot(pivot_df.index, pivot_df[col], alpha=0.3, label=provinces.get(col, f"ID {col}"))
        
        ax2.set_title(f"Середній {index_choice} по роках")
        ax2.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small', ncol=2)
        st.pyplot(fig2)