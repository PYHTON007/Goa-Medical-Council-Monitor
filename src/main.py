from message_builder import (
    no_change_message,
    change_message,
    website_down_message,
)

from scraper import (
    download_homepage,
    find_pdf_link,
    download_pdf,
)

from telegram_bot import send_update

from logger import log

from config import (
    SEND_STATUS_IF_NO_CHANGE,
    SEND_PDF_ON_CHANGE,
)


def main():

    log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    log("Goa Medical Council Monitor v1.0")
    log("Checking Goa Medical Council website...")

    try:

        html = download_homepage()

        pdf_link = find_pdf_link(html)

        if pdf_link is None:

            log("Website reachable, but FMG CRMI Internship PDF was not found.")

            send_update(website_down_message())

            return

        changed, current_pdf = download_pdf(pdf_link)

        if changed:

            log("Change detected.")

            message = change_message(pdf_link)

            if SEND_PDF_ON_CHANGE:
                send_update(message, current_pdf)
            else:
                send_update(message)

        else:

            log("No changes detected.")

            if SEND_STATUS_IF_NO_CHANGE:
                send_update(no_change_message(pdf_link))

        log("Monitor finished successfully.")
        log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    except Exception as e:

        log(f"ERROR: {e}")

        send_update(website_down_message())


if __name__ == "__main__":
    main()