#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

#define READ_CHUNK 4000

struct dream_wc {
    unsigned normal;
    unsigned lucid;
    unsigned notes;
};

struct dream_wc wc (char *name)
{
    FILE *fstream;
    fstream = fopen(name, "r");

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

int main (int argc, char **argv)
{
    if (argc < 2) {
        printf("Dreamdir word count utility\n");
        printf("Copyright 2016 Soren Bjornstad.\n\n");
        printf("Usage: %s <filenames...>\n", argv[0]);
        printf("The cumulative word count of <filenames> will be printed, in the format:\n");
        printf("normal lucid notes total\n");
        exit(1);
    }

    struct dream_wc total_counts = {0, 0, 0};
    struct dream_wc count;

    for (int i=1; i < argc; ++i) {
        count = wc(argv[i]);
        total_counts.normal += count.normal;
        total_counts.lucid += count.lucid;
        total_counts.notes += count.notes;
    }

    printf("%d %d %d %d\n",
           total_counts.normal, total_counts.lucid, total_counts.notes,
           total_counts.normal + total_counts.lucid + total_counts.notes);
    return 0;
}
