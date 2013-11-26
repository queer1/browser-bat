define(function(require) {
    'use strict';

    return Backbone.View.extend({
        el: '#downloads',
        
        initialize: function() {
            this.downloads = DATA.downloads;
        },

        events: {
            'keydown input[type=text]': 'search'
        },

        search: function() {
            var search = this.$('input[type=text]').val();
            var results = [];
            this.downloads.forEach(function(download) {
                if (download.url.indexOf(search) > -1 || download.path.indexOf(search) > -1) {
                    results.push(download);
                }
            });
            
            this.$('#dl-list').html('');
            _.forEach(results, function(result) {
                var file = result.path.replace(/^.*[\\\/]/, '')
                this.$('#dl-list').append('<button class="btn btn-default">' + file + '</button>');
            }, this);
        }
    });
});