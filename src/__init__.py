
# Import built-in classes
from expert import Experiment
from expert.tasks import Task, Welcome, Consent, Soundcheck, Thankyou

# Import local modules
from . import params

from .stim import Lang

# Your experiment class must be a subclass of expert.experiment.Experiment,
# but can have any name

class Brn(Experiment):

    # Title for experiment browser window
    window_title = 'Language experiment'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Print out actual probabilities, which may differ
        # slightly from specified probabilities
        # for phase in 'train', 'test':
        #     d = params.stim_counts[phase]
        #     for lang in Lang:
        #         pr_br = d[lang]['all']/params.n_trials[phase]
        #         pr_feat = d[lang]['feat']/d[lang]['all']
        #         print(f'actual {phase} probs ({lang}): {pr_br} {pr_feat}')

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
        training_task_name = self.profile.training_task_name()
        testing_task_name = self.profile.testing_task_name()
        testing_tasks = self.profile.testing_tasks()
        # Enable main section timeout by setting 'timeout_secs'
        # keyword argument of first task
        testing_tasks[0].kwargs['timeout_secs'] = params.timeout_secs

        (self.consent_task
         #.then(Soundcheck)

         # 'qnaire' template receives 'questions' variable containing
         # questionnaire questions
         #.then('qnaire', {'questions': params.qnaire_quests})

         .then(f'instruct_{training_task_name.lower()}')
         # Insert sequence of tasks;
         # delete [:4] to add all tasks instead of just first 4
         .then_all(self.profile.training_tasks()[:3])
         .then(f'instruct_{testing_task_name.lower()}')
         .then_all(testing_tasks[:3])

         #.then('exit_qnaire', {'questions': params.exit_qnaire_quests},
         # Disable main section timeout by setting 'timeout_secs'
         # keyword argument of task to a negative value
         #      timeout_secs=-1)
         .then(Thankyou))
