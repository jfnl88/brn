
# Import built-in classes
from expert import Experiment, app
from expert.tasks import Task, Welcome, Consent, Soundcheck, Thankyou

# Import local modules
from . import params

from .stim import Lang

# Your experiment class must be a subclass of expert.experiment.Experiment,
# but can have any name

class Brn(Experiment):

    # Title for experiment browser window
    window_title = 'Language experiment'

    @classmethod
    def _make_profiles(cls):
        # Print out actual probabilities, which may differ
        # slightly from specified probabilities
        for phase in 'train', 'test':
            app.logger.info(f'phase: {phase}')
            d = params.stim_counts[phase]
            for lang in Lang:
                app.logger.info(f'  lang: {lang}')
                n_br = d[lang]['all']
                p_br = n_br/params.n_trials[phase]
                n_feat = d[lang]['feat']
                p_feat = n_feat/d[lang]['all']
                app.logger.info(f'    counts: total={n_br}; feat={n_feat}')
                app.logger.info(f'    actual probs: {p_br} {p_feat}')
        super()._make_profiles()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # The first task is created as an instance of the
        # Task class, and assigned to self.task;
        # the first argument is the participant's session ID,
        # and the second is the name of the template to display.
        # Subsequent tasks are added by chaining calls
        # to the .then() method.

        # .then() creates a new instance of the Task class
        # using the arguments it is given. Optionally, the first
        # argument may be a custom subclass of Task.
        self.task = Welcome(self, 'welcome')
        self.consent_task = self.task.then(Consent, 'consent')

    def create_tasks(self):
        if self.profile.cond.mode == 'implicit':
            instruct_train = 'instruct_listen'
        else:
            instruct_train = 'instruct_twoafc'
        testing_tasks = self.profile.testing_tasks()
        # Enable main section timeout by setting 'timeout_secs'
        # keyword argument of first task
        testing_tasks[0].kwargs['timeout_secs'] = params.timeout_secs

        (self.consent_task
         .then(Soundcheck)

         # 'qnaire' template receives 'questions' variable containing
         # questionnaire questions
         .then('qnaire', {'questions': params.qnaire_quests})

         .then(instruct_train)
         .then_all(self.profile.training_tasks())
         .then('instruct_test')
         .then_all(testing_tasks)

         .then('exit_qnaire', {'questions': params.exit_qnaire_quests},
         # Disable main section timeout by setting 'timeout_secs'
         # keyword argument of task to a negative value
               timeout_secs=-1)
         .then(Thankyou))
