#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#define bool short int
#define true 1
#define false 0

typedef struct {
    long test;
    long* parts;
} predicate_t;

void free_preds(predicate_t** equations) {
    for (int eqidx = 0; equations[eqidx] != NULL; eqidx++) {
        free(equations[eqidx]->parts);
        free(equations[eqidx]);
    }
    free(equations);
}

bool matches(predicate_t* equation, bool with_concat) {
    bool ret = true;

    if(equation->parts[1] == -1) {
        return equation->test == equation->parts[0];
    }
    if(equation->parts[0] >= equation->test) {
        return false;
    }

    long pre1 = equation->parts[0], pre2 = equation->parts[1];
    equation->parts++;

    equation->parts[0] = pre1 + pre2;
    if(!matches(equation, with_concat)) {
        equation->parts[0] = pre1 * pre2;
        if(!matches(equation, with_concat)) {
            long pow = 1;
            while(pre2 >= pow) pow *= 10;
            equation->parts[0] = pre1 * pow + pre2;  
            if(!with_concat || !matches(equation, with_concat)) {
                ret = false;
            }
        }
    }

    equation->parts--;
    equation->parts[0] = pre1;
    equation->parts[1] = pre2;

    return ret;
}

predicate_t** read_input(char* fname) {
    FILE* fp = fopen(fname, "r");
    if(!fp) {
        perror("Cannot read file");
        return NULL;
    }

    predicate_t** equations = malloc(sizeof(predicate_t*) * 1000);
    char line[512];
    char* chunk;
    int eqidx;
    for(eqidx=0;;eqidx++) {
        fgets(line, 512, fp);
        if (feof(fp)) break;
        
        predicate_t* new_pred = malloc(sizeof(predicate_t));
        chunk = strtok(line, ":");

        new_pred->test = atol(chunk);
        new_pred->parts = malloc(sizeof(long) * 100);
        
        int idx;
        for(idx = 0; (chunk = strtok(NULL, " ")); idx++) {
            new_pred->parts[idx] = atol(chunk);
        }
        new_pred->parts[idx] = -1;
        equations[eqidx] = new_pred;
    }
    equations[eqidx] = NULL;

    free(chunk);
    fclose(fp);

    return equations;
}

int main(int argc, char** argv) {
    predicate_t** equations;

    if (argc > 1) {
        equations = read_input(argv[1]);
    } else {
        equations = read_input("input");
    }

    long part1 = 0, part2 = 0;
    for (int eqidx = 0; equations[eqidx] != NULL; eqidx++) {
        if(matches(equations[eqidx], false)) {
            part1+=equations[eqidx]->test;
            part2+=equations[eqidx]->test;
        } else if(matches(equations[eqidx], true)) {
            part2+=equations[eqidx]->test;
        }
    }
    printf("Part 1: %ld\nPart 2: %ld\n", part1, part2);

    free_preds(equations);

    return 0;
}
