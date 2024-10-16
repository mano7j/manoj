import pandas as pd
# from twilio.rest import Client


def detect_heatwaves(data, threshold=30, consecutive_days=3):
    data['heatwave'] = False
    count = 0

    for i in range(len(data)):
        if data['Data.Temperature.Avg Temp'][i] > threshold:
            count += 1
        else:
            count = 0

        if count >= consecutive_days:
            data['heatwave'][i] = True

    return data


# def send_sms(to, message):
#     account_sid = ''
#     auth_token = ''
#     client = Client(account_sid, auth_token)

#     message = client.messages.create(
#         body=message,
#         from_='',
#         to=to
#     )

#     print(f"Message sent to {to}: {message.sid}")


# Load historical temperature data from a CSV file
data = pd.read_csv('D:\INTERN\Task3\historical_temperature_data.csv')

# Apply heatwave detection
data = detect_heatwaves(data)

sms_sent = False

# Check for heatwaves and send notifications
for index, row in data.iterrows():
    if row['heatwave'] and not sms_sent:
        # send_sms('', f"Heatwave detected on {row['Date.Full']} with temperature {row['Data.Temperature.Avg Temp']}°C.")
        # sms_sent = True 
        break
