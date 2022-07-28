
import { Task } from '/survey/js/task.js';

class TYTask extends Task {
    constructor() {
        super();
        this.disableNext();
    }
}

export { TYTask as taskClass };
