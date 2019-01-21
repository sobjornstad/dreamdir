/* drwc - Dreamdir word count utility
 * Copyright 2016 Soren Bjornstad.
 * See usage message string below.
 *
 * Exit status:
 * 0 - success
 * 1 - invalid command-line parameters
 * 2 - file not found
 * 127 - impossible condition invoked (programming error)
 */

#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <getopt.h>

#define READ_CHUNK 4000

struct dream_wc {
    unsigned normal;
    unsigned lucid;
    unsigned notes;
};

struct options {
    bool show_normal;
    bool show_lucid;
    bool show_notes;
    bool show_total;
    bool pretty_print;
    bool summary_only;
};

void usage_msg (char **argv);
struct options new_opts (void);
struct options parse_opts (int argc, char **argv, int *shift_args);
struct dream_wc wc (char *name);
void print_counts (const struct dream_wc *counts, const char* filename,
                   const struct options *opts);
int main (int argc, char **argv);

const char *USAGE_MSG =
  "drwc - Dreamdir word count utility\n"
  "Copyright (c) 2016 Soren Bjornstad; see LICENSE for details.\n"
  "\n"
  "Usage: %s [options] filenames...\n"
  "Print word count for arguments, not including headers.\n"
  "\n"
  "Options:\n"
  "-h   Show this usage message.\n"
  "-n   Display the count of \"normal\" words (not in notes or lucid sections).\n"
  "-l   Display the count of \"lucid\" words (words in {curly braces}).\n"
  "-o   Display the count of \"notes\" words (words in [square brackets]).\n"
  "-t   Display the total of the above counts.\n"
  "-p   Pretty-print results, rather than showing the machine-readable format.\n"
  "-s   Display only the total (summary) word count, not each file's count.\n"
  "\n"
  "Counts are always shown in the order <normal> <lucid> <notes> <total>, with\n"
  "gaps for any counts that are not included. The machine-readable format is\n"
  "separated by spaces; the pretty format is separated by newlines and has labels.\n"
  "\n"
  "If none of -nlot are used, all four counts will be shown.\n";

void usage_msg (char **argv)
{
    printf(USAGE_MSG, argv[0], argv[0]);
}

struct options new_opts (void)
{
    struct options opts = {false, false, false, false, false};
    return opts;
}

struct options parse_opts (int argc, char **argv, int *shift_args)
{
    /* short-circuited if argc < 2 */
    if (argc < 2 || !strcmp(argv[1], "--help")) {
        usage_msg(argv);
        exit(argc < 2 ? 1 : 0);
    }

    struct options opts = new_opts();
    char opt;
    opterr = 0; // say we want to do our own error handling for getopt
    while ((opt = getopt(argc, argv, "hnlotps")) != -1) {
        switch (opt) {
            case 'h':  usage_msg(argv);           exit(0);
            case 'n':  opts.show_normal  = true;  break;
            case 'l':  opts.show_lucid   = true;  break;
            case 'o':  opts.show_notes   = true;  break;
            case 't':  opts.show_total   = true;  break;
            case 'p':  opts.pretty_print = true;  break;
            case 's':  opts.summary_only = true;  break;
            case '?':
                fprintf(stderr, "Invalid option '%c'.\n", optopt);
                usage_msg(argv);
                exit(1);
                break;
            default:
                fprintf(stderr, "Unhandled case %c in option routine!\n", opt);
                exit(127);
                break;
        }
    }
    /* If we didn't specify what we wanted to show, we want to see everything. */
    if (! (opts.show_normal || opts.show_lucid ||
           opts.show_notes  || opts.show_total) ) {
        opts.show_normal = opts.show_lucid =
            opts.show_notes = opts.show_total = true;
    }

    *shift_args = optind;
    return opts;
}

struct dream_wc wc (char *name)
{
    FILE *fstream;
    fstream = fopen(name, "r");
    if (!fstream) {
        fprintf(stderr, "Could not open '%s' for reading. "
                "Does the file exist?\n", name);
        exit(2);
    }

    struct dream_wc counts = {0, 0, 0};
    bool inHeaders = true, inLucid = false, inNotes = false;
    bool inWord = false;

    char buff[READ_CHUNK];
    while (fgets(buff, READ_CHUNK, fstream)) {
        /* Skip ahead until we're past the headers so as not to count them. */
        if (inHeaders) {
            if (buff[0] == '\n')
                inHeaders = false;
            continue;
        }

        for (int i=0; buff[i] != '\0'; ++i)
        {
            if (isalnum(buff[i]) || buff[i] == '\'') {
                if (!inWord) { /* starting a word, increase count */
                    if (inNotes)
                        counts.notes++;
                    else if (inLucid)
                        counts.lucid++;
                    else
                        counts.normal++;
                }
                inWord = true;
            } else { /* ending a word */
                inWord = false;
            }

            switch(buff[i]) {
                case '[':  inNotes = true;   break;
                case ']':  inNotes = false;  break;
                case '{':  inLucid = true;   break;
                case '}':  inLucid = false;  break;
            }
        }
    }
    fclose(fstream);
    return counts;
}

void print_counts (const struct dream_wc *counts, const char* filename,
                   const struct options *opts)
{
    if (opts->pretty_print) {
        if (!opts->summary_only)
            printf("\n");
        printf("~ %s ~\n", filename);
    }
    if (opts->show_normal)
        printf(opts->pretty_print ? "Normal:\t%d\n" : "%d ", counts->normal);
    if (opts->show_lucid)
        printf(opts->pretty_print ? "Lucid:\t%d\n" : "%d ", counts->lucid);
    if (opts->show_notes)
        printf(opts->pretty_print ? "Notes:\t%d\n" : "%d ", counts->notes);
    if (opts->show_total)
        printf(opts->pretty_print ? "Total:\t%d\n" : "%d ",
               counts->normal + counts->lucid + counts->notes);
    if (!opts->pretty_print) {
        printf("%s", filename);
        printf("\n");
    }
}

int main (int argc, char **argv)
{
    int shift_args;
    struct options opts = parse_opts(argc, argv, &shift_args);
    argv += shift_args; /* argv now points to start of filenames */

    struct dream_wc total_counts = {0, 0, 0};
    struct dream_wc count;

    if (! *argv) {
        /* no filenames given */
        usage_msg(argv - shift_args);
        exit(1);
    }
    while (*argv) {
        count = wc(*argv);
        if (!opts.summary_only)
            print_counts(&count, *argv, &opts);
        total_counts.normal += count.normal;
        total_counts.lucid  += count.lucid;
        total_counts.notes  += count.notes;
        argv++;
    }

    print_counts(&total_counts, "total", &opts);
    return 0;
}
