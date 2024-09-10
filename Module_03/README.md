## EX02 Wikipedia API

https://www.mediawiki.org/wiki/API:Main_page

https://www.mediawiki.org/w/api.php?action=help&modules=parse

https://github.com/daddyd/dewiki


## EX03 BeautitfulSoup

https://www.crummy.com/software/BeautifulSoup/bs4/doc/


## EX04 Virtual Environment

The issue is that when you run a Bash script, each command is executed in a subshell. When the script finishes, the virtual environment you activated gets deactivated because the subshell closes.

To keep the virtual environment active after the script finishes, you need to "source" the script instead of running it normally. Here's how to do that:

Instead of running your script as `bash my_script.sh`, use `source my_script.sh`

This will execute the script in the current shell context, keeping the virtual environment active.