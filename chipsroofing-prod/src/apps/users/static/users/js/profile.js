(function($) {

    /** @namespace window.js_storage.avatar_upload */
    /** @namespace window.js_storage.avatar_crop */
    /** @namespace window.js_storage.avatar_delete */

    // Обновление аватарок на странице
    var change_avatar = function(response) {
        // Обновление кнопок
        $.loadImageDeferred(response.normal_avatar).done(function() {
            $('#profile-avatar').replaceWith(response.profile_avatar_html);
            initUploader();
        });

        $(document).trigger('change_avatar.users', response);
    };

    // Инициализация загрузчика аватарки
    var initUploader = function() {
        return Uploader('#profile-avatar', {
            url: window.js_storage.avatar_upload,
            buttonSelector: '#upload-avatar',
            multiple: false,
            resize: {
                width: 1024,
                height: 1024
            },
            max_size: '12mb',

            onFileUploaded: function(file, json_response) {
                if (json_response) {
                    change_avatar(json_response);
                }
            },
            onFileUploadError: function(file, error, json_response) {
                if (json_response && json_response.message) {
                    alert(json_response.message)
                }
            }
        });
    };


    $(document).ready(function() {
        var $profile = $('#profile');

        // Обрезка аватара
        CropDialog($profile, {
            eventTypes: 'click.cropdialog',
            buttonSelector: '#crop-avatar',
            dialogOptions: {
                classes: 'popup-crop-avatar'
            },

            getImage: function($button) {
                return $button.data('source');
            },
            getMinSize: function($button) {
                return this.formatSize($button.data('min_dimensions'));
            },
            getAspects: function($button) {
                return this.formatAspects($button.data('aspect'));
            },
            getCropCoords: function($button) {
                return this.formatCoords($button.data('crop'));
            },
            onCrop: function($button, coords) {
                var coords_str = coords.join(':');
                $.ajax({
                    url: window.js_storage.avatar_crop,
                    type: 'POST',
                    data: {
                        coords: coords_str
                    },
                    dataType: 'json',
                    success: change_avatar,
                    error: $.parseError()
                });
                $button.data('crop', coords_str);
            }
        });

        // Клик на кнопку удаления аватара
        $profile.on('click', '.delete-avatar', function() {
            if (!confirm(gettext('Are you sure that you want to delete this avatar?'))) {
                return false;
            }

            $.ajax({
                url: window.js_storage.avatar_delete,
                type: 'POST',
                dataType: 'json',
                success: change_avatar,
                error: $.parseError()
            });

            return false;
        });

        // Инициализация загрузчика аватарки
        initUploader();
    });

})(jQuery);
