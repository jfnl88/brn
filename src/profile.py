
# **************************************************
# Profile
#
# Contains ordered stimuli to be presented to a
# single subject as they progress through the
# experiment.
# **************************************************

import random

import expert
from expert import profile
from expert.tasks import TaskDesc

from . import cond, params, stim, trialtasks



mode_tasks = {
    'implicit': {'train': trialtasks.Listen, 'test': trialtasks.TwoAFC},
    'explicit': {'train': trialtasks.TwoAFC, 'test': trialtasks.TwoAFC}
}


class Profile(profile.Profile):

    def __init__(self, condition):
        super().__init__(condition)
        b_flag = [f for f in cond.flags
                       if f != self.cond.flag][0]
        self.lang_flags = {
            stim.Lang.A: self.cond.flag,
            stim.Lang.B: b_flag
        }

        all_stims = {}
        for sign in '+-':
            featstr = f'{sign}{self.cond.feat}'
            with open(expert.experclass.dir_path /
                      f'stims{featstr}.txt') as f:
                # a set is used so we can easily remove used items
                # with set operations in self.choose_stims()
                all_stims[sign] = {l.rstrip() for l in f.readlines()}

        self.train_stims, self.test_stims = self.choose_stims(all_stims)

    @classmethod
    def load(cls, cond_str, subjid):
        inst = super().load(cond_str, subjid)
        with open(expert.experclass.profiles_path / cond_str / subjid) as f:
            b_flag = [t for t in cond.flags
                           if t != inst.cond.flag][0]
            inst.lang_flags = {
                stim.Lang.A: inst.cond.flag,
                stim.Lang.B: b_flag
            }
            inst.train_stims = [stim.Stim.parse(f.readline().rstrip())
                                for i in range(params.n_trials['train'])]
            inst.test_stims = [stim.Stim.parse(f.readline().rstrip())
                               for i in range(params.n_trials['test'])]
        return inst

    def save(self):
        fname = expert.experclass.profiles_path / self.cond.name / self.subjid
        with open(fname, 'w') as f:
            for s in self.train_stims:
                print(s.format_save(), file=f)
            for s in self.test_stims:
                print(s.format_save(), file=f)

    def choose_stims(self, avail_stims):
        # [train_stims, test_stims]
        audio = []
        for phase in 'train', 'test':
            stims = []
            cond_sign = '+' if self.cond.sign == 'pos' else '-'
            other_sign = '-' if cond_sign == '+' else '+'
            for lang in stim.Lang:
                counts = {}
                counts[cond_sign] = params.stim_counts[phase][lang]['feat']
                counts[other_sign] = \
                    params.stim_counts[phase][lang]['all'] - counts[cond_sign]
                # choose +feat and -feat stims
                for sign in '+-':
                    # sample available stims
                    sample = set(random.sample(avail_stims[sign], counts[sign]))
                    avail_stims[sign] -= sample
                    featstr = f'{sign}{self.cond.feat}'
                    for pron in sample:
                        stims.append(stim.Stim(featstr, pron, lang))
            random.shuffle(stims)
            audio.append(stims)
        return audio

    def training_tasks(self):
        return [
            TaskDesc([
                mode_tasks[self.cond.mode]['train'],
                stim,
                self.lang_flags,
                'training',
                {'fback': True}])
            for stim in self.train_stims]

    def testing_tasks(self):
        return [
            TaskDesc([
                mode_tasks[self.cond.mode]['test'],
                stim,
                self.lang_flags,
                'testing'])
            for stim in self.test_stims]
