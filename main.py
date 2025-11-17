import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

data = pd.read_excel('data/Total_Sales.xlsx')

#membuat dataframe baru yang berisi rata-rata profit berdasarkan model
data['PPV'] = data['Profit'] / data['Quantity Sold']
avg_model_profit = data.groupby(['Model'])['PPV'].mean().reset_index().round(2).sort_values(by='PPV', ascending=False)

# menambahkan column quarter yang sesuai dengan bulan penjualan
data['Quarter'] = data['Date'].dt.to_period('Q').astype(str)

# membuat dataframe baru yang berisi total quantity sold per quarter di tahun 2024 dan 2025
quarterly_sales_trend = data.groupby('Quarter')[['Quantity Sold']].sum().reset_index().round(2)
quarterly_sales_trend = quarterly_sales_trend[quarterly_sales_trend['Quarter'].str.startswith(('2024', '2025'))]

dealer_yoy = data.groupby(['Dealer ID', 'Year'])['Profit'].sum().reset_index()
dealer_yoy['Growth'] = dealer_yoy.groupby('Dealer ID')['Profit'].pct_change().fillna(0).round(4) * 100

# menghitung rata-rata growth rate per dealer
dealer_avg_growth = dealer_yoy.groupby('Dealer ID').agg({'Growth':'mean'}).round(2).sort_values(by='Growth', ascending=False)
plt.figure(figsize=(10, 8))
plt.suptitle('Data Visualization')

plt.subplot(221)
plt.bar(avg_model_profit['Model'], avg_model_profit['PPV'], color='skyblue')
plt.grid(linestyle='--', alpha=0.5)
plt.title('Average Profit per Model')
plt.xlabel('Model')
plt.ylabel('Average Profit')
plt.xticks(fontsize=9)
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))

plt.subplot(222)
plt.plot(quarterly_sales_trend['Quarter'], quarterly_sales_trend['Quantity Sold'], color='skyblue')
plt.grid(linestyle='--', alpha=0.5)
plt.title('Total Unit Sold per Quarter')
plt.xlabel('Quarter')
plt.ylabel('Total Unit Sold')
plt.xticks(fontsize=7)
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))

plt.subplot(223)
for dealer in dealer_yoy['Dealer ID'].unique():
    dealer_data = dealer_yoy[dealer_yoy['Dealer ID'] == dealer]
    plt.plot(dealer_data['Year'].astype('str'), dealer_data['Growth'], label=dealer)
plt.grid(linestyle='--', alpha=0.5)
plt.title('Total Profit Growth per Dealer')
plt.xlabel('Year')
plt.ylabel('Growth')
plt.legend(loc='lower left')
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:.1f}%'))

plt.subplot(224)
plt.bar(dealer_avg_growth.index.astype('str'), dealer_avg_growth['Growth'], color='skyblue')
plt.grid(linestyle='--', alpha=0.5)
plt.title('Average Profit Growth per Dealer')
plt.xlabel('Dealer')
plt.ylabel('Average Growth')
plt.xticks(fontsize=8)
plt.gca().yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:.1f}%'))

plt.tight_layout()
plt.show()