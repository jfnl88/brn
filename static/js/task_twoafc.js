
import { Task, FSA } from '/expert/js/task.js';
import { elts, aPlay } from '/expert/js/util.js';


const dom = elts(
    'play-btn', 'play-btn-wrapper',
    'images-wrapper', 'transport-img1', 'transport-img2',
    'feedback-btn', 'feedback-btn-wrapper',
    'feedback-incorrect', 'feedback-correct');


class States {

    constructor(task) {
        this.task = task;
        this.transits = {
            q0: {sound_ended: 'q1'},
            q1: {img_clicked: 'q2'},
            q2: {feedback_clicked: 'q3'}
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

    // selection has been made
    q2() {
        if (this.task.vars['fback']) {
            this.task.guide(dom['feedback-btn']);
            dom['feedback-btn'].disabled = false;
        } else {
            this.task.enableNext();
        }
    }

    // feedback button has been clicked
    async q3() {
        this.task.imgClickEnabled = false;
        dom['play-btn'].disabled = true;
        dom['feedback-btn'].disabled = true;
        const feedback = await this.task.api(
            'get_feedback', this.task.response);
        dom['feedback-btn'].style.display = 'none';
        if (feedback) {
            dom['feedback-correct'].style.display = 'block';
            await aPlay(this.task.correct);
        } else {
            dom['feedback-incorrect'].style.display = 'block';
            await aPlay(this.task.incorrect);
        }
        this.task.playerShowProgress = false;
        await aPlay(this.task.player);
        if (feedback) {
            await aPlay(this.task.transportSounds[this.task.response]);
        } else {
            const corrAns = this.task.response === 'train' ? 'boat' : 'train';
            await aPlay(this.task.transportSounds[corrAns]);
        }
        this.task.enableNext()
    }
}


class BrnTask extends Task {

    constructor() {
        super();

        dom['transport-img1'].addEventListener('click', () => {
            if (this.imgClickEnabled) {
                this.setResponse(this.aTransport);
                dom['transport-img2'].classList.remove('selected');
                dom['transport-img1'].classList.add('selected');
                this.fsa.event('img_clicked');
            }
        });
        dom['transport-img2'].addEventListener('click', () => {
            if (this.imgClickEnabled) {
                this.setResponse(this.bTransport);
                dom['transport-img1'].classList.remove('selected');
                dom['transport-img2'].classList.add('selected');
                this.fsa.event('img_clicked');
            }
        });

        dom['play-btn'].addEventListener('click', () => this.player.play());
        dom['feedback-btn'].addEventListener(
            'click', () => this.fsa.event('feedback_clicked'));

        this.guide(dom['play-btn-wrapper']);
    }

    async reset() {
        await super.reset();
        this.imgClickEnabled = false;
        this.playerShowProgress = true;
        this.aTransport = this.vars['a_transport'];
        this.bTransport = this.aTransport === 'train' ? 'boat' : 'train';
        dom['transport-img1'].src = `/expert/brn/img/${this.aTransport}.jpg`;
        dom['transport-img2'].src = `/expert/brn/img/${this.bTransport}.jpg`;
        this.clearImgSel();
        // show feedback button and hide correct/incorrect text
        // (wrapper for both is hidden by default)
        dom['feedback-btn'].style.display = null;
        dom['feedback-correct'].style.display = null;
        dom['feedback-incorrect'].style.display = null;
        const states = new States(this);
        this.fsa = new FSA(states);
        this.fsa.enter('q0');
        this.player = this.initPlayer(this.vars['sound']);
        if (this.vars['fback']) {
            dom['feedback-btn'].disabled = true;
            this.correct = this.loadSound('_correct');
            this.incorrect = this.loadSound('_incorrect');
            dom['feedback-btn-wrapper'].style.display = 'flex';
            this.transportSounds = {
                train: this.loadSound('_train'),
                boat: this.loadSound('_boat')
            };
        }
    }

    clearImgSel() {
        dom['transport-img1'].classList.remove('selected');
        dom['transport-img2'].classList.remove('selected');
    }

    initPlayer(sound) {
        const player = this.loadSound(sound);
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
        player.addEventListener('ended', () => {
            dom['play-btn'].style.background = null; // '#e1e1e1'
            // task.setResponse(idx)
            // playBtns.classList.add('selected')
            // playBtns[1 - idx].classList.remove('selected')
            this.fsa.event('sound_ended');
        });
        player.autoplay = true;
        return player;
    }

}

export { BrnTask as taskClass };
