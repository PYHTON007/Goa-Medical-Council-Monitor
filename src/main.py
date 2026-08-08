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

from summarizer import summarize_pdf

from telegram_bot import send_update

from logger import log

from state_manager import load_state, save_state

from config import (
    SEND_STATUS_IF_NO_CHANGE,
    SEND_PDF_ON_CHANGE,
    SEND_SUMMARY,
)


STARTING_CREDIT = 15.00


def build_usage_footer(
    input_tokens,
    output_tokens,
    total_tokens,
    request_cost,
    state,
):
    """Build the AI usage and estimated credit footer."""

    cumulative_input = state.get("ai_input_tokens", 0)
    cumulative_output = state.get("ai_output_tokens", 0)
    cumulative_total = state.get("ai_total_tokens", 0)
    cumulative_cost = state.get("ai_total_cost", 0.0)

    estimated_remaining = max(
        0.0,
        STARTING_CREDIT - cumulative_cost
    )

    return (
        "\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🤖 GPT-5.6 Luna\n\n"
        "📊 THIS REQUEST\n"
        f"• Input: {input_tokens:,} tokens\n"
        f"• Output: {output_tokens:,} tokens\n"
        f"• Total: {total_tokens:,} tokens\n"
        f"• Estimated cost: ${request_cost:.6f}\n\n"
        "📈 CUMULATIVE\n"
        f"• Input: {cumulative_input:,} tokens\n"
        f"• Output: {cumulative_output:,} tokens\n"
        f"• Total: {cumulative_total:,} tokens\n"
        f"• Estimated cost: ${cumulative_cost:.6f}\n\n"
        "💰 ESTIMATED API CREDIT\n"
        f"• Starting credit: ${STARTING_CREDIT:.2f}\n"
        f"• Estimated remaining: ${estimated_remaining:.6f}\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )


def build_no_ai_footer(state):
    """Build usage footer for a check where Luna was not called."""

    cumulative_input = state.get("ai_input_tokens", 0)
    cumulative_output = state.get("ai_output_tokens", 0)
    cumulative_total = state.get("ai_total_tokens", 0)
    cumulative_cost = state.get("ai_total_cost", 0.0)

    estimated_remaining = max(
        0.0,
        STARTING_CREDIT - cumulative_cost
    )

    return (
        "\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🤖 GPT-5.6 Luna\n"
        "📊 THIS CHECK\n"
        "• AI call: None\n"
        "• Tokens used: 0\n\n"
        "📈 CUMULATIVE\n"
        f"• Input: {cumulative_input:,} tokens\n"
        f"• Output: {cumulative_output:,} tokens\n"
        f"• Total: {cumulative_total:,} tokens\n"
        f"• Estimated cost: ${cumulative_cost:.6f}\n\n"
        "💰 ESTIMATED API CREDIT\n"
        f"• Starting credit: ${STARTING_CREDIT:.2f}\n"
        f"• Estimated remaining: ${estimated_remaining:.6f}\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )


def main():

    log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    log("Goa Medical Council Monitor v1.2")
    log("Checking Goa Medical Council website...")

    try:

        html = download_homepage()

        pdf_link = find_pdf_link(html)

        if pdf_link is None:

            log(
                "Website reachable, but FMG CRMI Internship PDF "
                "was not found."
            )

            state = load_state()

            message = website_down_message()
            message += build_no_ai_footer(state)

            send_update(message)

            return

        changed, current_pdf = download_pdf(pdf_link)

        state = load_state()

        if changed:

            log("Change detected.")

            message = change_message(pdf_link)

            summary = None

            if SEND_SUMMARY:

                log("Generating AI summary...")

                try:

                    result = summarize_pdf(current_pdf)

                    summary = result["summary"]

                    input_tokens = result["input_tokens"]
                    output_tokens = result["output_tokens"]
                    total_tokens = result["total_tokens"]
                    request_cost = result["cost"]

                    # Update cumulative usage
                    state["ai_input_tokens"] = (
                        state.get("ai_input_tokens", 0)
                        + input_tokens
                    )

                    state["ai_output_tokens"] = (
                        state.get("ai_output_tokens", 0)
                        + output_tokens
                    )

                    state["ai_total_tokens"] = (
                        state.get("ai_total_tokens", 0)
                        + total_tokens
                    )

                    state["ai_total_cost"] = (
                        state.get("ai_total_cost", 0.0)
                        + request_cost
                    )

                    save_state(state)

                    log("AI summary generated successfully.")

                    log(
                        f"AI usage: "
                        f"{input_tokens} input / "
                        f"{output_tokens} output / "
                        f"{total_tokens} total tokens"
                    )

                    log(
                        f"Estimated request cost: "
                        f"${request_cost:.6f}"
                    )

                except Exception as e:

                    log(f"AI summary failed: {e}")

                    summary = (
                        "⚠️ AI summary could not be generated. "
                        "Please review the attached PDF."
                    )

                    input_tokens = 0
                    output_tokens = 0
                    total_tokens = 0
                    request_cost = 0.0

            else:

                input_tokens = 0
                output_tokens = 0
                total_tokens = 0
                request_cost = 0.0

            if summary:

                message += (
                    "\n\n🤖 AI RECAP\n\n"
                    + summary
                )

            # Add usage information
            if SEND_SUMMARY:

                message += build_usage_footer(
                    input_tokens,
                    output_tokens,
                    total_tokens,
                    request_cost,
                    state,
                )

            if SEND_PDF_ON_CHANGE:

                send_update(message, current_pdf)

            else:

                send_update(message)

        else:

            log("No changes detected.")

            if SEND_STATUS_IF_NO_CHANGE:

                message = no_change_message(pdf_link)

                message += build_no_ai_footer(state)

                send_update(message)

        log("Monitor finished successfully.")
        log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

    except Exception as e:

        log(f"ERROR: {e}")

        state = load_state()

        message = website_down_message()
        message += build_no_ai_footer(state)

        send_update(message)


if __name__ == "__main__":
    main()