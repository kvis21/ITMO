class App {
    constructor() {
        this.graph = new GraphManager();
        this.init();
    }
    
    init() {
        this.graph.init(this);
    }
    
    updateGraph() {
        this.graph.update();
    }
}

document.addEventListener('DOMContentLoaded', function() {
    window.app = new App();
});

function updateGraph() {
    if (window.app) {
        window.app.updateGraph();
    } else {
        console.warn('App not initialized');
    }
}