
import { Task, FSA } from '/survey/js/task.js';
import { elts, aPlay } from '/survey/js/util.js';


const dom = elts(
    'play-btn', 'play-btn-wrapper', 'play-btn-label',
    'images-wrapper', 'flag-img1', 'flag-img2',
    'feedback-wrapper',
    'feedback-incorrect', 'feedback-correct');


class States {

    constructor(task) {
        this.task = task;
        this.transits = {
            q0: {sound_ended: 'q1'},
            q1: {img_clicked: 'q2'}
        };
    }

    q0() {
        this.task.disableNext();
        dom['play-btn'].disabled = false;
        this.task.guide(dom['play-btn']);
    }

    // sound (city name) has ended
    q1() {
        this.task.guide(dom['images-wrapper']);
        this.task.imgClickEnabled = true;
    }

    // image has been clicked
    async q2() {
        this.task.imgClickEnabled = false;
        dom['play-btn'].disabled = true;
        if (this.task.vars['fback']) {
            const feedback = await this.task.api(
                'get_feedback', this.task.response);
            if (feedback) {
                dom['feedback-correct'].classList.remove('hidden');
                await aPlay(this.task.correct);
            } else {
                dom['feedback-incorrect'].classList.remove('hidden');
                await aPlay(this.task.incorrect);
            }
            //this.task.playerShowProgress = false;
            //await aPlay(this.task.player);
        }
        this.task.enableNext()
    }
}


class BrnTask extends Task {

    constructor() {
        super();

        dom['flag-img1'].addEventListener('click', () => {
            if (this.imgClickEnabled) {
                this.setResponse(this.aFlag);
                dom['flag-img2'].classList.remove('selected');
                dom['flag-img1'].classList.add('selected');
                this.fsa.event('img_clicked');
            }
        });
        dom['flag-img2'].addEventListener('click', () => {
            if (this.imgClickEnabled) {
                this.setResponse(this.bFlag);
                dom['flag-img1'].classList.remove('selected');
                dom['flag-img2'].classList.add('selected');
                this.fsa.event('img_clicked');
            }
        });

        dom['play-btn'].addEventListener('click', () => this.player.play());

        this.guide(dom['play-btn-wrapper']);
    }

    async reset() {
        await super.reset();
        this.imgClickEnabled = false;
        this.playerShowProgress = true;
        this.aFlag = this.vars['a_flag'];
        this.bFlag = this.aFlag === 'star' ? 'crown' : 'star';
        const dir = this.vars['exp_app_img'];
        dom['flag-img1'].src = `${dir}/${this.aFlag}.jpg`;
        dom['flag-img2'].src = `${dir}/${this.bFlag}.jpg`;
        this.clearImgSel();
        // hide correct/incorrect text
        dom['feedback-correct'].classList.add('hidden');
        dom['feedback-incorrect'].classList.add('hidden');
        const states = new States(this);
        this.fsa = new FSA(states);
        this.fsa.enter('q0');
        this.player = this.initPlayer(
            this.vars['sound'],
            () => this.fsa.event('sound_ended'));
        if (this.vars['fback']) {
            this.correct = this.loadSound('_correct');
            this.incorrect = this.loadSound('_incorrect');
        }
    }

    clearImgSel() {
        dom['flag-img1'].classList.remove('selected');
        dom['flag-img2'].classList.remove('selected');
    }

    initPlayer(sound, onended) {
        const player = this.loadSound(sound);
        dom['play-btn-label'].textContent = 'Play';
        player.addEventListener('timeupdate', () => {
            if (this.playerShowProgress) {
                const pct = 100 * player.currentTime / player.duration;
                // default button background is set in the stylesheet
                dom['play-btn'].style.background =
                  `linear-gradient(
                     to right,
                     lightgreen ${pct}%,
                     #e1e1e1 ${pct + 1}%, #e1e1e1)`;
            }
        });
        player.addEventListener('play', () => {
            dom['play-btn'].disabled = true;
        });
        player.addEventListener('ended', () => {
            dom['play-btn'].style.background = null; // '#e1e1e1'
            dom['play-btn'].disabled = false;
            dom['play-btn-label'].textContent = 'Play Again';
            if (onended) {
                onended();
            }
        });
        player.autoplay = true;
        return player;
    }

}

export { BrnTask as taskClass };
