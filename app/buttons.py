from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def button_menu():
	"""Inline Buttons"""
	btn = [[
		InlineKeyboardButton("help", callback_data='help'),
		InlineKeyboardButton("search", callback_data='search'),
		InlineKeyboardButton("cancel", callback_data='cancel')
	]]
	return InlineKeyboardMarkup(btn)
