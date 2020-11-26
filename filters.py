from telegram.ext import Filters
import re


# Message Handler filters
any_text_not_a_command = Filters.text & (~Filters.command)
help_cmd = Filters.command(False) & Filters.regex(r'help')

# Filter any command - required for Unknown command handler
any_command = Filters.command
