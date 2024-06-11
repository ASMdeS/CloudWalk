from datetime import datetime
import pytz
from Analyzing_the_Data import means, standard_deviations
import pandas as pd
from send_email import write_email
import matplotlib.pyplot as plt
import making_requests


def detect_anomaly():
    gmt_sao_paulo = pytz.timezone('America/Sao_Paulo')
    current_time_sao_paulo = datetime.now(gmt_sao_paulo)
    formatted_time = current_time_sao_paulo.strftime("%Hh %M")
    file_path = 'transactions_1.csv'
    df = pd.read_csv(file_path)
    filtered_time = hello.get_rows_by_time("http://localhost:5000", formatted_time)
    sum_filtered = filtered_time.sum(numeric_only=True)
    total_sum = sum_filtered.sum()
    print(filtered_time)
    print(total_sum)
    if total_sum > 2:
        print("hjodnisocda")
        if 'denied' in filtered_time['status'].values:
            denied_payments = filtered_time.loc[filtered_time['status'] == 'denied', 'f0_'].values[0]
            if (((denied_payments / total_sum) - means['denied']) / standard_deviations['denied']) > 3:
                message_to_send = 'Risk of issuer: denied payment'
                print(message_to_send)
                write_email(message_to_send)
            else:
                print('No risk of issuer (deny)')
        else:
            print('not denied')
        if 'failed' in filtered_time.columns:
            failed_payments = filtered_time.loc[filtered_time['status'] == 'failed', 'f0_'].values[0]
            if (((failed_payments / total_sum) - means['failed']) / standard_deviations['failed']) > 3:
                message_to_send = 'Transaction with problem: failed payment'
                print(message_to_send)
                write_email(message_to_send)
            else:
                print('No problem detected (failure)')
        if 'reversed' in filtered_time.columns:
            reversed_payments = filtered_time.loc[filtered_time['status'] == 'reversed', 'f0_'].values[0]
            if (((reversed_payments / total_sum) - means['reversed']) / standard_deviations['reversed']) > 3:
                message_to_send = 'Transaction with problem: reversed payment'
                print(message_to_send)
            else:
                print('No problem detected (reversion)')
    grouped = filtered_time.groupby('status')['f0_'].sum()

    # Plot as a column chart
    color_map = {status: plt.cm.tab10(i) for i, status in enumerate(grouped.index)}

    # Plot as a column chart with colors based on 'status'
    grouped.plot(kind='bar', color=[color_map[status] for status in grouped.index])
    plt.title('Status vs. Count')
    plt.xlabel('Status')
    plt.ylabel('Count')
    plt.xticks(rotation=0)  # Rotate x-axis labels if needed
    plt.show(block=False)
    plt.pause(58)
    plt.close()


while True:
    detect_anomaly()
