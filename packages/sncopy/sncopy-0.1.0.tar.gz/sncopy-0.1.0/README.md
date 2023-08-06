# sncopy; Copy-Paste Tool from Slack to Notion

It's very stressfull to copy some contents on Slack to Notion because their html are not compatible.  
So, when I copy the contents include `Bulleted list` or `Numbered list`, I have to fix them manually.  

## What is the difference

These are the sample outputs of copy from Slack and Notion.
In short, we will save text as plain text not markdown on Slack.

**Case 1 : normal lines**

```
[Original]
Apple
Google
Microsoft

[on Slack]
'Apple\nGoogle\nMicrosoft'

[on Notion]
'Apple\n\nGoogle\n\nMicrosoft'
```

**Case 2 : bulleted lines**

```
[Original]
- Apple
- Google
  - Microsoft

[on Slack]
'Apple\nGoogle\nMicrosoft'

[on Notion]
'- Apple\n- Google\n    - Microsoft'
```

**Case 3 : numbered lines**

```
[Original]
1. Apple
2. Google
  a. Microsoft

[on Slack]
'Apple\nGoogle\nMicrosoft'

[on Notion]
'1. Apple\n1. Google\n    1. Microsoft'
```

Because Slack will return plain one, we cannot keep the structure of nested lines...  


## Installation

```
pip install sncopy
```


## Usage

Basically, you only have to call `sncopy` on your terminal after copying your contents on Slack.  
This command will automatically convert them to Notion's format.  

If you want to convert to bulleted lines, please call `sncopy` command with `--mode` option.  

```
sncopy --mode bullet
```

for numbered lines,  

```
sncopy --mode numbered
```