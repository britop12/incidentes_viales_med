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

    window = st.selectbox('¿Que ventana de tiempo desea utilizar?',
                          ['Diaria', 'Semanal', 'Mensual'])

    map_class_accident = {
        'Choque': 'choque',
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
                    'quarter': date.quarter,
                    'weekofyear': date.weekofyear,
                    'is_fortnight': is_fortnight(date.month, date.day), 
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
                data['sin_week'] = np.sin(2*np.pi*date.weekday()/7)
                data['cos_week'] = np.cos(2*np.pi*date.weekday()/7)
                input_data.append(data)

            df = pd.DataFrame(input_data)

            y = model_diary.predict(df.drop(columns=['date']))
            y[y < 0] = 0
            df = pd.concat([df, pd.DataFrame(y.astype(int))], axis=1)
            df['date'] = df['date'].dt.strftime('%d/%m/%Y')
            df.rename(columns={0: 'Predicción de choques', 'date': "Fecha"}, inplace=True)
            df.index = df['Fecha']

            st.write(df[['Predicción de choques']])
            

        if window == 'Semanal':
            for date in pd.date_range(start, end):
                data = {
                    'year': date.year,
                    'weekofyear': date.weekofyear,
                    'is_holiday': date in holidays.CO(),
                    'is_holiday_next_week': date + dt.timedelta(days=7) in holidays.CO(),
                    'is_start_month': date.is_month_start,
                    'is_end_month': date.is_month_end,
                    'is_fortnight': date.day in [15, 30],
                    'date': date,
                }
                

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
            df['Fecha'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
            df.rename(columns={0: 'Predicción de choques',}, inplace=True)
            df['Semana del año'] = df['Fecha'].dt.strftime('%U')
            df_semanal = df.groupby('Semana del año').agg({'Fecha': ['min', 'max'], "Predicción de choques": 'mean'})

            df_semanal.columns = ['_'.join(col).strip() for col in df_semanal.columns.values]

            # Convertir el promedio a entero
            df_semanal['Predicción de choques_mean'] = df_semanal['Predicción de choques_mean'].astype(int)
            df_semanal['Fecha_min'] = df_semanal['Fecha_min'].dt.strftime('%d/%m/%Y')
            df_semanal['Fecha_max'] = df_semanal['Fecha_max'].dt.strftime('%d/%m/%Y')

            # Renombrar las columnas
            df_semanal.columns = ['Fecha Inicial', 'Fecha Final', "Predicción de choques"]
            st.write(df_semanal)
            

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
            df['date'] = df['date'].dt.strftime('%m/%Y')
            df.rename(columns={0: 'Predicción de choques', 'date': "Mes"}, inplace=True)
            df.index = df['Mes']

            st.write(df[['Predicción de choques']])
           

if __name__ == '__main__':
    main()
