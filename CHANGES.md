Changes in 2.0.0
----------------

This release of `dr` breaks interface backwards compatibility
    and removes several low-value features
    that were not worth maintaining.
The format of dream files has not changed.
If you have any scripts that call the `dr` command,
    you should review this list for breaking changes.


### New features

* New `-f` option to the `tagged` search to match the entire header line with
  an ERE rather than using an hregex. This is intended for fields like “Title”
  which shouldn’t be treated as multiple comma-separated values.
* New `date` search, which works like `dr find date lt 2018-01-01` to find
  dreams from before January 1, 2018.
* The template for `dr new` has gotten smaller but can now be customized with a
  `.dream_template` file. Review `dr help new` for details.


### Removed features

* `stats` has been removed due to being buggy and very specific to me.
  You can easily write external scripts to produce the statistics you want.
* `xwinnow` has been removed due to lack of convincing use cases. It can be
  replaced with a combination of OR and AND conditions.
* `validate` is removed as a synonym of `check-validity` (this was deprecated
  in 1.0.4).
* The Python `word-count` implementation is no longer supported. The C
  implementation must be built and installed to the system path to get word
  counts.


## Changed behaviors

* The machine-readable format of `drwc` now separates its fields with tabs
  rather than spaces, to match the behavior of the standard `wc` Unix command.
  section.


### Bugfixes

* `1 matches` is now properly singular in the results of a `find` search.
* The `tagged` search no longer matches the filename as a tag value if the
  value specified is numeric (e.g., `tagged Tags 500` would match dream 500
  even if dream 500 didn’t have a tag value of 500).
* `get-header` now allows an empty search-expression.
* Several fixes for `act` (some arguments were not being passed forward;
  terminal could become broken on launching an interactive editor; all dreams
  were acted on without warning if no input was received).
* `winnow` now gives a useful error if something that is not a dream filename
  is piped into it.


### Dependency changes

New dependencies:

* `python3` is now required, but solely for the `regenerate-tags` command,
  so it could reasonably be omitted if you don’t need ctags files.
  (Python 2 is no longer required or supported.)
* `awk` is now used fairly extensively. Any POSIX-compliant `awk` should
  work.
* `drwc` (included in this repository) must now be installed to the system
  path to use the `word-count` function.

Removed dependencies:

* `python2` is no longer required. All Python snippets have either been
  converted to `bash` or `awk` or upgraded to Python 3.
* `ed` is no longer required due to an increasing number of distros
  not supplying it in the base package.
* `seq`, `shuf`, and `tac`, which are not POSIX standards, are no longer
  required. They will be used if available, but `dr` now includes fallback
  versions.
* The `scripts` folder is no longer required in a dreamdir,
  and `dr` does not need to access
  any external files in the dreamdir besides the actual data.


### Miscellaneous

* Significant performance improvements to searching, syntax highlighting, and
  other operations.
* Code cleanup, test coverage improvements, and fixing of shellcheck errors.
* The `scripts` directory has not been retested or reviewed, and no part of
  `dr` itself depends on these anymore. Base your work on example scripts at
  your own risk.


Changes in 1.0.5
----------------

Bugfixes:

* Work around vim's system() getting messed up by a nonstandard umask: just
  change the permissions with chmod after creation rather than using umask.

New features:

* You can place, e.g., 'dr act dump-headers' at the end of a 'winnow' pipeline
  to run dump-headers on the results, rather than having to use shell command
  substitution like 'dr dump-headers $(dr find ...)'.
* Vim tags support, and a generation script and 'regenerate-tags' action to go
  with it. See the Vim section of the README for details.


Changes in 1.0.4
----------------

This release mainly consists of internal cleanup and fixes introduced as a
result of static analysis with 'shellcheck' and an extended test suite, but a
few user-facing changes have been made as well.

Bugfixes:

* Fix 'random' not shifting away its arguments and preventing any subsequent
  search expressions from working.
* Don't break when additional search expressions are placed after an
  expression with an optional argument that is not provided (e.g., 'dr find
  random tagged Places home').
* 'validate' has been changed to 'check-validity' to resolve an abbreviation
  conflict with 'version'. 'validate' is retained as a deprecated alias of
  'check-validity'; 'v' now works only for 'version'.

New features:

* "headerdex" script to create an index from the headers of all dreams.
* Numerical ranges can now be used as search expressions (1-5, 1-, and -5 are
  all valid ranges, with the open end being replaced with the first or last
  dream as appropriate).
* 'cat' and 'dump-headers' will now color their output in a manner similar to
  the vim syntax highlighting file, if output is to a terminal. Note that this
  may cause a noticeable slowdown if printing a very large amount of output to a
  terminal.
* 'stats' now uses the improved Dreamdir word counts rather than the system 'wc'
  command. This means your word counts may drop noticeably because your headers
  are no longer being counted as part of your dream text.

Under-the-hood improvements:

* Add use of 'shellcheck' to the pre-commit hook script, and add notes about
  running these tests before contributing any code.
* Too many others to list -- please see the commit history for details.


Changes in 1.0.3
----------------

This release improves and normalizes a number of search functions. Despite all
the changes, I think the new syntax in this version is entirely
backwards-compatible with 1.0.2.

Bugfixes:

* Fix limit option to search expressions not working at all.
* Don't display '1 dreams' anywhere.

New features:

* Improve 'titleadd.sh' script, rename to 'headeradd.sh' to reflect widening
  function.
* Add empty search expressions and search expression 'all' to match all dreams.
* Adjustments to online help formatting and content.
* Greatly improve runtime of header-replace, and make it take any search
  expression rather than just a list of filenames to apply the changes over.
* Change separator used for 'sed' in header-replace so that you can use pipes in
  your search regex.
* list-headers and header-values now accept search expressions to limit their
  application to a subset of dreams.

Under-the-hood improvements:

* Change a bunch of variables used in functions to local ones.


Changes in 1.0.2
----------------

This is primarily a bugfix release.

Bugfixes:

* Add an ftdetect file so the vim plugin actually loads on .dre files out of
  the box.
* Remove dependency on a script on my local machine that wasn't included in the
  distribution.
* The formatting of 'dr find' is no longer messed up if dreams with ID numbers
  greater than 9999 are included in the output.
* Search expression options -vrsl are now applied in a consistent and documented
  order.
* Dream files are now pulled with the glob '[0-9][0-9][0-9][0-9][0-9].dre'
  rather than '*.dre', so other .dre files in the directory that are not dreams
  (for instance, temporary files that you wanted syntax highlighting to work on)
  will not confuse the search functions.
* Fix tests several times, and add a pre-commit hook that can be set to run
  tests before committing.
* Fix RegeneratePlots.sh getting very confused when the scripts/ directory in a
  dreamdir is a symlink.

New features:

* Add a -f option for 'dr cat' that folds lines at 80 characters, trying to do
  so at word boundaries (using 'fold -s').
* Print word counts for each individual dream, not just the total (and add an
  option that prints only the total).


Changes in 1.0.1
----------------

Bugfixes:

* Fix a bug where '.' was not correctly handled in search regexes.
* Add a blank line at the end of the headers when creating a new dream; not
  doing so was an accidental regression.
* Fix a problem where options set by the vim plugin only applied to the first
  buffer if multiple files were loaded.
* Display the average words/day, not the average words/dream, as the "average"
  in the statistics table.

New features:

* Add a new script to help with adding titles to dreams that don't have them.
* Implement word count feature in C, and add a front-end in `dr`.
* Write some tests for the `dr` script; more to come.

# vim:tw=80:
