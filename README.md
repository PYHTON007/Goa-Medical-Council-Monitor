# 🏥 Goa Medical Council Monitor

An automated Python monitor for the Goa Medical Council website.

The monitor checks the **FMG CRMI Internship** PDF and notifies you via Telegram whenever changes are detected.

## Features

- Website monitoring
- Automatic PDF download
- SHA-256 change detection
- Timestamped archive of previous PDFs
- Telegram notifications
- Automatic PDF attachment
- AI-powered PDF recaps using GPT-5.6 Luna
- AI token usage tracking
- Estimated AI API cost tracking
- Cumulative AI usage tracking
- Estimated remaining API credit tracking
- Scheduled GitHub Actions monitoring
- Manual workflow execution
- Logging
- Configurable settings

## Technologies

- Python
- Requests
- BeautifulSoup
- pypdf
- OpenAI API
- Telegram Bot API
- GitHub Actions

## AI Recaps

When a new FMG/CRMI Internship PDF is detected, **GPT-5.6 Luna** analyzes the document and generates a concise Telegram-ready recap.

The recap focuses on:

- What changed
- Important dates
- Key requirements
- Internship and selection details
- Important instructions for FMGs

The AI is **only called when the monitored PDF changes**, preventing unnecessary API usage during routine checks.

## AI Usage Tracking

Each Telegram update includes information about AI usage, including:

- Input tokens
- Output tokens
- Total tokens
- Estimated cost for the request
- Cumulative token usage
- Cumulative estimated API cost
- Estimated remaining API credit

The estimated remaining credit is calculated from the configured starting API credit and the monitor's recorded API usage.

## Monitoring Schedule

The monitor runs automatically through GitHub Actions:

- 06:00 IST
- 12:00 IST
- 18:00 IST
- 00:00 IST

A manual workflow trigger is also available through GitHub Actions.

## Project Structure

    Goa-Medical-Council-Monitor/
    |
    +-- .github/
    |   +-- workflows/
    |       +-- monitor.yml
    |
    +-- src/
    |   +-- config.py
    |   +-- logger.py
    |   +-- main.py
    |   +-- message_builder.py
    |   +-- pdf_utils.py
    |   +-- scraper.py
    |   +-- state_manager.py
    |   +-- summarizer.py
    |   +-- telegram_bot.py
    |
    +-- data/
    |   +-- pdfs/
    |
    +-- logs/
    |
    +-- state/
    |
    +-- requirements.txt
    +-- .env
    +-- README.md

## Security

API keys and Telegram credentials are stored as environment variables and GitHub Secrets.

The `.env` file is excluded from Git using `.gitignore` and should **never be committed** to the repository.

## Version

**Current Release: v1.2**

### Version History

- **v1.2** — Added GPT-5.6 Luna AI recaps, token usage tracking, estimated API cost tracking, and Telegram usage reporting.
- **v1.1** — Added scheduled GitHub Actions monitoring and automated state management.
- **v1.0** — Initial Goa Medical Council FMG/CRMI PDF monitoring system.

---

Developed by **IJ**