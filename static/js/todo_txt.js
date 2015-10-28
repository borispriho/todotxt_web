var TodoTxtApp = new Backbone.Marionette.Application();

TodoTxtApp.addRegions({
    contentRegion: '#content'
});

TodoTxtApp.TodoModel = Backbone.Model.extend({
    defaults: {
        line: '',
        done: false
    },
    toJSON: function() {
        var json = Backbone.Model.prototype.toJSON.apply(this, arguments);
        json.cid = this.cid;
        return json;
    }
});

TodoTxtApp.TodoCollection = Backbone.Collection.extend({
    url: '/todo/',
    model: TodoTxtApp.TodoModel
});

TodoTxtApp.TodoItemView = Backbone.Marionette.ItemView.extend({
    template: '#todo-item',
    model: TodoTxtApp.TodoModel,
    tagName: 'tr',
    className: 'todotxt__item',
    ui: {
        checkbox: '.js-checkbox'
    },
    events: {
        'change .js-checkbox': "recordTicked"
    },
    recordTicked: function(e) {
        var done = this.ui.checkbox.hasClass('is-checked');
        this.model.set('done', done);
        this.$el.toggleClass('js-done');
    },
    onRender: function() {
        componentHandler.upgradeElements(this.el);
        if (this.model.get('done')) {
            this.$el.addClass('js-done');
        }
    }
});

TodoTxtApp.TodoCompositeView = Backbone.Marionette.CompositeView.extend({
    template: '#todo-list',
    tagName: 'table',
    collection: TodoTxtApp.TodoCollection,
    childView: TodoTxtApp.TodoItemView,
    childViewContainer: 'tbody',
    className: "todotxt__list mdl-data-table mdl-js-data-table",
    initialize: function(options) {
        var self = this;
        TodoTxtApp.vent.on('todo:save', function(e) {
            self.saveTodo(e);
        });
        TodoTxtApp.vent.on('todo:add', function(e) {
            self.addTask(e);
        });
    },
    saveTodo: function(e) {
        var self = this;
        self.collection.sync('create', self.collection);
    },
    addTask: function(e) {
        var self = this;
        console.log(self);
    }
});

TodoTxtApp.addInitializer(function() {
    var self = this;
    var todo_collection = new TodoTxtApp.TodoCollection();
    todo_collection.fetch();
    var todo_view = new TodoTxtApp.TodoCompositeView({collection: todo_collection});
    this.contentRegion.show(todo_view);
    $('body').on('click', '.js-add-button', function(e) {
        self.vent.trigger('todo:add', e);
    });
    $('body').on('click', '.js-save-button', function(e) {
        self.vent.trigger('todo:save', e);
    });
});

$(function() {
    TodoTxtApp.start();
});
