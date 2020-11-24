from telegram.ext import Filters


# Message Handler filters
any_text_not_a_command = Filters.text & (~Filters.command)


# Filter any command - required for Unknown command handler
any_command = Filters.command
