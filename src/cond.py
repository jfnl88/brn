

from dataclasses import dataclass
from functools import cached_property


modes = ['implicit', 'explicit']
feats = ['disyll', 'onset', 'coda']
flags = ['star', 'crown']


@dataclass(frozen=True)
class Cond:
    mode: str
    feat: str
    # flag for language A
    flag: str

    @cached_property
    def name(self):
        return f'{self.mode}-{self.feat}-{self.flag}'

    def __str__(self):
        return self.name


conds = {}
for mode in modes:
    for feat in feats:
        for flag in flags:
            c = Cond(mode, feat, flag)
            conds[c.name] = c
del c
