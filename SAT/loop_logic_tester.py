
def test(val):
    if val >= 6:
        return True
    else:
        return False

last_distance_failed = 0
last_distance_found = 14 #da primo ciclo
last_distance_trial = 0

condizione_uscita = True

found = True

print("inizio ciclo")

while (last_distance_found - last_distance_failed > 1):

    #tento di dimezzare
    # if found:
    #     last_distance_trial = (last_distance_found + last_distance_failed) // 2
    # else:
    last_distance_trial = (last_distance_failed + last_distance_found) // 2

    print("last_distance_failed",last_distance_failed)
    print("last_distance_found",last_distance_found)
    print("last_distance_trial", last_distance_trial)
    print("found",found)
    print("-"*10)

    #testo la nuova distanza
    if test(last_distance_trial): #ritorna True/False per Sat/Unsat
        #caso SAT -> dimezzo ancora
        found = True
        last_distance_found = last_distance_trial
    else:
        #caso UNSAT -> media fra ultimo trovato e ultimo fallito
        found = False
        last_distance_failed = last_distance_trial

#stampa uscita da ciclo
print("SAT -> valore:",last_distance_found)