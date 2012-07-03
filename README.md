drive-letter-watcher
====================

Watches (polls every 5 seconds) for Windows drive letter connection or disconnection events and allows scheduling of tasks, to run accordingly.

Fill in the appropriate drive letter in the config with the command you want the script to run for it (see also http://docs.python.org/library/os.html#os.startfile).

Requires pywin32 (http://sourceforge.net/projects/pywin32/files/)