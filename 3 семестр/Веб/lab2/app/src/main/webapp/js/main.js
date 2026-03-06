class Application {
    constructor() {
        this.init();
    }

    init() {
        try {
            this.formManager = new FormManager();
            
            this.graphManager = new GraphManager('graphCanvas');
            
            window.formManager = this.formManager;
            window.graphManager = this.graphManager;
            
            console.log('Application initialized successfully');

            
        } catch (error) {
            console.error('Error initializing application:', error);
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    new Application();
});