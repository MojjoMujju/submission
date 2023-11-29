# Streamlit
import streamlit as st
from streamlit_option_menu import option_menu

# Data Manipulation
import pandas as pd

# Data Visualization
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


def main():
    sns.set_style('whitegrid')

    # =============== Import Dataset ==================
    df_CustOrderPayment = pd.read_csv('G:\My Drive\DS_PROJECT_PORTFOLIO\submission\dashboard\main_data.csv')

    df_CustOrderPayment['order_purchase_timestamp'] = pd.to_datetime(df_CustOrderPayment['order_purchase_timestamp'])
    df_CustOrderPayment['order_approved_at'] = pd.to_datetime(df_CustOrderPayment['order_approved_at'])
    df_CustOrderPayment['order_delivered_carrier_date'] = pd.to_datetime(df_CustOrderPayment['order_delivered_carrier_date'])
    df_CustOrderPayment['order_delivered_customer_date'] = pd.to_datetime(df_CustOrderPayment['order_delivered_customer_date'])
    df_CustOrderPayment['order_estimated_delivery_date'] = pd.to_datetime(df_CustOrderPayment['order_estimated_delivery_date'])

    # =============== Helper Function ===================
    # Function to plot lineplot
    def lineplotfunct(df, min_date_filter, max_date_filter, xlabel=str, ylabel=str, title=str, freq=str, metode=str):
        
        dfmasking= df[
            (df['order_approved_at'] >= pd.to_datetime(min_date_filter)) & (df['order_approved_at'] <= pd.to_datetime(max_date_filter))
        ]

        if(metode == 'sum'):
            df_group_masking = dfmasking.groupby(
                by= pd.Grouper(key='order_approved_at', freq=freq))['payment_value'].sum()
        if(metode == 'mean'):
            df_group_masking = dfmasking.groupby(
                by= pd.Grouper(key='order_approved_at', freq=freq))['payment_value'].mean()
        if(metode == 'count'):
            df_group_masking = dfmasking.groupby(
                by= pd.Grouper(key='order_approved_at', freq=freq))['order_approved_at'].count()

        fig, axline= plt.subplots(figsize=(18,8))
        plt.title(
            title,
            pad=40,
            fontdict=({'fontsize':23})
        )

        axline= (
            sns.lineplot(
                x= df_group_masking.index, y= df_group_masking,
                marker= '.',
                markersize= 10,
                markerfacecolor= 'red',
            ),
            axline.set_xlabel(xlabel,fontdict={'fontsize':18}),
            axline.set_ylabel(ylabel,fontdict={'fontsize':18}),
            axline.xaxis.set_major_locator(mdates.MonthLocator(interval=1)),
            axline.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y')),
            plt.xticks(rotation=45)
        )

        return fig

    # lineplotfunct_two (this function specific for Customer State Analysis)
    def lineplotfuncttwo(df, hue=str, xlabel=str, ylabel=str, title=str, freq=str, metode=str):
        
        if(metode == 'sum'):
            df_group_masking = df.groupby(
                by= ['customer_state', pd.Grouper(key='order_approved_at', freq=freq)])['payment_value'].sum()
            df_group_masking =  pd.DataFrame(df_group_masking).reset_index()
        if(metode == 'mean'):
            df_group_masking = df.groupby(
                by= ['customer_state', pd.Grouper(key='order_approved_at', freq=freq)])['payment_value'].mean()
        df_group_masking =  pd.DataFrame(df_group_masking).reset_index()
        if(metode == 'count'):
            df_group_masking = df.groupby(
                by= ['customer_state', pd.Grouper(key='order_approved_at', freq=freq)])['order_approved_at'].count()
        df_group_masking =  pd.DataFrame(df_group_masking).reset_index()

        fig, axline= plt.subplots(figsize=(18,8))
        plt.title(
            title,
            pad=40,
            fontdict=({'fontsize':23})
        )

        axline= (
            sns.lineplot(
                x= df_group_masking['order_approved_at'], y= df_group_masking['payment_value'],
                marker= '.',
                markersize= 10,
                markerfacecolor= 'red',
                hue=df_group_masking[hue]
            ),
            axline.set_xlabel(xlabel,fontdict={'fontsize':18}),
            axline.set_ylabel(ylabel,fontdict={'fontsize':18}),
            axline.xaxis.set_major_locator(mdates.MonthLocator(interval=1)),
            axline.xaxis.set_major_formatter(mdates.DateFormatter('%b-%Y')),
            plt.xticks(rotation=45)
        )

        return fig

    # Function to plot histogram
    def histogramplot(dataframe, start=None, end=None, xlabel=str, ylabel=str, title=str):
        fig, axhist= plt.subplots(figsize=(18,8))
        plt.title(
            title,
            pad=40,
            fontdict=({'fontsize':23})
        )

        dataframe_filter = dataframe[(dataframe >= start) & (dataframe <= end)]
        axhist= (
            sns.histplot(dataframe_filter),
            axhist.set_xlabel(xlabel,fontdict={'fontsize':18}),
            axhist.set_ylabel(ylabel,fontdict={'fontsize':18})
        )

        return fig

    def PlotPiechart(df, title=str):
        
        df_group_masking = df.groupby(
            by= ['payment_type'])['payment_type'].count()
        
        fig, ax = plt.subplots()

        plt.title(
            title,
            fontdict=({'fontsize':18})
        )

        ax.pie(
            df_group_masking,
            labels= df_group_masking.index,
            autopct='%0.01f%%'
        )

        centre_circle = plt.Circle((0,0), 0.7, fc='white')
        plt.Circle((0,0), 0.7, fc='white')
        plt.gcf()
        fig.gca().add_artist(centre_circle)

        return fig

    def plotbarplot(df, title=str):
        
        df_group_masking = df.groupby(
            by= ['customer_state'])['payment_value'].sum()
        
        fig, ax = plt.subplots()

        plt.title(
            title,
            pad=40,
            fontdict=({'fontsize':25})
        )

        ax= (
            ax.bar(
                x= df_group_masking.index,
                height= df_group_masking
            ),
            ax.set_xlabel('State', fontdict=({'fontsize':15})),
            ax.set_ylabel('Total Payment Values', fontdict=({'fontsize':15}))
        )

        return fig

    # =============== Streamlit Main App =================
    min_date = df_CustOrderPayment['order_approved_at'].min()
    max_date = df_CustOrderPayment['order_approved_at'].max()

    with st.sidebar:
        selected= option_menu(
            menu_title="Main menu",
            options= ['Dataset Information', 'RFM Distribution Analysis', 'Trend Analysis', 'Customer State Analysis']
        )

    if selected == 'Dataset Information':
        st.title(f'{selected}')
        st.markdown(
            '<div style="text-align: justify;">Dataset ini mencakup informasi mengenai industri e-commerce pada negara brazil. Data ini memberikan distribusi pelanggan di setiap negara bagian, memungkinkan pemahaman tentang preferensi dan kebiasaan belanja di berbagai wilayah Brazil.</div>', unsafe_allow_html=True)

    if selected == 'RFM Distribution Analysis':
        st.title(f'{selected}')
        st.markdown(
            '<div style="text-align: justify;">RFM analysis adalah metode analisis pelanggan yang digunakan untuk mengkategorikan pelanggan berdasarkan tiga faktor utama: Recency (kebaruan), Frequency (frekuensi), dan Monetary (nilai moneter). Analisis ini membantu bisnis untuk memahami perilaku pelanggan dan mengidentifikasi segmen pelanggan yang berbeda berdasarkan kebiasaan pembelian mereka.</div>', unsafe_allow_html=True)
        st.text(" ")
        tab1, tab2, tab3 = st.tabs(["Recency", "Frequency", "Monetary"])

        def myslider(FilterData):
            start, end = st.select_slider(
                'Filter Your Data',
                options=range(int(FilterData.min()), int(FilterData.max()) + 1),
                value=(int(FilterData.min()), int(FilterData.max()))
            )
            st.write('You selected values between', start, 'and', end)
            return start, end

        with tab1:
            recency = df_CustOrderPayment.groupby('customer_id')['order_approved_at'].max()
            recency = max(recency) - recency
            recency = recency.dt.days
            st.pyplot(histogramplot(recency, start=recency.min(), end=recency.max(), xlabel='Recency', ylabel='Number of Customer', title='Recency Distribution Analysis'))

        with tab2:
            frequency = df_CustOrderPayment.groupby('customer_id')['customer_id'].count()
            start, end = myslider(frequency)
            st.pyplot(histogramplot(frequency, start=start, end=end, xlabel='Frequency', ylabel='Number of Customer', title='Frequency Distribution Analysis'))
        
        with tab3:
            monetary = df_CustOrderPayment.groupby('customer_id')['payment_value'].sum()
            start, end = myslider(monetary)
            st.pyplot(histogramplot(monetary, start=start, end=end, xlabel='Monetary', ylabel='Jumlah Customer', title='Monetary Distribution Analysis'))

    if selected == 'Trend Analysis':
        st.title(f'{selected}')
        st.markdown(
            '<div style="text-align: justify;">Analisis trend melibatkan pemeriksaan data dari waktu ke waktu untuk mengidentifikasi pola, kecenderungan, atau perubahan yang dapat memberikan wawasan tentang arah suatu bisnis atau pasar.</div>',unsafe_allow_html=True
        )
        st.text(" ")

        min_date_filter, max_date_filter= st.sidebar.date_input(
            "Pick a date", 
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date]
        )

        select_freq= st.sidebar.selectbox(
            "Choose Freq (1 Month - 1 Quartile)",
            options= ['1M', '1W', '1D', '1Q']
        )

        tab1, tab2= st.tabs(["Frequency", "Monetary"])

        with tab1:
            st.pyplot(lineplotfunct(df_CustOrderPayment, min_date_filter, max_date_filter, xlabel= 'Tanggal', ylabel= 'Jumlah Pesanan', title='Trend Banyaknya Pesanan', freq=select_freq, metode='count'))

        with tab2:
            st.pyplot(lineplotfunct(df_CustOrderPayment, min_date_filter, max_date_filter, xlabel= 'Tanggal', ylabel= 'Jumlah Pendapatan', title='Trend Jumlah pendapatan', freq=select_freq, metode='sum'))
            st.pyplot(lineplotfunct(df_CustOrderPayment, min_date_filter, max_date_filter, xlabel= 'Tanggal', ylabel= 'Rata-rata Jumlah Pendapatan', title='Trend rata-rata Jumlah Pendapatan', freq=select_freq, metode='mean'))

    if selected == 'Customer State Analysis':
        st.title('Customer State Analysis')
        st.markdown(
            """
            <div style="text-align: justify;">
                Disini, dilakukan analisis data berdasarkan negara pelanggan. 
                Data ini memberikan wawasan bagaimana preferensi dan kebiasaan pelanggan setiap negara bagian. 
                Melalui eksplorasi data ini, kami berharap dapat mengidentifikasi tren 
                dan memberikan pandangan terkait pelanggan, untuk meningkatkan pemahaman akan strategi pemasaran di setiap wilayah negara bagian.
            </div> 
            """
            , unsafe_allow_html=True
        )
        st.tabs(['  '])
        st.text(" ")

        options = ['All'] + list(df_CustOrderPayment['customer_state'].unique())

        state= st.sidebar.multiselect(
            'Select Customer State',
            options= df_CustOrderPayment['customer_state'].unique(),
        )

        Selection_state= df_CustOrderPayment.query(
            "customer_state == @state"
        )

        select_freq= st.sidebar.selectbox(
            "Choose Freq (1 Month - 1 Quartile)",
            options= ['1M', '1W', '1D', '1Q']
        )

        col1, col2, col3 = st.columns(3)
        col1.caption('Total Payment Value')
        col1.subheader(round(Selection_state['payment_value'].sum(), 3))
        col2.caption('Average Payment Value')
        col2.subheader(round(Selection_state['payment_value'].mean(), 3))
        col3.caption('Total Jumlah Penjualan')
        col3.subheader(Selection_state['payment_value'].count())

        st.markdown("\n\n\n")

        col4, col5 = st.columns(2)
        col4.pyplot(plotbarplot(Selection_state, title='Total Payment Values by State'))
        col5.pyplot(PlotPiechart(Selection_state, title= 'Payment Types'))
        st.pyplot(lineplotfuncttwo(Selection_state, hue= 'customer_state', xlabel='Tanggal', ylabel="Trend Jumlah Pendapatan", title="Jumlah Pendapatan by State", freq=select_freq, metode="sum"))

        
    st.sidebar.text("  ")    
    st.sidebar.text("  ")      

if __name__ == "__main__":
    main()