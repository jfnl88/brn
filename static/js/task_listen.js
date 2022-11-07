
import { Task } from '/survey/js/task.js';
import { elts } from '/survey/js/util.js'


const dom = elts('play-btn-wrapper', 'country-flag-wrapper', 'play-btn-label');
dom['play-btn'] = dom['play-btn-wrapper'].querySelector('.play-btn');

class ListenTask extends Task {

    constructor() {
        super();
        dom['play-btn'].addEventListener('click', () => this.player.play());
    }

    async reset() {
        await super.reset();
        const flag = this.vars['flag'];
        dom['country-flag-wrapper'].replaceChildren();
        const img = document.createElement('img');
        const dir = this.vars['exp_app_img'];
        img.src = `${dir}/${flag}.jpg`;
        dom['country-flag-wrapper'].append(img);

        this.disableNext()
        dom['play-btn'].disabled = false;
        this.guide(dom['play-btn']);

        this.player = this.initPlayer(this.vars['sound'], () =>
            this.enableNext());
    }

    initPlayer(sound, onended) {
        const player = this.loadSound(sound);
        dom['play-btn-label'].textContent = 'Play';
        player.addEventListener('timeupdate', () => {
            const pct = 100*player.currentTime/player.duration;
            // default button background is set in the stylesheet
            dom['play-btn'].style.background =
                `linear-gradient(
                   to right,
                   lightgreen ${pct}%,
                   #e1e1e1 ${pct + 1}%, #e1e1e1)`;
        });
        player.addEventListener('play', () => {
            dom['play-btn'].disabled = true;
            dom['play-btn-label'].textContent = 'Playing';
        });
        player.addEventListener('ended', () => {
            dom['play-btn'].style.background = null; //'#e1e1e1'
            dom['play-btn'].disabled = false;
            dom['play-btn-label'].textContent = 'Play Again'
            if (onended) {
                onended();
            }
        });
        player.autoplay = true;
        return player;
    }

}

export { ListenTask as taskClass };

