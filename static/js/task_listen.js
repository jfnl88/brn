
import { Task, FSA } from '/expert/js/task.js';
import { elts, aPlay, aSleep } from '/expert/js/util.js'


const dom = elts('play-btn-wrapper');
dom['play-btn'] = dom['play-btn-wrapper'].querySelector('.play-btn');

class ListenTask extends Task {

    constructor() {
        super();
        dom['play-btn'] .addEventListener('click', () => this.player.play());
    }

    async reset() {
        await super.reset();
        const transportSound = this.loadSound(`_${this.vars['transport']}`);

        this.disableNext()
        this.guide(dom['play-btn']);

        this.player = this.initPlayer(this.vars['sound'], async () => {
            await aSleep(1000);
            await aPlay(transportSound);
            this.enableNext();
        });

    }

    initPlayer(sound, onended) {
        const player = this.loadSound(sound);
        player.addEventListener('timeupdate', () => {
            const pct = 100*player.currentTime/player.duration;
            // default button background is set in the stylesheet
            dom['play-btn'].style.background =
                `linear-gradient(
                   to right,
                   lightgreen ${pct}%,
                   #e1e1e1 ${pct + 1}%, #e1e1e1)`;
        });
        player.addEventListener('ended', () => {
            dom['play-btn'].style.background = null; //'#e1e1e1'
            if (onended) {
                onended();
            }
        });
        //player.autoplay = true
        return player;
    }


}

export { ListenTask as taskClass };

