import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime

# Load data
day_df = pd.read_csv("https://raw.githubusercontent.com/alalghzy/submission_analisis_data/main/dashboard/day_data.csv")
hour_df = pd.read_csv("https://raw.githubusercontent.com/alalghzy/submission_analisis_data/main/dashboard/hour_data.csv")

custom_palette = ['#d0deec', '#97b2cc', '#8a9296']
bulan = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

day_df['month'] = pd.Categorical(day_df['month'], categories=bulan, ordered=True)

# Mengelompokkan berdasarkan bulan dan tahun
monthly_counts = day_df.groupby(by=["month", "year"]).agg({
    "count": "sum"
}).reset_index()

seasonal_usage = day_df.groupby('season').sum(numeric_only=True).reset_index()

seasonal_usage_year = day_df.groupby(['year', 'season']).sum(numeric_only=True).reset_index()

colors = ['#8C1C04', '#b7d657', '#ffc800', '#00b4cb']

# Menyiapkan daily_rent_df
def create_daily_rent_df(df):
    daily_rent_df = df.groupby(by='dateday').agg({
        'count': 'sum'
    }).reset_index()
    return daily_rent_df

# Menyiapkan daily_casual_rent_df
def create_daily_casual_rent_df(df):
    daily_casual_rent_df = df.groupby(by='dateday').agg({
        'casual': 'sum'
    }).reset_index()
    return daily_casual_rent_df

# Menyiapkan daily_registered_rent_df
def create_daily_registered_rent_df(df):
    daily_registered_rent_df = df.groupby(by='dateday').agg({
        'registered': 'sum'
    }).reset_index()
    return daily_registered_rent_df

# Menyiapkan season_rent_df
def create_season_rent_df(df):
    season_rent_df = df.groupby(by='season')[['registered', 'casual']].sum().reset_index()
    return season_rent_df

# Menyiapkan monthly_rent_df
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({
        'count': 'sum'
    })
    ordered_months = [
        'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Menyiapkan weekday_rent_df
def create_weekday_rent_df(df):
    weekday_rent_df = df.groupby(by='weekday').agg({
        'count': 'sum'
    }).reset_index()
    return weekday_rent_df

# Menyiapkan workingday_rent_df
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({
        'count': 'sum'
    }).reset_index()
    return workingday_rent_df

# Menyiapkan holiday_rent_df
def create_holiday_rent_df(df):
    holiday_rent_df = df.groupby(by='holiday').agg({
        'count': 'sum'
    }).reset_index()
    return holiday_rent_df

# Menyiapkan weather_rent_df
def create_weather_rent_df(df):
    weather_rent_df = df.groupby(by='weather_cond').agg({
        'count': 'sum'
    })
    return weather_rent_df

# Membuat komponen filter
min_date = pd.to_datetime(day_df['dateday']).dt.date.min()
max_date = pd.to_datetime(day_df['dateday']).dt.date.max()

with st.sidebar:
    st.image('seepeda.png', caption='seepeda')
    
    # Mengambil start_date dari date_input
    start_date = st.date_input(
        label='Pilih Tanggal Awal',
        min_value=min_date,
        max_value=max_date,
        value=min_date
    )
    
    # Mengambil end_date dari date_input
    end_date = st.date_input(
        label='Pilih Tanggal Akhir',
        min_value=min_date,
        max_value=max_date,
        value=max_date
    )

main_df = day_df[(day_df['dateday'] >= str(start_date)) & 
                (day_df['dateday'] <= str(end_date))]

# Menyiapkan berbagai dataframe
daily_rent_df = create_daily_rent_df(main_df)
daily_casual_rent_df = create_daily_casual_rent_df(main_df)
daily_registered_rent_df = create_daily_registered_rent_df(main_df)
season_rent_df = create_season_rent_df(main_df)
monthly_rent_df = create_monthly_rent_df(main_df)
weekday_rent_df = create_weekday_rent_df(main_df)
workingday_rent_df = create_workingday_rent_df(main_df)
holiday_rent_df = create_holiday_rent_df(main_df)
weather_rent_df = create_weather_rent_df(main_df)

# Membuat Dashboard secara lengkap

# Membuat judul
st.header('Seepeda✨')
st.subheader('[Bike Sharing]', divider='rainbow')

# Membuat jumlah penyewaan harian
st.subheader('Peminjam Seepeda')
col1, col2, col3 = st.columns(3)

with col1:
    daily_rent_casual = daily_casual_rent_df['casual'].sum()
    st.metric('Peminjam Biasa', value=daily_rent_casual)

with col2:
    daily_rent_registered = daily_registered_rent_df['registered'].sum()
    st.metric('Peminjam Terdaftar', value=daily_rent_registered)

with col3:
    daily_rent_total = daily_rent_df['count'].sum()
    st.metric('Total Peminjam', value=daily_rent_total)
    
st.divider()

# Membuat jumlah penyewaan bulanan
st.subheader('Peminjam Bulanan Berdasarkan Rentang Waktu')
fig, ax = plt.subplots(figsize=(30, 10))
ax.plot(
    monthly_rent_df.index,
    monthly_rent_df['count'],
    marker='o', 
    linewidth=2,
    color='tab:blue'
)

for index, row in enumerate(monthly_rent_df['count']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
plt.xlabel('Bulan')
plt.ylabel('Jumlah Pengguna Sepeda')
st.pyplot(fig)

st.divider()

selected_chart = st.selectbox('Pilih Grafik',
                            ('Jumlah Pengguna Sepeda berdasarkan Kondisi Cuaca',
                            'Jumlah Pengguna Sepeda per Bulan untuk Setiap Tahun',
                            'Jumlah Penyewaan Sepeda berdasarkan Musim',))

if selected_chart == 'Jumlah Pengguna Sepeda berdasarkan Kondisi Cuaca':
    st.subheader('Jumlah Pengguna Sepeda berdasarkan Kondisi Cuaca')

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=day_df,
        x='weather_cond',
        y='count',
        hue='weather_cond',
        palette=custom_palette,
        ax=ax
    )
    plt.title('Jumlah Pengguna Sepeda berdasarkan Kondisi Cuaca')
    plt.xlabel('Kondisi Cuaca')
    plt.ylabel('Jumlah Pengguna Sepeda')
    st.pyplot(fig)

elif selected_chart == 'Jumlah Pengguna Sepeda per Bulan untuk Setiap Tahun':
    st.subheader('Jumlah Pengguna Sepeda per Bulan untuk Setiap Tahun')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=monthly_counts,
        x="month",
        y="count",
        hue="year",
        palette="tab10",
        ax=ax
    )
    plt.title("Jumlah Pengguna Sepeda per Bulan untuk Setiap Tahun")
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah")
    plt.legend(title="Tahun", loc="upper right")
    st.pyplot(fig)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(
        data=monthly_counts,
        x="month",
        y="count",
        hue="year",
        palette="tab10",
        marker="o",
        ax=ax
    )
    plt.title("Jumlah Pengguna Sepeda per Bulan untuk Setiap Tahun")
    plt.xlabel("Bulan")
    plt.ylabel("Jumlah")
    plt.legend(title="Tahun", loc="upper right")
    st.pyplot(fig)

elif selected_chart == 'Jumlah Penyewaan Sepeda berdasarkan Musim':
    st.subheader('Jumlah Penyewaan Sepeda berdasarkan Musim')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=seasonal_usage,
        x='season',
        y='count',
        palette=colors,
        ax=ax
    )
    plt.xlabel("Musim")
    plt.ylabel("Jumlah")
    plt.title("Jumlah Penyewaan Sepeda berdasarkan Musim")
    st.pyplot(fig)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=seasonal_usage_year,
        x='season',
        y='count',
        hue='year',
        ax=ax
    )
    plt.xlabel("Musim")
    plt.ylabel("Jumlah")
    plt.title("Jumlah Peminjaman Sepeda berdasarkan Musim untuk Setiap Tahun")
    plt.legend(title='Tahun')
    st.pyplot(fig)

st.markdown('---')
st.caption('Copyright (c) alalghzy 2024')
