import json
from collections import OrderedDict

with open('input.json') as file:
    data = json.load(file)

dfa_states = 2 ** data["states"]
dfa_letters = data["letters"]
dfa_start = data["start"]
dfa_func = []
dfa_final = []
dfa_list = []
q = []

q.append((dfa_start,))

nfa = {}
dfa = {}

for transition in data["t_func"]:
    nfa[(transition[0], transition[1])] = transition[2]

for instate in q:
    for symbol in dfa_letters:
        if len(instate) == 1 and (instate[0], symbol) in nfa:
            dfa[(instate, symbol)] = nfa[(instate[0], symbol)]

            if tuple(dfa[(instate, symbol)]) not in q:
                q.append(tuple(dfa[(instate, symbol)]))
        else:
            dest = []
            f_dest = []

            for n_state in instate:
                if (n_state, symbol) in nfa and nfa[(n_state, symbol)] not in dest:
                    dest.append(nfa[(n_state, symbol)])

            if dest:
                for d in dest:
                    for value in d:
                        if value not in f_dest:
                            f_dest.append(value)

                dfa[(instate, symbol)] = f_dest

                if tuple(f_dest) not in q:
                    q.append(tuple(f_dest))
for key, value in dfa.items():
    temp_list = [[key[0], key[1], value]]
    dfa_func.extend(temp_list)

for q_state in q:
    for f_state in data["final"]:
        if f_state in q_state:
            dfa_final.append(q_state)

dfa = OrderedDict()
dfa["states"] = dfa_states
dfa["letters "] = dfa_letters
dfa["t_func"] = dfa_func
dfa["start"] = dfa_start
dfa["final"] = dfa_final

with open('output1.json', 'w') as output_file1:
    json.dump(dfa, output_file1, separators=('\t', ':'))
