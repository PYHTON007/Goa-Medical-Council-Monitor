from datetime import datetime


def current_datetime():
    return datetime.now().strftime("%d %b %Y • %I:%M %p")


FOOTER = (
    "\n━━━━━━━━━━━━━━━━━━━━━━\n"
    "<b>🤖 Goa Medical Council Monitor</b>\n"
    "<i>Version 1.0 • Developed by IJ</i>"
)


def no_change_message(pdf_link):

    return f"""
🟩🟩🟩🟩🟩🟩🟩

<b>🏥 GOA MEDICAL COUNCIL</b>

<b>📋 FMG CRMI MONITOR</b>

🟩 <b>DAILY STATUS</b>

🟩🟩🟩🟩🟩🟩🟩

📅 <b>Checked</b>

{current_datetime()}

━━━━━━━━━━━━━━━━━━━━━━

✅ <b>No changes detected.</b>

📄 <b>FMG CRMI Internship PDF</b>

The monitored PDF remains unchanged.

🔗 <b>Current PDF</b>

{pdf_link}
{FOOTER}
"""


def change_message(pdf_link):

    return f"""
🟥🟥🟥🟥🟥🟥🟥

<b>🏥 GOA MEDICAL COUNCIL</b>

<b>📋 FMG CRMI MONITOR</b>

🟥 <b>CHANGE DETECTED</b>

🟥🟥🟥🟥🟥🟥🟥

📅 <b>Detected</b>

{current_datetime()}

━━━━━━━━━━━━━━━━━━━━━━

🚨 <b>A new version of the FMG CRMI Internship PDF has been detected.</b>

📎 The latest PDF is attached below.

📝 <b>Summary</b>

• New PDF detected.
• Previous version archived.
• Latest version downloaded.

🔗 <b>Current PDF</b>

{pdf_link}
{FOOTER}
"""


def website_down_message():

    return f"""
🟨🟨🟨🟨🟨🟨🟨

<b>🏥 GOA MEDICAL COUNCIL</b>

<b>📋 FMG CRMI MONITOR</b>

🟨 <b>WEBSITE UNAVAILABLE</b>

🟨🟨🟨🟨🟨🟨🟨

📅 <b>Checked</b>

{current_datetime()}

━━━━━━━━━━━━━━━━━━━━━━

⚠️ The monitor could not reach the Goa Medical Council website.

Possible reasons:

• Website temporarily unavailable
• Internet connection unavailable
• Server timeout

The monitor will automatically try again during the next scheduled check.
{FOOTER}
"""