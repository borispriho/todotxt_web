var TodoTxtApp = new Backbone.Marionette.Application();

TodoTxtApp.addRegions({
    contentRegion: '#content'
});

TodoTxtApp.TodoModel = Backbone.Model.extend({
    defaults: {
        text: ''
    }
});

TodoTxtApp.TodoCollection = Backbone.Collection.extend({
    url: '/todo/',
    model: TodoTxtApp.TodoModel
});

TodoTxtApp.TodoItemView = Backbone.Marionette.ItemView.extend({
    template: '#todo-item',
    model: TodoTxtApp.TodoModel,
    tagName: 'tr'
});

TodoTxtApp.TodoCompositeView = Backbone.Marionette.CompositeView.extend({
    template: '#todo-list',
    tagName: 'table',
    collection: TodoTxtApp.TodoCollection,
    childView: TodoTxtApp.TodoItemView,
    childViewContainer: 'tbody',
    className: "todotxt__list mdl-data-table mdl-js-data-table mdl-data-table--selectable"
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
