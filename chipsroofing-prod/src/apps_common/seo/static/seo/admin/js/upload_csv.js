(function($) {

    var initButton = function($button) {
        var $dialog;
        Uploader($button, {
            url: $button.attr('href'),
            fileName: 'csv',
            multiple: false,
            max_size: '40mb',
            mime_types: [
                {title: "CSV files", extensions: "csv"}
            ],
            prevent_duplicates: false,
            onFileAdded: function() {
                $dialog = $('<h3>').text(
                    gettext('Please, wait...')
                ).dialog({
                    dialogClass: 'upload-csv-dialog',
                    modal: true,
                    draggable: false,
                    resizable: false,
                    closeOnEscape: false,
                    open: function(event, ui) {
                        $(".ui-dialog-titlebar-close", ui.dialog | ui).hide();
                    }
                });
            },
            onFileUploaded: function(file, response) {
                var is_reload = $button.data('reload') || !response.redirect;
                if (is_reload) {
                    location.reload(true);
                } else {
                    location.href = response.redirect;
                }
            }
        });
    };

    $(document).ready(function() {
        $('.upload-csv').each(function() {
            initButton($(this));
        });
    });

})(jQuery);
