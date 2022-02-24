odoo.define('assignment.bold', function (require) {
    "use strict";
    // import packages
    var basic_fields = require('web.basic_fields');
    var registry = require('web.field_registry');

    // widget implementation
    var BoldWidget = basic_fields.FieldChar.extend({
        _renderReadonly: function () {
            this._super();
            var old_html_render = this.$el.html();
            var new_html_render = '<b>' + old_html_render + '</b>'
            this.$el.html(new_html_render);
        },
    });

    var ItalicWidget = basic_fields.FieldChar.extend({
        _renderReadonly: function () {
            this._super();
            var old_html_render = this.$el.html();
            var new_html_render = '<i>' + old_html_render + '</i>'
            this.$el.html(new_html_render);
        },
    });
    registry.add('bold', BoldWidget); // add our "bold" widget to the widget registry
    registry.add('italic', ItalicWidget);
});