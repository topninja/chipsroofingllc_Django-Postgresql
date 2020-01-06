(function($) {

    var $form;

    $(document).ready(function() {
        $form = $('#sendtest-dialog').find('form').detach();
    });

    $(document).on('click', '.sendtest-btn', function() {
        if (!$form.length) {
            return false;
        }

        var $dialog_form = $form.clone();
        $dialog_form.get(0).reset();
        $dialog_form.find('[name="receiver"]').val($.cookie('last_receiver') || '');
        $dialog_form.attr('id', 'sendtest-form');
        $dialog_form.on('submit', function() {
            var $form = $(this);
            var dialog = $form.dialog('instance');
            if (dialog.uiDialog.hasClass('preloader')) {
                return false
            }

            $.ajax({
                url: $form.attr('action'),
                type: $form.attr('method'),
                data: $form.serialize(),
                beforeSend: function() {
                    dialog.uiDialog.addClass('preloader');
                },
                success: function() {
                    dialog.close();
                },
                error: function(xhr) {
                    if (xhr.statusText === 'abort') {
                        return
                    }

                    if (xhr.responseText) {
                        try {
                            var response = JSON.parse(xhr.responseText + "");
                            var errors = [];
                            for (var field in response.errors) {
                                if (response.errors.hasOwnProperty(field)) {
                                    errors.push(response.errors[field][0])
                                }
                            }

                            alert(errors.join('\n'));
                        } catch (err) {
                            // ответ - не JSON
                            alert(gettext('Undefined server error'))
                        }
                    } else {
                        alert(xhr.responseText);
                    }
                },
                complete: function() {
                    dialog.uiDialog.removeClass('preloader');
                }
            });

            return false
        });

        $dialog_form.dialog({
            dialogClass: "send-email-dialog",
            title: gettext('Send test e-mail'),
            minWidth: 200,
            closeText: '',
            modal: true,
            resizable: false,
            show: {
                effect: "fadeIn",
                duration: 100
            },
            hide: {
                effect: "fadeOut",
                duration: 100
            },
            close: function() {
                $(this).dialog('destroy');
            },
            buttons: [
                {
                    text: gettext("Cancel"),
                    "class": 'btn',
                    icons: {
                        primary: "ui-icon-cancel"
                    },
                    click: function() {
                        $(this).dialog("close");
                    }
                },
                {
                    text: gettext("Ok"),
                    "class": 'btn btn-info',
                    icons: {
                        primary: "ui-icon-check"
                    },
                    click: function() {
                        $(this).submit();
                    }
                }
            ]
        });

        return false;
    });

})(jQuery);