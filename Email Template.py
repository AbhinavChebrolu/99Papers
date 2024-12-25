import pandas as pd
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import os

# Set limits and constants
MAIL_LIMIT = 70  # Limit per sender per day
TIME_GAP = 900  # 15 minutes in seconds
EMAIL_LOG_FILE = 'email_log.csv'
DAILY_COUNT_LOG_FILE = 'daily_count_log.csv'
HTML_CONTENT_FILE = '99papers-content.html'
ALIAS_TEXT = """<p>Hello Team,&nbsp;</p>
<p>Best wishes on the successful incorporation of your company! and Welcome to the business ecosystem.</p>
<p>You must have received the company documents such as AoA, MoA and Certificate of Incorporation from the Ministry of Corporate Affairs. However, many other documents are essential for a company to operate without facing any legal trouble. As overwhelming as it is to start a new company, the burden of the sorting out the required formalities and documentation often adds to the worries, leading to missed deadlines and high penalties. Essential Legal &amp; HR Documents bundle by&nbsp;<span class="il">99papers</span>&nbsp;is a set of pre-prepared editable documents required at different stages of the company, which can be used directly only by affixign your company letterhead to it.&nbsp;</p>
<p>At&nbsp;<a href="https://www.99papers.in/">99papers.in</a>, we take pride in offering a vast array of esteemed documents tailored to meet the diverse requirements of your organisation. Whether you are navigating through lawful intricacies, streamlining HR processes, or seeking templates for various business activities, we have got you covered.</p>
<p>The bundle contains documents fit for a wide range of processes &amp; applications such as -&nbsp;</p>
<ul>
<li>COVID-19 related documents&nbsp; | Statutory Documents&nbsp;| Non-Disclosure &amp; Copyright</li>
<li>Hiring | &nbsp;Performance Review | Employee Policies</li>
<li>Recruitment | HR Forms | HR Letters</li>
<li>Co-founders' agreement | Tenanncy Agreenment | NDA | Freelancer agreement&nbsp;</li>
</ul>
<p>Some fo the important documents which you'll find in the bundle is listed below&nbsp;</p>
<table border="1">
<tbody>
<tr>
<td>Legal Documents &amp; Templates&nbsp;</td>
<td>HR Documents and templates</td>
</tr>
<tr>
<td>1. NDA(Non-disclosure agreement)</td>
<td>- Employee Information form</td>
</tr>
<tr>
<td>2. New employee offer letter</td>
<td>- Leave request form</td>
</tr>
<tr>
<td>3. Conflict of interest</td>
<td>- Performance evaluation form</td>
</tr>
<tr>
<td>4. Confidentiality agreement</td>
<td>- Employee Incident report form</td>
</tr>
<tr>
<td>5. Employee appraisal form</td>
<td>- Return to Work form</td>
</tr>
<tr>
<td>6. Company loan agreement</td>
<td>- Covid-19 Self Screening form</td>
</tr>
<tr>
<td>7. Invention agreement</td>
<td>- Employee Reference Request&nbsp;</td>
</tr>
<tr>
<td>8. Contractor agreement</td>
<td>- Employee Complaint form</td>
</tr>
<tr>
<td>9. Advisor agreement</td>
<td>- Employee Nomination form</td>
</tr>
<tr>
<td>10. Important agreements like partnership deed, dealership agreement etc.</td>
<td>- Labour application form</td>
</tr>
<tr>
<td>+ 4000 other important documents &amp; templates&nbsp;</td>
<td>&nbsp;</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
<p><strong>How does it help?</strong></p>
<p>Legal documents are not something you can prepare without experience and We can't stress enough how important it is that the documents you use are compliant with the latest laws, guidelines and statutes.&nbsp; All documents provided by&nbsp;<span class="il">99papers</span>&nbsp;are updated every quarter and if there are any changes in the documents you are using, you'll receive a notification regarding the same through e-mail.&nbsp;</p>
<p>&nbsp;</p>
<p><strong>Cost - Rs. 1299, including taxes.</strong></p>
<p>&nbsp;</p>
<p>Visit our website with the link here -&nbsp;<a href="https://99papers.in/" target="_blank" rel="noopener" data-saferedirecturl="https://www.google.com/url?q=https://lsxqm3jn.r.us-east-2.awstrack.me/L0/https:%252F%252Flazyslate.com%252F/1/010f018d6d2afb58-826969b1-3b9a-49a8-9d6f-df14f5a42e00-000000/RYGvGPm39mwkJdcC41Eitoq4p1w%3D144&amp;source=gmail&amp;ust=1734980047291000&amp;usg=AOvVaw1aodjL2fRcdduad-ztNv66"><strong>Visit Website</strong></a>.</p>
<p>You can get further information and the link to payment of the bundle using the link here -&nbsp;<a href="https://docs.99papers.in/99Papers%20-%20Sample%20Documents.pdf" target="_blank" rel="noopener" data-saferedirecturl="https://www.google.com/url?q=https://lsxqm3jn.r.us-east-2.awstrack.me/L0/https:%252F%252Flazyslate.com%252F/1/010f018d6d2afb58-826969b1-3b9a-49a8-9d6f-df14f5a42e00-000000/RYGvGPm39mwkJdcC41Eitoq4p1w%3D144&amp;source=gmail&amp;ust=1734980047291000&amp;usg=AOvVaw1aodjL2fRcdduad-ztNv66"><strong>SAMPLE DOCUMENTS</strong></a>.</p>
<p>If you have any questions, feel free to reply to this mail or contact us at <a href="mailto:support@99papers.in">support@99papers.in</a> or +91 6379934788 with your query.&nbsp;</p>
<p>Regards,</p>
<p>Team&nbsp;<span class="il">99Papers, IN</span></p>
<div>&nbsp;</div>"""  # Alias if HTML not available
REFETCH_INTERVAL = 300  # Refetch interval in seconds (5 minutes)

def load_html_content():
    """Load HTML content from file or use alias text."""
    if os.path.exists(HTML_CONTENT_FILE):
        print(f"Loading HTML content from {HTML_CONTENT_FILE}...")
        with open(HTML_CONTENT_FILE, 'r', encoding='utf-8') as file:
            return file.read()
    print(f"{HTML_CONTENT_FILE} not found, using alias text.")
    return ALIAS_TEXT

def append_to_csv(log_file, data):
    """Helper function to append data to CSV, create the file if it doesn't exist."""
    df = pd.DataFrame([data])
    if not os.path.exists(log_file):
        print(f"Creating new log file: {log_file}")
        df.to_csv(log_file, mode='a', header=True, index=False)
    else:
        print(f"Appending to existing log file: {log_file}")
        df.to_csv(log_file, mode='a', header=False, index=False)

def get_daily_count(sender_email, date):
    """Retrieve how many emails the sender has sent today."""
    if not os.path.exists(DAILY_COUNT_LOG_FILE):
        print(f"No daily log found, returning count as 0 for {sender_email}.")
        return 0
    log_df = pd.read_csv(DAILY_COUNT_LOG_FILE)
    sender_logs = log_df[(log_df['sender_email'] == sender_email) & (log_df['date'] == date)]
    if not sender_logs.empty:
        print(f"{sender_email} has already sent {sender_logs.iloc[0]['mail_count']} emails today.")
        return sender_logs.iloc[0]['mail_count']
    return 0

def update_daily_count(sender_email, date, new_count):
    """Update the count of emails sent by the sender on a particular day."""
    if not os.path.exists(DAILY_COUNT_LOG_FILE):
        print(f"Creating new daily log for {sender_email}.")
        append_to_csv(DAILY_COUNT_LOG_FILE, {'date': date, 'sender_email': sender_email, 'mail_count': new_count})
    else:
        log_df = pd.read_csv(DAILY_COUNT_LOG_FILE)
        if not log_df[(log_df['sender_email'] == sender_email) & (log_df['date'] == date)].empty:
            log_df.loc[(log_df['sender_email'] == sender_email) & (log_df['date'] == date), 'mail_count'] = new_count
            log_df.to_csv(DAILY_COUNT_LOG_FILE, index=False)
            print(f"Updated daily log for {sender_email} with {new_count} emails.")
        else:
            print(f"Adding new daily log entry for {sender_email}.")
            append_to_csv(DAILY_COUNT_LOG_FILE, {'date': date, 'sender_email': sender_email, 'mail_count': new_count})

def check_email_sent(recipient_email, date):
    """Check if any email has already been sent to the recipient today by any sender."""
    if not os.path.exists(EMAIL_LOG_FILE):
        print(f"No email log found, no emails have been sent yet.")
        return False
    log_df = pd.read_csv(EMAIL_LOG_FILE)
    recipient_logs = log_df[(log_df['recipient_email'] == recipient_email) & (log_df['send_time'].str.startswith(date))]
    if not recipient_logs.empty:
        print(f"Email already sent to {recipient_email} on {date}. Skipping...")
        return True
    return False

def send_email(sender_email, sender_password, recipient_email, content_type='text'):
    """Send an email to a recipient."""
    try:
        print(f"Preparing to send email from {sender_email} to {recipient_email}...")

        # Create email
        msg = MIMEMultipart()
        msg['From'] = f"99papers Document Expert <{sender_email}>"
        msg['To'] = recipient_email
        msg['Subject'] = f"99Papers - find perfect documents for your business now - Reg"

        if content_type == 'html':
            body = load_html_content()
            msg.attach(MIMEText(body, 'html'))
        else:
            msg.attach(MIMEText(ALIAS_TEXT, 'plain'))

        # Connect to SMTP server and send the email
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(sender_email, sender_password)
        smtp_server.sendmail(sender_email, recipient_email, msg.as_string())
        smtp_server.quit()

        send_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"Email successfully sent from {sender_email} to {recipient_email} at {send_time}")

        # Log the sent email details
        append_to_csv(EMAIL_LOG_FILE, {
            'sender_email': sender_email,
            'recipient_email': recipient_email,
            'send_time': send_time
        })
        return True

    except Exception as e:
        print(f"Error while sending email from {sender_email} to {recipient_email}: {e}")
        return False

# Start sending emails in a loop
while True:
    # Refetch sender and recipient lists
    senders_df = pd.read_csv('Sender.csv')
    recipients_df = pd.read_csv('Mailer.csv')

    today_date = datetime.now().strftime('%Y-%m-%d')
    next_sender_index = 0  # Track the next sender
    last_send_times = [None] * len(senders_df)  # Track the last send time for each sender

    while True:
        if next_sender_index >= len(senders_df):
            print("All senders have been processed. Exiting this round...")
            break  # Exit if all senders have been processed

        sender = senders_df.iloc[next_sender_index]
        sender_email = sender['Email']
        sender_password = sender['Password']

        # Check how many emails this sender has sent today
        daily_count = get_daily_count(sender_email, today_date)
        if daily_count >= MAIL_LIMIT:
            print(f"{sender_email} has already reached the limit of {MAIL_LIMIT} emails today. Moving to the next sender.")
            next_sender_index += 1  # Move to the next sender
            continue

        # Loop through recipients and send emails
        for _, recipient in recipients_df.iterrows():
            recipient_email = recipient['Mail']

            # Check if the sender is ready to send another email based on the last send time
            current_time = time.time()
            if last_send_times[next_sender_index] is not None:
                elapsed_time = current_time - last_send_times[next_sender_index]
                if elapsed_time < TIME_GAP:
                    print(f"{sender_email} has sent an email within the TIME_GAP. Switching to the next sender...")
                    next_sender_index += 1  # Move to the next sender
                    break  # Exit the recipient loop to switch senders

            # Check if the email has already been sent to this recipient today by any sender
            if check_email_sent(recipient_email, today_date):
                continue  # Skip sending email to this recipient

            email_sent = send_email(sender_email, sender_password, recipient_email, 'html')

            if email_sent:
                daily_count += 1
                update_daily_count(sender_email, today_date, daily_count)
                last_send_times[next_sender_index] = current_time  # Update the last send time for this sender

                # If the sender has reached the limit for the day, stop
                if daily_count >= MAIL_LIMIT:
                    print(f"{sender_email} has reached the daily limit of {MAIL_LIMIT} emails. Moving to the next sender.")
                    next_sender_index += 1  # Move to the next sender
                    break

            else:
                print(f"Failed to send email to {recipient_email}. Moving to the next recipient.")

    # Wait for the refetch interval before the next round
    print(f"Waiting for {REFETCH_INTERVAL} seconds before refetching sender and recipient lists...")
    time.sleep(REFETCH_INTERVAL)

print("All emails processed.")
