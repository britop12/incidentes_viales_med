import streamlit as st
import datetime as dt
import pandas as pd
import numpy as np
import holidays
import joblib

st.set_page_config(page_title="Predicción de Accidentes")

df_diary = pd.read_csv('datasets/dairy_2019.csv')
df_weekly = pd.read_csv('datasets/weekly_2019.csv')
df_monthly = pd.read_csv('datasets/monthly_2019.csv')
model_diary = joblib.load('models/lr_model_diary.pkl')
model_monthly = joblib.load('models/lr_model_monthly.pkl')
model_weekly = joblib.load('models/lr_model_weekly.pkl')


def is_fortnight(month, day):
    if day == 15 or day == 30:
        return True
    if month == 2 and day == 28:
        return True
    return False


def main():
    global df_diary
    st.title('Predicción de incidentes viales en la ciudad de Medellín')
    start = st.date_input('Fecha inicial', dt.date(2023, 10, 27))
    end = st.date_input('Fecha final')
    class_accident = st.selectbox('¿Qué tipo de accidente quieres predecir:',
                                  ['Caida Ocupante', 'Choque', 'Atropello',
                                   'Volcamiento', 'Incendio', 'Otro'])

    window = st.selectbox('¿Que ventana de tiempo desea utilizar?',
                          ['Diaria', 'Semanal', 'Mensual'])

    map_class_accident = {
        'Choque': 'choque',
        'Atropello': 'atropello',
        'Caida Ocupante': 'caida',
        'Otro': 'otro',
        'Volcamiento': 'volcamiento',
        'Incendio': 'incendio'
    }
    input_data = []

    if st.button("Ejecutar"):
        if window == 'Diaria':
            for date in pd.date_range(start, end):
                data = {
                    'year': date.year,
                    'month': date.month,
                    'day': date.day,
                    'day_of_week': date.weekday(),
                    'is_weekend': (date.dayofweek in [5, 6])*1,
                    'is_holiday': date in holidays.CO(),
                    'is_fortnight': is_fortnight(date.month, date.day),
                    'quarter': date.quarter,
                    'weekofyear': date.weekofyear,
                    'sin_week': np.sin(2*np.pi*date.weekday()/7),
                    'cos_week': np.cos(2*np.pi*date.weekday()/7),
                    'date': date,
                }
                data['lag_1'] = df_diary[(df_diary['year'] == 2019) & (
                    df_diary['month'] == data['month']) & (df_diary['day'] == data['day'])]['lag_1'].values[0]
                
                data['lag_2'] = df_diary[(df_diary['year'] == 2019) & (
                    df_diary['month'] == data['month']) & (df_diary['day'] == data['day'])]['lag_2'].values[0]
                
                data['lag_3'] = df_diary[(df_diary['year'] == 2019) & (
                    df_diary['month'] == data['month']) & (df_diary['day'] == data['day'])]['lag_3'].values[0]
                
                data['lag_4'] = df_diary[(df_diary['year'] == 2019) & (
                    df_diary['month'] == data['month']) & (df_diary['day'] == data['day'])]['lag_4'].values[0]
                
                data['lag_5'] = df_diary[(df_diary['year'] == 2019) & (
                    df_diary['month'] == data['month']) & (df_diary['day'] == data['day'])]['lag_5'].values[0]
                
                data['lag_6'] = df_diary[(df_diary['year'] == 2019) & (
                    df_diary['month'] == data['month']) & (df_diary['day'] == data['day'])]['lag_6'].values[0]
                
                data['lag_7'] = df_diary[(df_diary['year'] == 2019) & (
                    df_diary['month'] == data['month']) & (df_diary['day'] == data['day'])]['lag_7'].values[0]

                data['rolling_mean_7'] = df_diary[(df_diary['year'] == 2019) & (
                    df_diary['month'] == data['month']) & (df_diary['day'] == data['day'])]['rolling_mean_7'].values[0]
                
                data['rolling_mean_3'] = df_diary[(df_diary['year'] == 2019) & (
                    df_diary['month'] == data['month']) & (df_diary['day'] == data['day'])]['rolling_mean_3'].values[0]
                input_data.append(data)

            df = pd.DataFrame(input_data)
            y = model_diary.predict(df.drop(columns=['date']))
            y[y < 0] = 0
            df = pd.concat([df, pd.DataFrame(y.astype(int))], axis=1)
            df.rename(columns={
                0: 'choque', 1: 'atropello', 2: 'caida',
                3: 'otro', 4: 'volcamiento', 5: 'incendio'
            },
                inplace=True)
            
            st.line_chart(df, x='date', y=map_class_accident[class_accident])

        if window == 'Semanal':
            for date in pd.date_range(start, end):
                data = {
                    'year': date.year,
                    'weekofyear': date.weekofyear,
                    'is_holiday': date in holidays.CO(),
                    'is_start_month': date.is_month_start,
                    'is_end_month': date.is_month_end,
                    'is_fortnight': date.day in [15, 30],
                    'date': date,
                }

                data["date_next_week"] = date + dt.timedelta(days=7)
                data['is_holiday_next_week'] = data["date_next_week"] in holidays.CO()
                
                # Delete date_next_week
                del data["date_next_week"]

                data['lag_1'] = df_weekly[(df_weekly['year'] == 2019) & (
                    df_weekly['weekofyear'] == data['weekofyear'])]['lag_1'].values[0]
                
                data['lag_2'] = df_weekly[(df_weekly['year'] == 2019) & (
                    df_weekly['weekofyear'] == data['weekofyear'])]['lag_2'].values[0]
                
                data['lag_3'] = df_weekly[(df_weekly['year'] == 2019) & (
                    df_weekly['weekofyear'] == data['weekofyear'])]['lag_3'].values[0]
                
                data['lag_52'] = df_weekly[(df_weekly['year'] == 2019) & (
                    df_weekly['weekofyear'] == data['weekofyear'])]['lag_52'].values[0]
                
                data['rolling_mean_3'] = df_weekly[(df_weekly['year'] == 2019) & (
                    df_weekly['weekofyear'] == data['weekofyear'])]['rolling_mean_3'].values[0]
                
                input_data.append(data)

            df = pd.DataFrame(input_data)
            y = model_weekly.predict(df.drop(columns=['date']))
            y[y < 0] = 0
            df = pd.concat([df, pd.DataFrame(y.astype(int))], axis=1)
            df.rename(columns={
                0: 'choque', 1: 'atropello', 2: 'caida',
                3: 'otro', 4: 'volcamiento', 5: 'incendio'
            },
                inplace=True)

            
            st.line_chart(df, x='weekofyear', y=map_class_accident[class_accident])

        if window == "Mensual":
            for date in pd.date_range(start, end):
                data = {
                    'date': date,
                    'year': date.year,
                    'month': date.month,
                    'day' : date.day,}
                input_data.append(data)

            data_df = pd.DataFrame(input_data)
            data_df["is_holiday"] = data_df["date"].isin(holidays.CO())

            df = data_df.groupby(["year", "month"]).agg({"is_holiday": "sum"}).reset_index()
            df['date'] = pd.to_datetime(df[['year', 'month']].assign(Day=1))

            df['days_in_month'] = df['date'].dt.daysinmonth
            df["num_weekends"] = df["days_in_month"].apply(lambda x: x//7)

            df['lag_1'] = df_monthly[(df_monthly['year'] == 2019) & (
                df_monthly['month'] == data['month'])]['lag_1'].values[0]
            
            df['lag_2'] = df_monthly[(df_monthly['year'] == 2019) & (
                df_monthly['month'] == data['month'])]['lag_2'].values[0]
            
            df['lag_3'] = df_monthly[(df_monthly['year'] == 2019) & (
                df_monthly['month'] == data['month'])]['lag_3'].values[0]
            
            df['lag_6'] = df_monthly[(df_monthly['year'] == 2019) & (
                df_monthly['month'] == data['month'])]['lag_6'].values[0]
            
            df["rolling_mean_3"] = df_monthly[(df_monthly['year'] == 2019) & (
                df_monthly['month'] == data['month'])]['rolling_mean_3'].values[0]
            
            y = model_monthly.predict(df.drop(columns=['date']))
            y[y < 0] = 0
            df = pd.concat([df, pd.DataFrame(y.astype(int))], axis=1)
            df.rename(columns={
                0: 'choque', 1: 'atropello', 2: 'caida',
                3: 'otro', 4: 'volcamiento', 5: 'incendio'
            },
                inplace=True)
            
            ### agregar columna para mostrar año y mes
            df['month'] = df['date'].dt.month_name()
            df['year'] = df['date'].dt.year
            df['date'] = df['month'] + ' ' + df['year'].astype(str)

            st.line_chart(df, x='date', y=map_class_accident[class_accident])

if __name__ == '__main__':
    main()
