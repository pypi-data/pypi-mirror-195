# -*- coding: utf-8 -*-
import pyperclip


def slack2notion(mode=None) -> None:
    slack_text = pyperclip.paste()
    slack_lines = slack_text.split('\n')


    if mode == 'bullet':
        notion_text = '\n'.join(['- ' + l for l in slack_lines])
    elif mode == 'number':
        notion_text = '\n'.join(['1. ' + l for l in slack_lines])
    else:
        notion_text = '\n\n'.join(slack_lines)

    pyperclip.copy(notion_text)


if __name__ == "__main__":
    pass