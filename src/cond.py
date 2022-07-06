

from dataclasses import dataclass
from functools import cached_property


modes = ['implicit', 'explicit']
feats = ['disyll', 'onset', 'coda']
transports = ['train', 'boat']


@dataclass(frozen=True)
class Cond:
    mode: str
    feat: str
    # transport type for language A
    transport: str

    @cached_property
    def name(self):
        return f'{self.mode}-{self.feat}-{self.transport}'

    def __str__(self):
        return self.name


conds = {}
for mode in modes:
    for feat in feats:
        for transport in transports:
            c = Cond(mode, feat, transport)
            conds[c.name] = c
del c
