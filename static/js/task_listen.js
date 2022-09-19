
import { Task, FSA } from '/survey/js/task.js';
import { elts, aPlay, aSleep } from '/survey/js/util.js'


const dom = elts('play-btn-wrapper', 'transport-img1', 'transport-img2');
dom['play-btn'] = dom['play-btn-wrapper'].querySelector('.play-btn');

class ListenTask extends Task {

    constructor() {
        super();
        dom['play-btn'].addEventListener('click', () => {
            this.player.play();
        });
    }

    async reset() {
        await super.reset();
        const transportSound = this.loadSound(`_${this.vars['transport']}`);
        const transports = [
            this.vars['a_transport'],
            this.vars['a_transport'] === 'train' ? 'boat' : 'train'
        ];
        const images = [dom['transport-img1'], dom['transport-img2']];
        const dir = this.vars['exp_app_img'];
        images.forEach((img, i) => {
            img.src = `${dir}/${transports[i]}.jpg`;
            img.classList.remove('selected');
        });

        this.disableNext()
        dom['play-btn'].disabled = false;
        this.guide(dom['play-btn']);

        this.player = this.initPlayer(this.vars['sound'], async () => {
            await aSleep(1000);
            const i = transports.indexOf(this.vars['transport']);
            images[i].classList.add('selected');
            images[1 - i].classList.remove('selected');
            await aPlay(transportSound);
            this.enableNext();
        });
        this.player.addEventListener('play', () => {
            dom['play-btn'].disabled = true;
            this.guide(null);
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
        player.autoplay = true;
        return player;
    }


}

export { ListenTask as taskClass };

