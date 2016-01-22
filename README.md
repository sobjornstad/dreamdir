Dreamdir – the Unix dream journal format

Introduction
============

*Dreamdir* is a format for storing a dream journal inspired by the popular [Maildir](https://en.wikipedia.org/wiki/Maildir) way of storing mailboxes and the RFC 2822 email format itself.

Dreamdir follows the *Unix philosophy*:

* All dreams are stored in plain text formatted in a consistent way. The format is human-readable and is normally read and written directly.
* Dreamdir is first and foremost a format, not an application. Simple code designed to do one thing well is provided to make working with this format easier.
* In addition to the provided code, standard Unix text-processing tools and simple scripts can easily manipulate dreams stored in a Dreamdir.

Features:

* Each dream is stored in its own plain text file.
* Each dream file begins with a list of attributes, such as the date, the names of people who appeared in the dream, and tags.
* The remainder of the dream file is simply the text of your entry, and you can do anything you like with it.
* The provided shell script `dr` makes it easy to create new dreams, check the validity of your dreamdir format, and do common searches.
* Example scripts are provided for tasks like graphing day-to-day recall and generating indexes. A small Python library is also available for user scripts.
* Free and open source: the Dreamdir format itself and this documentation are public domain, and all code is provided under the MIT license (see the LICENSE file for details).


Dreamdir format
===============

Formatting rules
----------------

Dreamdir scripts are permitted to assume that the rules specified in this section are followed, so you should definitely follow them. Conformance to some of the rules can be checked with the `dr validate` command.

The easiest way to learn the format is to look at an example dream file:

    Id:	00952
    Date:	2015-11-19
    Time:	6:02
    People:	M, MD, T [names written out in full in the actual dream file]
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

At the top you see the *attributes*, also called *headers*, especially when referring to their position in the file. Each attribute is separated from its *value* by a colon followed by a hard tab. (The requirement of a tab makes commands like `grep` easier to use, since a colon will not be followed by a tab in running text.) For attributes that can take multiple values, such as People, Places, and Tags, individual values are separated by a comma and a space.

Two attributes are **required** to form a valid dream file: the *Id* number and the *Date*. All other attributes are optional. There are no rules about what constitutes a valid attribute name, and it is fine for some dreams to not have a particular optional attribute at all. The headers can come in any order. Scripts may stop looking for header lines when they reach the first blank line.

The two required attributes are somewhat fussier, as follows:

* **Id**: Dreamdir uses fixed-width five-digit ID numbers, beginning at `00001` and increasing for each dream up to `99999`. (If you manage to record 100,000 dreams, I congratulate you and also suspect you have enough time on your hands to change a few scripts to use six-digit numbers!)
* **Date**: Dreamdir scripts expect ISO 8601-formatted dates (YYYY-MM-DD).

Beneath the attributes, following a blank line, comes the text of the dream. As long as you don’t begin any later line with a header (i.e., a line containing a colon immediately followed by a hard tab), you can do anything you like here, though you may wish to look at the “Formatting guidelines” section, below.


Formatting guidelines
---------------------

These conventions are currently not known to any Dreamdir scripts, but they are rules I follow and may end up being recognized by scripts in future versions, so you may wish to follow them too. If you use the vim syntax highlighting file, these conventions are also recognized by it.

* **Emphasis**: Use `*single stars*` around the area to be emphasized.
* **Commentary**: Place notes that are not actually part of the dream in `[square brackets]`. The commentary may continue over multiple lines.
* **Verbatim quoting**: Place text that is directly quoted from some earlier form of notes (such as a notebook you scribbled in in bed) in `` `backticks` ``.
* **Lucid sections**: If you lucid dream, you can place sections where you knew you were dreaming in `{curly braces}`. I also use the header `Lucid:	1` to make it easier to find these dreams.

I use one physical line per paragraph and [double-space between sentences](http://stevelosh.com/blog/2012/10/why-i-two-space/), but I don’t see those conventions ever being expected by any code.

Suggested attributes
--------------------

As mentioned earlier, you can use any attributes you like as long as you include the ID number and the date. As a starting point, here are the ones I currently use:

* **People**: Comma-separated list of waking-life people who appeared in the dream.
* **Places**: Ditto for places with proper names and general geographic regions.
* **Tags**: List of motifs, categories, and other elements that are useful to track across multiple dreams but don’t fit into other attributes.
* **Time**: If I had a clock handy and remembered to write it down, the time at which I woke up from the dream.
* **Lucid**: Included and with a value of 1 if the dream was lucid at any point.


File names and locations
------------------------

All dreams are kept in the main directory. A dream’s filename is its ID number with a `.dre` extension, e.g., `00592.dre`.

There are several other files and directories in a standard Dreamdir. A file listing of the Dreamdir might look something like this:

    -rw------- 1 soren soren   623 Dec 14  2014 00001.dre
    -rw------- 1 soren soren   211 May 18  2015 00002.dre
    [...]
    -rw------- 1 soren soren  4682 Jan  7 22:42 01021.dre
    -rw------- 1 soren soren  1823 Jan  7 19:41 01022.dre
    -rwxr-xr-x 1 soren soren  4949 Jan  8 07:20 dr
    drwxr-xr-x 2 soren soren  4096 Jan  2 09:54 graphs
    drwxr-xr-x 4 soren soren  4096 Jan  8 07:25 scripts
    -rw-rw-r-- 1 soren soren   163 Jan  7 22:39 TODO.txt

Of note:

* The `dr` script is located in the Dreamdir.
* Other scripts, including the `ddirparse` Python library `dr` uses for several tasks, are in the `scripts/` subdirectory.
* Graphs generated by scripts go in the `graphs` subdirectory.

Scripts may assume that the `dr` script and these two directories are present, and may use their presence to confirm that they are working in a Dreamdir.


The `dr` script
===============

The `dr` script provides convenient tools to manage your dreamdir. The script works on the current directory (i.e., $PWD), so is often run like this:

    $ cd ~/dreams
    $ ./dr new

Alternatively, `dr` recognizes the environment variable `$DREAMDIR` as the path to your dreamdir. If this variable is defined and you are not currently in a dreamdir when you run `dr`, that dreamdir will be used instead.

Usage information can be obtained with `./dr help`. Many of the actions are self-explanatory; some example usages are shown below.

    $ ./dr find-tagged People Maud
    8 matches: [80, 81, 106, 388, 524, 823, 937, 952]

    $ ./dr open-tagged People Maud
    (calls $EDITOR 00080.dre 00081.dre 00106.dre 00388.dre 00524.dre 00823.dre 00937.dre 00952.dre)

    $ ./dr header-list Places
    Arby's
    ARC
    Arts and Sciences Building
    ASB
    Australia
    [...]
    Whiting Energy Center
    Wisconsin
    Wrigley Field

    $ ./dr show-headers
    Date
    Id
    Lucid
    People
    Places
    Tags
    Time

    $ ./dr new
    (Run on January 8, 2016 with highest dream number 01022.
     New file opens in $EDITOR with content:)
    Id:	01023
    Date:	2016-01-08
    Time:	
    Tags:	

Note that `find-tagged` and `open-tagged` can optionally be used without a `value` parameter; in this case the search will look for all dreams that specify that header, regardless of its value.
