
from collections import namedtuple

from .stim import Lang

# Number of subject profiles to create
# (more may be created if necessary to have an equal number
# for each condition)
n_profiles = 200

timeout_secs = 3600

qnaire_quests = [
    ['radio', 'What is your age range?',
     '18-24', '25-34', '35-44',
     '45-54', '55-64', '65 and older'],
    ['radio', 'What is your highest completed level of education?',
     'Less than high school diploma',
     'High school diploma or equivalent (for example: GED)',
     'Some college credit, no degree',
     'Trade/technical/vocational training',
     'Associate degree',
     'Bachelor’s degree',
     'Master’s degree',
     'Professional degree',
     'Doctorate degree'],
    ['shorttext', 'What is your native language? (the language that you learned first before you were 5)'],
    ['shorttext', 'List any other languages you speak'
     ' (to any level of ability);'
     ' answer "none" if no other languages'],
    ['shorttext', 'Briefly describe any prior experience with'
     ' or knowledge of linguistics you have'],
#    ['radio', 'Do you have any significant hearing problems'
#     ' that would make it difficult for you to take part'
#     ' in an experiment involving listening?', 'Yes', 'No']
]

exit_qnaire_quests = [
    ['checkbox', 'How did you approach the first part of the experiment (choose all that apply)?',
     'just listened to the words ', 'went by intuition or gut feeling', 'looked for a rule or a pattern',
     'took notes'],
     ['shorttext', 'Please describe what you did in as much detail as possible. If you looked for a rule, what rules did you try?'],
     ['checkbox', 'How did you approach the second part of the experiment (choose all that apply)?',
      'chose words randomly', 'went by intuition or gut feeling', 'used a rule/pattern I identified in part I',
     'relied on my notes'],
     ['shorttext', 'Again please describe in detail what you did. If you relied on a rule, what was it?'],
     ['shorttext', 'What percent of the test questions do you think you got right?']
]

# Number of training and testing trials
n_trials = {'train': 20, 'test': 10}

audio_dir = 'audio'

# Data structure for language probabilities (base rate and feature)
LangProbs = namedtuple('LangProbs', 'br feat')

control_probs = {Lang.A: LangProbs(0.25, 1), Lang.B: LangProbs(0.75, 0)}
#control_probs = {Lang.A: LangProbs(0.25, 0.69), Lang.B: LangProbs(0.75, 0.23)}
actual_probs = {Lang.A: LangProbs(0.35, 0.8), Lang.B: LangProbs(0.65, 0.35)}

probs = actual_probs

# Compute number of stimuli of each lang for each phase
# (and number of stims that have feat within each lang)
# NB: use of ints alters probabilities slightly
stim_counts = {}
for phase in 'train', 'test':
    stim_counts[phase] = d = {Lang.A: {}, Lang.B: {}}
    d[Lang.A]['all'] = round(probs[Lang.A].br*n_trials[phase])
    d[Lang.B]['all'] = n_trials[phase] - d[Lang.A]['all']
    d[Lang.A]['feat'] = round(d[Lang.A]['all']*probs[Lang.A].feat)
    d[Lang.B]['feat'] = round(d[Lang.B]['all']*probs[Lang.B].feat)

