**Dreamdir** – the Unix dream journal format

Introduction
============

*Dreamdir* is a format for storing a dream journal inspired by the popular [Maildir](https://en.wikipedia.org/wiki/Maildir) way of storing mailboxes and the [RFC 2822](https://tools.ietf.org/html/rfc2822) email format itself.

Dreamdir follows the [Unix philosophy](https://en.wikipedia.org/wiki/Unix_philosophy):

* All dreams are stored in plain text formatted in a consistent way. The format is human-readable and is normally read and written directly.
* Dreamdir is first and foremost a format, not an application. Simple code designed to do one thing well is provided to make working with the format easier.
* In addition to the provided code, standard Unix text-processing tools and simple scripts can easily manipulate dreams stored in a Dreamdir.

Features:

* Each dream is stored in its own plain text file.
* Each dream file begins with a list of data fields (called *headers*), which can store things like the date, the names of people who appeared in the dream, and tags.
* The remainder of the dream file is simply the text of your entry, and you can do anything you like with it.
* The provided shell script `dr` offers easy commands to create new dreams, view and edit existing dreams, do arbitrarily complex searches, combine tags, and more. (See the “Searching Walkthrough” section for some examples.)
* Example user scripts are provided for tasks like graphing day-to-day recall and generating indexes. A small Python library is also available.
* Free and open source: the Dreamdir format itself and this documentation are public domain, and all code is provided under the MIT license (see the LICENSE file for details).

The `dr` shell script is still under fairly active development, so if you wish to use it you should be aware that the syntax may change when you update. Also, while I’m comfortable enough with the stability of `dr` to do development with my own personal dreamdir, please back up your dreams regularly while using it.

The Dreamdir format itself is so simple it is essentially fixed, and changing it to something else would be very easy, so there will be no portability problems if you begin using it right now.


Dreamdir format
===============

Formatting rules
----------------

Dreamdir scripts are permitted to assume that the rules specified in this section are followed, so you should definitely follow them. Conformance to some of the rules can be checked with the `dr validate` command.

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

At the top you see the *headers*. Each header is separated from its *values* by a colon followed by a hard tab. (The requirement of a tab makes commands like `grep` easier to use, since a colon will not be followed by a tab in running text.) For headers that can take multiple values, such as People, Places, and Tags, individual values are separated by a comma and a space.

Two headers are **required** to form a valid dream file: the *Id* number and the *Date*. All other headers are optional. There are no rules about what constitutes a valid header name, and it is fine for some dreams to not have a particular optional header at all. The headers can come in any order. A blank line follows the headers.

The two required headers are somewhat fussier, as follows:

* **Id**: Dreamdir uses fixed-width five-digit ID numbers, beginning at `00001` and increasing for each dream up to `99999`. (If you manage to record 100,000 dreams, updates to the program and a beer are on me!)
* **Date**: Dreamdir scripts expect [ISO 8601](https://xkcd.com/1179/)-formatted dates (YYYY-MM-DD).

Beneath the headers, following a blank line, comes the text of the dream. As long as you don’t begin any later line with a header (i.e., a line containing a colon immediately followed by a hard tab), you can do anything you like here, though you may wish to look at the “Formatting guidelines” section, below.


Formatting guidelines
---------------------

Emphasis and verbatim quoting are not conventions currently recognized by any Dreamdir scripts. Lucid sections and commentary are recognized by the word count scripts (word counts can be split into “normal,” “lucid,” and “notes”). The vim syntax highlighting file recognizes all of these.

* **Emphasis**: Use `*single stars*` or `_underlines_` around the area to be emphasized.
* **Commentary**: Place notes that are not actually part of the dream in `[square brackets]`. The commentary may continue over multiple lines.
* **Verbatim quoting**: Place text that is directly quoted from some earlier form of notes (such as a notebook you scribbled in in bed) in `` `backticks` ``.
* **Lucid sections**: If you lucid dream, you can place sections where you knew you were dreaming in `{curly braces}`. I also use the header `Lucid:	1` to make it easier to find these dreams.

I use one physical line per paragraph and [double-space between sentences](http://stevelosh.com/blog/2012/10/why-i-two-space/), but I don’t see those conventions ever being expected by any code.

Suggested headers
-----------------

As mentioned earlier, you can use any headers you like as long as you include the ID number and the date. As a starting point, here are the ones I currently use:

* **People**: Comma-separated list of waking-life people who appeared in the dream.
* **Places**: Ditto for places with proper names and general geographic regions.
* **Tags**: List of motifs, categories, and other elements that are useful to track across multiple dreams but don’t fit into other headers.
* **Title**: A title...
* **Time**: If I had a clock handy and remembered to write it down, the time at which I woke up from the dream.
* **Lucid**: Included and with a value of 1 if the dream was lucid at any point.


File names and locations
------------------------

All dreams are kept in the main directory. A dream’s filename is its ID number with a `.dre` extension, e.g., `00592.dre`.

There are several other files and directories in a standard Dreamdir. A file listing of the Dreamdir might look something like this:

    -rw-------  1 soren soren   623 Dec 14  2014 00001.dre
    -rw-rw-r--  1 soren soren   210 Feb 14 19:00 00002.dre
    [...]
    -rw-------  1 soren soren  3075 Apr 28 21:25 01227.dre
    -rw-------  1 soren soren  1600 Apr 27 13:21 01228.dre
    -rw-rw-r--  1 soren soren     0 Apr 29 15:56 .dreamdir
    -rwxrwxr-x  1 soren soren 30337 Apr 29 13:32 dr
    drwxr-xr-x  2 soren soren  4096 Jan 17 19:37 graphs
    drwxr-xr-x 4 soren soren   4096 Apr 29 16:02 scripts
    -rw-rw-r-- 1 soren soren    163 Jan  7 22:39 TODO.txt

Of note:

* There is a `.dreamdir` file, which marks this directory as a Dreamdir. The content is currently unimportant, but scripts may check for this file to ensure they’re working in a dreamdir.
* The `dr` script is located in the Dreamdir.
* Other scripts, including the `ddirparse` Python library `dr` uses for several tasks, are in the `scripts/` subdirectory.
* Graphs generated by scripts go in the `graphs` subdirectory.

Installation / creating a Dreamdir
==================================

The minimum you need to do to start your dreamdir is to clone down this repository, delete or move any files you don’t want (`LICENSE`, `README`, etc.), then `touch .dreamdir` to mark the folder as a dreamdir.

You may also wish to set the environment variable `$DREAMDIR` to the path to your dreamdir and symlink the `dr` script somewhere on your `$PATH`; this way you can run `dr` from anywhere in your filesystem.

If you want to use any graphs, you should `mkdir graphs`.

There are two implementations of the dreamdir word count program, one in C and one in Python. The Python one will be acceptable for small dreamdirs, but the C implementation is over 20 times faster and is therefore better for large numbers of dreams. You can build the C implementation by changing into the scripts directory and running `make`; this requires gcc. The `word-count` function of `dr` will automatically choose the C implementation if it has been built, and the Python implementation otherwise.

(Note: The C implementation probably doesn’t count multibyte characters exactly right; this leads to insignificant errors if you use only a few as I do, but might be a problem if you’re writing in a non-Latin alphabet. Let me know if you have problems or suggestions for this.)

I keep my dreamdir under `git` control to keep track of any revisions I make to headers and dreams and as an extra backup against scripting and [PEBKAC](https://en.wikipedia.org/wiki/User_error#Acronyms_and_other_names) errors. You may wish to do likewise.

`dr` should run on any POSIX-compliant system with a modern version of `bash` and `python2`. The graph/plot functions currently require an installation of R with ggplot2; in the future I may look into using a Python plot library instead to get rid of this annoying dependency.

Dreamdir scripts
================

A number of scripts, largely written in Python, are provided in the `scripts/` directory of this repository; you may wish to use some of these as models for building your own scripts. Of particular note is `ddirparse.py`, which is a general library for use in developing Dreamdir scripts.

I don’t make any guarantees about the general applicability of these scripts. In particular, you should read through the code of any script you hope to use before using it; you may find there are still file paths or other constants only applicable to my system lurking in there somewhere.

Vim plugin
==========

For those who use vim, my syntax highlighting and ftplugin files are located in the `vim/` directory; you can install these to your `~/.vim` directory directly or use your favorite plugin manager.

You may want to remove the `setlocal cpoptions+=J` (`:help cpo-J`) line from `vim/ftplugin/dream.vim` if you don’t want to double-space between sentences (see the “Formatting guidelines” section above).

Tags functionality for vim is also included. The tags file contains tags for all dream ID numbers and all header values. You can do a number of handy things with this. Among others:

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

The `dr` script provides convenient tools to manage your dreamdir. The script assumes the current directory is your dreamdir, so it may be run like this:

    $ cd ~/dreams
    $ ./dr new

Alternatively, `dr` recognizes the environment variable `$DREAMDIR` as the path to your dreamdir. If this variable is defined and you are not currently in a dreamdir when you run `dr`, that directory will be used instead.

Detailed help on all the functions and options you have can be obtained at the command line. There are three pages of help:

* `dr help`: Shows a brief listing of all the actions available.
* `dr help search`: Shows information on search expressions.
* `dr help header-replace`: Shows information on header search-and-replace (this can be used to merge two similar tags together, for instance).

Note that all commands can be abbreviated by their initials; `find` is `f`, for example, and `dump-headers` is `dh`. Keywords in search expressions can be abbreviated similarly, so to find dreams tagged with `Maud` in the `People` field, we can use `dr f t People Maud` as well as `dr find tagged People Maud`. The long names are normally used throughout the documentation for clarity, and they are easier to remember when you’re getting started, but once you know what you’re doing you can save quite a few keystrokes this way.

Searching walkthrough
---------------------

A complete reference on search commands, along with a few concise examples, is available by running `dr help search`. This section will instead give some examples of actually doing something with the program to give you an idea of what is possible.

Though unassuming, the search function is quite powerful. The most common use is probably to look at or edit a given dream number:

    $ dr dump-headers 429
    Id: 00429
    Date:   2012-04-28
    Places: Chicago
    People: U.J, M.
    Tags:   Cinco de Mayo, marijuana, drugs

    $ dr edit 429
    ==> vim 00429.dre

Assuming your editor supports opening multiple files at once, it’s also handy to open a set of dreams that you’re interested in looking at or editing:

    $ dr edit 0100[345]
    ==> vim 01003.dre 01004.dre 01005.dre

This is all well and good if we know what specific dream we’re looking for, but what if we don’t? Imagine we look at #429 and decide we want to investigate the motif of marijuana further. What other dreams include it?

    $ dr find tagged Tags marijuana
    4 matches: [429, 584, 1181, 1198]

I happen to know offhand that there’s also a dream that involves heroin (not its use, thankfully). Maybe we should look at that, too. We are allowed to put any number of criteria in one search expression and have the results ORed together:

    $ dr find tagged Tags 'marijuana' tagged Tags 'heroin'
    5 matches: [429, 584, 1181, 1198, 426]

Since the tag search uses extended regular expressions and both of our criteria are searching in the Tags field, we could also combine these:

    $ dr find tagged Tags 'marijuana|heroin'
    5 matches: [426, 429, 584, 1181, 1198]

When did I have those dreams?

    $ dr get-header Date 429 584 1181 1198 426
    429: 2012-04-28
    584: 2012-09-10
    1181: 2016-03-26
    1198: 2016-04-04
    426: 2012-04-27

If we wanted to look closer here, of course, we could use `dump-headers` to get an idea about what happened in these dreams, and `cat` or `edit` if we wanted to read the actual reports.

So that we can get a better look at the more heavy-duty search features, let’s look at a different motif that shows up more frequently in my own dreams: trains.

    $ dr find tagged Tags train
    46 matches: [97, 105, 225, 269, 276, 299, 308, 416, 420, 456, 514, 563, \
                 612, 668, 681, 709, 724, 725, 771, 774, 779, 785, 801, 872, \
                 878, 923, 976, 979, 981, 987, 1005, 1031, 1032, 1044, 1080, \
                 1103, 1114, 1162, 1182, 1188, 1191, 1205, 1210, 1213, 1216, 1222]

Some of these no doubt involve *traveling* with a train, but some of them do not. How can we sort these out? Assuming we have added the tag “travel” as appropriate, we can use the `winnow` function. This takes a list of filenames on standard input, runs another search, and outputs only the filenames from standard input that also match the search criteria. We can use it in a pipeline, beginning with `filename-display`, like so:

    $ dr filename-display tagged Tags train | dr winnow tagged Tags travel
        00097.dre 00105.dre 00299.dre 00724.dre 00771.dre 00785.dre 00872.dre \
        00979.dre 00987.dre 01031.dre 01032.dre 01103.dre 01114.dre 01188.dre \
        01205.dre 01222.dre

The filename output might not be what we prefer. If we want to take a search action on the results of a pipeline like this, we can use the `act` action (note the use of `!!` for the previous command):

    $ !! | dr act get-header Places
    771: San Diego
    785: St. Olaf, California
    872: Sunnyside, U.J.'s house
    979: Dune Park station
    987: St. Olaf
    1031: St. Olaf, Buntrock
    1032: TLC, Home Lodge
    1114: Milwaukee
    1188: Chicago, Dune Park station
    1205: Atlantic City

(Note that there are only 10 results, but there are in fact 16 matches: `get-header` displays nothing if an input dream doesn’t have that header, and **Places** is an optional header.) Of course, the output can also be piped into another `winnow` command for further refinement.

Those are the ones that involved both trains and travel, but what about the ones that involve trains but *not* travel? With a moderate input size such as this one, we could manually take the set difference, but that would be stupid when we have the `-v` option:

    $ dr filename-display tagged Tags train | dr winnow -v tagged Tags travel | dr act find
    30 matches: [225, 269, 276, 308, 416, 420, 456, 514, 563, 612, 668, 681, \
                 709, 725, 774, 779, 801, 878, 923, 976, 981, 1005, 1044, \
                 1080, 1162, 1182, 1191, 1210, 1213, 1216]

If we want to check that we got the right result, we might want to OR two AND conditions together and confirm that we get the original values. We can do this using our shell’s command substitution, taking advantage of the fact that a list of filenames is a valid search expression:

    $ dr find $(dr filename-display tagged Tags train | dr winnow -v tagged Tags travel) \
              $(dr filename-display tagged Tags train | dr winnow tagged Tags travel)
    46 matches: [225, 269, 276, 308, 416, 420, 456, 514, 563, 612, 668, 681, \
                 709, 725, 774, 779, 801, 878, 923, 976, 981, 1005, 1044, \
                 1080, 1162, 1182, 1191, 1210, 1213, 1216, 97, 105, 299, 724, \
                 771, 785, 872, 979, 987, 1031, 1032, 1103, 1114, 1188, 1205, 1222]

You will probably seldom need such a complicated condition, but it is possible to make one just using I/O redirection.

I’ve left out several useful types of search expressions; in addition to finding tags in headers and selecting dream numbers individually or with globs, you can do full-text search (`grep`), select numbers backwards from the end (`back` and `last`), and select some dreams randomly for your entertainment or edification (`random`). See `dr help search` for all the options.


Summarizing headers
-------------------

There are two more search functions that are useful if you don’t know what kind of tags and header values you have. These are more *list* tools than strictly *search* tools, but they can be used with search expressions as well. Often you may want to use them on all your dreams; conveniently (and not accidentally), a blank search expression is the same as selecting all dreams.

What headers do we actually use in our dreamdir?

    $ dr list-headers
    Date
    Id
    Lucid
    People
    Places
    Tags
    Time
    Title

From these options, we might like to take a closer look at, say, the places that show up in our dreams. We might also like to know *how often* these places appear; for this, we can use the *frequency*, `-f` option (also applicable to `list-headers`):

    $ dr header-values -f Places
    175 Sunnyside
    160 St. Olaf
     76 VHS
     65 TLC
    [...]
      5 Chapel of the Resurrection
      5 Chesterton Montessori
      5 Luther College
      5 Regents Hall
    [...]
      1 Quinlan & Fabish Pens
      1 Regents
      1 Ritolado
    [...]
      1 Wrigley Field

The output is sorted by frequency, then in alphabetical order, or just in alphabetical order if you don’t show frequency.

There’s something wrong with this output, though: I have **Regents Hall** as well as **Regents**. In fact, these are the same building; I’ve made a sloppy mistake in tagging. It’s time to use `header-replace`.

Header search and replace
-------------------------

As seen in the above example, sometimes you will probably want to merge two tags together, or change the name of a tag. This can be a real pain manually and make you question the wisdom of using plain text files instead of a database. But never fear, `header-replace` comes to the rescue.

First we may wish to make sure that we have the right search expression to find the tag that’s wrong (`Regents`). The form of search expression we use with `dr find tagged` and `dr header-replace` is an *hregex*, the precise definition of which can be found in the online help (`dr help search`). For now, we just need to know that we can match the beginning and the end of a tag with `^` and `$` (the beginning- and end-of-line anchors in standard regexes). Thus:

    $ dr dump-headers tagged Places '^Regents$'
    Id:	01121
    Date:	2016-02-21
    Time:	5:45
    People:	M.
    Places:	Sunnyside, Regents, St. Olaf
    Tags:	travel

Then we actually call `header-replace` for the dreamdir:

    $ dr header-replace Places '^Regents$' 'Regents Hall'
                        === Preview of changes to be applied ===
    01121.dre:
      -Regents
      +Regents Hall
      =Places:	Sunnyside, Regents Hall, St. Olaf

    Changes will affect 1 file.
    To make these changes, rerun the command with the '-f' option.

Since the diff output looks like what we wanted, we then call it again with the *force*, `-f`, parameter to actually make the changes:

    $ dr header-replace -f Places '^Regents$' 'Regents Hall'
    You are about to apply a search-and-replace that will affect 1 dream.
    If this doesn't sound right, please check the results without -f first!
    Do you wish to continue (y/n)?

    01121.dre modified
    Changed 1 file.

Note the two-step process. You should definitely *not* try to skip the first step; since this is essentially just a really fancy way of using `sed` across all your dream files, a particularly badly formed regex (e.g, replace `.` with `q`) could do very bad things to your dreams (pun intended).

Of course, this example is trivial, and this particular error could be fixed much faster by doing `dr edit` and changing the tag manually; the real benefit comes when there are tens of dreams (or more) that need changes.

Support & Development
=====================

Please post bugs on the Github issue tracker; if you prefer you can email me at `contact@sorenbjornstad.com`. If you have a problem with `dr`, please mention your operating system and version of bash.

Improvements and pull requests are welcome as long as you release your code under the MIT license and they are consistent with the project’s philosophy. Please make sure that `tests/pre-commit-hook.sh` exits successfully before submitting any modifications to `dr`; this requires [shellcheck](http://www.shellcheck.net/), [BATS](https://github.com/sstephenson/bats), and GCC. If you have modified the behavior of `dr`, you may need to change the tests in `tests/test_dr`; they are pretty easy to figure out. If you don’t want to install `shellcheck` (it requires Haskell and takes some time to install), you can paste the code on the shellcheck website and then run `tests/test_dr` and `cd scripts && make clean && make` manually to finish the pre-commit tests.
