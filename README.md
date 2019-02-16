**Dreamdir** – the Unix dream journal format

Overview
========

*Dreamdir* is a format for storing a dream journal inspired by the popular
[Maildir](https://en.wikipedia.org/wiki/Maildir) mailbox format and the
[RFC 2822](https://tools.ietf.org/html/rfc2822) email format itself.

## Philosophy

Dreamdir follows the [Unix philosophy](https://en.wikipedia.org/wiki/Unix_philosophy),
as follows:

* All dreams are stored in plain text formatted in a consistent way.
  The format is human-readable and is normally read and written directly.
* Dreamdir is first and foremost a format, not an application.
  Simple code designed to do one thing well is provided
  to make working with the format easier.
* In addition to the provided code,
  standard Unix text-processing tools and simple scripts
  can easily manipulate dreams stored in a Dreamdir.

## Important factoids

Data format:

* Each dream is stored in its own plain text file.
* Each dream file begins with a list of data fields (called *headers*),
  which can store things like the date, the names of people who appeared in the dream, and tags.
* The remainder of the dream file is the text of your entry.

Application:

* The `dr` script offers powerful and intuitive search functionality
  and several other useful tools to create new dreams, combine tags, and so on.
  It easily integrates with other Unix tools.
* Example user scripts are provided for tasks like graphing day-to-day recall
  and generating indexes. A small Python library is also available.
* Free and open source:
  the Dreamdir format itself and this documentation are public domain,
  and all code is provided under the MIT license (see the LICENSE file for details).


Dreamdir format
===============

Specification -- Requirements
-----------------------------

Dreamdir scripts are permitted to assume that the rules specified in this
section are followed, so you should definitely follow them. Conformance to the
most basic rules can be checked with the `dr check-validity` command.

The easiest way to learn the format is to look at an example dream file (people’s names are censored here but are written out in full in the actual file format):

    Id:	00952
    Date:	2015-11-19
    Time:	6:02
    People:	M., Md., T.
    Places:	Wal-Mart
    Tags:	store, radio, cottage, enchantment, police

    I'm in some kind of large store which sells food, perhaps a supermarket or
    Wal-Mart or something of that nature.  I have found two small individual
    packages of applesauce and eaten them, and I now am wondering if that's
    okay and how I will pay for them.  I'm with M here.  Near the back of the
    store, there's a small table with a store walkie-talkie on it.  I pick this
    up, and though I'm not sure exactly how this happened, I soon get into a
    heated argument with a store manager over the radio.  It starts off being
    about the applesauce in some fashion, but it soon turns into a tirade about
    consumerism and the advertising in their store.  Eventually the manager
    gets so pissed at what I'm saying (though I wasn't *trying* to upset him, I
    also wasn't trying to be careful) that he tells me he's going to have the
    police come and arrest me.  I don't question that he has the authority to
    do this, and so M and I decide that we should leave quickly before they
    arrive.  We head out of the store; as a final "screw you" I grab a Snickers
    bar that's sitting on a table as I leave.

    [remainder of dream clipped]

At the top you see the *headers*.
Each header is separated from its *values* by a colon followed by a hard tab.
(The requirement of a tab makes commands like `grep` easier to use,
    since a colon will not be followed by a tab in running text.)
For headers that can take multiple values,
    such as People, Places, and Tags,
    individual values are separated by a comma and a space.

Two headers are **required** to form a valid dream file:
    the *Id* number and the *Date*.
All other headers are optional.
There are no rules about what constitutes a valid header name
    (except that of course it cannot contain a colon followed by a hard tab),
    and it is fine for some dreams
    to not have a particular optional header at all.
The headers can come in any order.
A blank line follows the headers.

The two required headers are fussier, as follows:

* **Id**: Dreamdir uses fixed-width five-digit ID numbers,
  beginning at `00001` and increasing for each dream up to `99999`.
  (If you manage to record 100,000 dreams, updates to the program and a beer are on me!)
* **Date**: Dreamdir scripts expect [ISO 8601](https://xkcd.com/1179/)-formatted
  dates (YYYY-MM-DD).

Beneath the headers, following a blank line, comes the text of the dream.
As long as you don’t begin any later line with a header
    (i.e., a line containing a colon immediately followed by a hard tab),
    you can do anything you like here,
    though you may wish to look at the “Formatting guidelines” section, below.


Specification -- Suggestions
----------------------------

* **Emphasis**: Use `*single stars*` or `_underlines_` around the area to be emphasized.
* **Commentary**: Place notes that are not actually part of the dream in `[square brackets]`. The commentary may continue over multiple lines.
* **Verbatim quoting**: Place text that is directly quoted from some earlier form of notes (such as a notebook you scribbled in in bed) in `` `backticks` ``.
* **Lucid sections**: If you lucid dream, you can place sections where you knew you were dreaming in `{curly braces}`. I also use the header `Lucid:	1` to make it easier to find these dreams.

Emphasis and verbatim quoting
    are recognized by the syntax highlighting functionality.
Lucid sections and commentary are recognized by the word count scripts
    (word counts can be split into “normal,” “lucid,” and “notes”).

I use one physical line per paragraph
    and [double-space between sentences](http://stevelosh.com/blog/2012/10/why-i-two-space/),
    but I don’t see those conventions ever being expected by any code.


Suggested headers
-----------------

As mentioned earlier,
    you can use any headers you like as long as you include the ID number and the date.
    As a starting point, here are the ones I currently use:

* **People**: Comma-separated list of waking-life people who appeared in the dream.
* **Places**: Ditto for places with proper names and general geographic regions.
* **Tags**: List of motifs, categories, and other elements that are useful to track across multiple dreams but don’t fit into other headers.
* **Title**: A title...
* **Time**: If I had a clock handy and remembered to write it down, the time at which I woke up from the dream.
* **Lucid**: Included and with a value of 1 if the dream was lucid at any point.


File names and locations
------------------------

All dreams are kept in the root of the dreamdir.
A dream’s filename is its ID number with a `.dre` extension, e.g., `00592.dre`.

    -rw-------  1 soren soren   623 Dec 14  2014 00001.dre
    -rw-rw-r--  1 soren soren   210 Feb 14 19:00 00002.dre
    [...]
    -rw-------  1 soren soren  3075 Apr 28 21:25 01227.dre
    -rw-------  1 soren soren  1600 Apr 27 13:21 01228.dre
    -rw-rw-r--  1 soren soren     0 Apr 29 15:56 .dreamdir

Note the `.dreamdir` file, which marks this directory as a Dreamdir.
The content is currently unimportant,
    but scripts may check for this file to ensure they’re working in a dreamdir.

`dr` uses the current directory as the dreamdir
    if it contains that `.dreamdir` file.
Otherwise, it checks the environment variable `DREAMDIR`
    for a path and uses that location if it’s set to a valid dreamdir.
If neither of these locations are valid dreamdirs,
    `dr` will exit without doing anything.


Installation / creating a Dreamdir
==================================

Begin by copying the `dr` script to somewhere on your system path.

If you want to use the `word-count` functionality,
    which differs from the standard `wc` in that it ignores headers
    and can count marked lucid and notes sections separately,
    change into the `drwc` directory and run `make` (this requires `gcc`),
    then install the compiled `drwc` binary to your system path as well.

If you want to use the ctags generation functionality,
    make sure you have `python3` available on your path.

Finally, create a directory for your dreamdir and use `touch .dreamdir`
    to mark the directory as a dreamdir.
You should now be able to use `dr new` to create your first dream file.

You may also wish to set the environment variable `DREAMDIR`
    to the path to your dreamdir;
    this way you can run `dr` from anywhere in your filesystem.

I keep my dreamdir under `git` control
    to keep track of any revisions I make to headers and dreams
    and as an extra backup against scripting and [PEBKAC][] errors.
    You may wish to do likewise.

[PEBKAC]: https://en.wikipedia.org/wiki/User_error#Acronyms_and_other_names

Dependencies
------------

Utilities needed by dr that are not part of POSIX:

* `bash` 4.0+
* `python3` (needed for `regenerate-tags`)

dr tries to stick to POSIX standards,
    but we have limited ability to test that we have done so
    across multiple systems.
If something in `dr` doesn’t work right in your version of a POSIX utility,
    or if a system in common use doesn’t comply with the relevant aspects
    of a POSIX standard `dr` relies upon,
    please submit a bug report.

(dr also uses `seq`, `tac`, and `shuf` when available,
    but includes slower, more memory-intensive fallback methods
    for when GNU coreutils aren’t present,
    so they are not necessary.)


Dreamdir scripts
================

A number of example scripts, largely written in Python, are provided in the
`scripts/` directory of this repository; you may wish to use some of these as
models for building your own scripts. Of particular note is `ddirparse.py`,
which is a general library for use in developing Dreamdir scripts.

I don’t make any guarantees about the general applicability or correctness of
these scripts. Some have not been tested recently. *You must read through the
code of any script that looks interesting before using it*; you may find there
are still file paths, system-specific constants, or other surprises lurking
somewhere.


Vim plugin
==========

For those who use vim, syntax highlighting and ftplugin files are located in
the `vim/` directory; you can install these to your `~/.vim` directory directly
or use your favorite plugin manager.

You may want to remove the `setlocal cpoptions+=J` (`:help cpo-J`) line from
`vim/ftplugin/dream.vim` if you don’t want to double-space between sentences
(see the “Formatting guidelines” section above).

Ctags functionality is included in dreamdir. The tags file contains tags for
all dream ID numbers and all header values. You can do a number of handy things
with this in vim. Among others:

* With a dream open, jump to a different dream N with `:ta N`, e.g., `:ta 900`.
* With the cursor on a dream number (*see #900*), press `Control-]` to open
  that dream.
* With a header value highlighted in visual mode, or with the cursor on top of
  a single-word header value, press `g]` to show all matching tags. This will
  show all the dreams that use that header value, along with the whole header
  line and the Title header of the matching dream (if available).
* Search for header values containing *foo* with `:tjump /foo`. Along with
  being a handy way to do a quick search without having to leave your editor
  and run `dr` again, this is an easy way to answer questions about what tags
  you’ve previously used when you’re thinking of tags for the dream you’re
  currently writing up.

Tags are stored in the file `.dreams.ctags` in your dreamdir folder. They need
to be initially created as well as updated periodically by running `dr
regenerate-tags`; any changes to headers or new dreams will not be known to Vim
until the tags file is updated.


The `dr` script
===============

The `dr` script provides convenient tools to manage your dreamdir. The script
assumes the current directory is your dreamdir, so it may be run like this:

    $ cd ~/dreams
    $ dr new

Alternatively, `dr` recognizes the environment variable `DREAMDIR` as the path
to your dreamdir. If this variable is defined and you are not currently in a
dreamdir when you run `dr`, that directory will be used instead.

Detailed help on all the functions and options you have can be obtained at the
command line. Type `dr help` for the basics, and it will refer you to other help pages
(e.g., `dr help search`) where appropriate.

Note that all commands can be abbreviated by their initials; `find` is `f`, for
example, and `dump-headers` is `dh`. Keywords in search expressions can be
abbreviated similarly, so to find dreams tagged with `Maud` in the `People`
field, we can use `dr f t People Maud` as well as `dr find tagged People Maud`.
The long names are normally used throughout the documentation for clarity, and
they are easier to remember when you’re getting started, but once you know what
you’re doing you can save quite a few keystrokes this way.


Support & Development
=====================

Please post bugs on the Github issue tracker; if you prefer you can email me at
`contact@sorenbjornstad.com`. If you have a problem with `dr`, please mention
your operating system and version of bash.

Improvements and pull requests are welcome as long as you release your code
under the MIT license and they are consistent with the project’s philosophy.
Please make sure that `tests/pre-commit-hook.sh` exits successfully before
submitting any modifications to `dr`; this requires
[shellcheck](http://www.shellcheck.net/),
[BATS](https://github.com/sstephenson/bats), and GCC. If you have modified the
behavior of `dr`, you may need to change the tests in `tests/test_dr`; they are
pretty easy to figure out. If you don’t want to install `shellcheck` (it
requires Haskell and takes some time to install), you can paste the code on the
shellcheck website and then run `tests/test_dr` and `cd scripts && make clean
&& make` manually to finish the pre-commit tests.
