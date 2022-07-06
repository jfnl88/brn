
from dataclasses import dataclass
from enum import Enum


class Lang(Enum):
    A = 0
    B = 1


@dataclass
class Stim:
    feat: str
    pron: str
    lang: Lang

    @classmethod
    def parse(cls, text):
        inst = super().__new__(cls)
        fields = text.split('\t')
        inst.feat = fields[0]
        inst.pron = fields[1]
        inst.lang = Lang[fields[2]]
        return inst

    def format_save(self):
        return f'{self.feat}\t{self.pron}\t{self.lang.name}'
