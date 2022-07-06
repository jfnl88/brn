
import { Task } from '/expert/js/task.js';

class TYTask extends Task {
    constructor() {
        super();
        this.disableNext();
    }
}

export { TYTask as taskClass };
