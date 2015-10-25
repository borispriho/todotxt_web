var TodoTxtApp = new Backbone.Marionette.Application();

TodoTxtApp.addRegions({
    contentRegion: '#content'
});

TodoTxtApp.TodoModel = Backbone.Model.extend({
    defaults: {
        line: ''
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
    onRender: function() {
        componentHandler.upgradeElements(this.el);
    }
});

TodoTxtApp.TodoCompositeView = Backbone.Marionette.CompositeView.extend({
    template: '#todo-list',
    tagName: 'table',
    collection: TodoTxtApp.TodoCollection,
    childView: TodoTxtApp.TodoItemView,
    childViewContainer: 'tbody',
    className: "todotxt__list mdl-data-table mdl-js-data-table"
});

TodoTxtApp.addInitializer(function() {
    var todo_collection = new TodoTxtApp.TodoCollection();
    todo_collection.fetch();
    var todo_view = new TodoTxtApp.TodoCompositeView({collection: todo_collection});
    this.contentRegion.show(todo_view);
});

$(function() {
    TodoTxtApp.start();
});
