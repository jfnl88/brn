
from expert.tasks import Task

from . import params
from .stim import Lang


class TrialTask(Task):

    # Abstract base class for all trial tasks types
    def __init__(self, inst, template=None, variables=None, timeout_secs=None):
        super().__init__(inst, template, variables, timeout_secs)

    def find_sound(self, pron):
        audiopath = self.inst.static_path / params.audio_dir
        globpat = f'{pron.replace(" ", "-")}.mp3'
        matches = list(audiopath.glob(globpat))
        assert len(matches) == 1, \
            f'need exactly 1 match for "{pron}", got {len(matches)}'
        return matches[0].stem


class Listen(TrialTask):

    def __init__(self, inst, stim, lang_transports,
                 variables=None, timeout_secs=None):
        super().__init__(inst, 'listen', variables, timeout_secs)
        self.variables['sound'] = self.find_sound(stim.pron)
        self.variables['transport'] = lang_transports[stim.lang]
        # the transport for lang A (always shown on the left)
        self.variables['a_transport'] = lang_transports[Lang.A]
        self.resp_extra['transport'] = lang_transports[stim.lang]


class TwoAFC(TrialTask):

    def __init__(self, inst, stim, lang_transports,
                 variables=None, timeout_secs=None):
        super().__init__(inst, 'twoafc', variables, timeout_secs)
        langs = list(Lang)
        # the correct answer
        self.correct_ans = lang_transports[stim.lang]
        # the transport for lang A (always shown on the left)
        self.variables['a_transport'] = lang_transports[Lang.A]
        self.variables['sound'] = self.find_sound(stim.pron)
        if not self.variables.get('fback'):
            self.variables['fback'] = False
        # save correct answer in the participant response extra field
        self.resp_extra['transport'] = lang_transports[stim.lang]

    def get_feedback(self, response):
        return response == self.correct_ans
