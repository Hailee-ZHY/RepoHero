from transformers import pipeline
import logging, os, csv
import Levenshtein
import sys 

# sys.stdout.reconfigure(encoding='utf-8') 

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')

fill_mask = pipeline('fill-mask', model='distilbert-base-uncased')
mask = fill_mask.tokenizer.mask_token

def get_typo_locations(fh):
    tsv_f = csv.reader(fh, delimiter='\t')
    for line in tsv_f:   
        yield (
            # line[0] contains the comma separated indices of typo words
            [int(i) for i in line[0].split(',')],
            # line[1] contains the space separated tokens of the sentence
            line[1].split()  
        )

def select_correction(typo, predict):

    best_score = -1
    best_word = typo  
    alpha = 0.8
    
    for p in predict:
        cand = p['token_str']  

        # -- Calculate combined score (distance+score)---
        # Using the Levenshtein distance to measure similarity between
        # Score 0.23->0.63
        sim = 1 - Levenshtein.distance(typo, cand) / max(len(typo), len(cand))
        score = (alpha * sim) + ((1-alpha) * p['score'])


        # --- filter out the candidates identical to typo ---
        # Score 0.75 -> 0.76

        if score > best_score and typo.lower() != cand.lower():
            best_score = score
            best_word = cand

            # print((best_score, best_word))
            
        # --- Capitalization handling ---
        # If the original word starts with a capital letter,
        # capitalize the chosen correction as well.
        # Score 0.63 -> 0.70
        if typo and typo[0].isupper():
            best_word = best_word.capitalize()    
            
    return best_word

def spellchk(fh):
    for (locations, sent) in get_typo_locations(fh):
        spellchk_sent = sent
        for i in locations:
            # predict top_k replacements only for the typo word at index 
            predict = fill_mask(
                " ".join([ sent[j] if j != i else mask for j in range(len(sent)) ]), 

                # ---Increase top_K from 20 to 500 ---
                # Increase top_k to have more candidates for selection
                # Score 0.70 -> 0.75
                top_k=500  
            )
            logging.info(predict)
            spellchk_sent[i] = select_correction(sent[i], predict)
        yield(locations, spellchk_sent)

if __name__ == '__main__':
    import argparse
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-i", "--inputfile", 
                            dest="input", 
                            default=os.path.join('data', 'input', 'dev.tsv'), 
                            help="file to segment")
    argparser.add_argument("-l", "--logfile", 
                            dest="logfile", 
                            default=None, 
                            help="log file for debugging")
    opts = argparser.parse_args()
 
    if opts.logfile is not None:  
        logging.basicConfig(filename=opts.logfile, filemode='w', level=logging.DEBUG)

    with open(opts.input) as f:
        for (locations, spellchk_sent) in spellchk(f):
            print("{locs}\t{sent}".format(
                locs=",".join([str(i) for i in locations]),
                sent=" ".join(spellchk_sent)
            ))
