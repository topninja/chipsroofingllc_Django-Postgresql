(function($) {
    'use strict';

    /*
        Загрузчик асинхронных блоков.

        Требует:
            jquery.utils.js

        Для отлова события загрузки всех блоков можно
        использовать событие "loaded.ajax_blocks":
            $(document).on('loaded.ajax_blocks', function() {

            })
     */

    /** @namespace window.js_storage.ajax_attached_block */

    var keyMap = {};
    var UNDEFINED_KEY = 'undefined';

    /*
        Анализ заглушки асинхронно подгружаемого блока
     */
    var registerBlocksPlaceholder = function() {
        var data = $(this).data();
        var block_id = parseInt(data.id);
        if (!block_id) return;

        var map_id;
        var cid = parseInt(data.cid);
        var oid = parseInt(data.oid);
        if (!isNaN(cid) && !isNaN(oid)) {
            map_id = cid + '_' + oid;
        } else {
            map_id = UNDEFINED_KEY;
        }

        if (map_id in keyMap) {
            keyMap[map_id].push(block_id);
        } else {
            keyMap[map_id] = [block_id];
        }
    };

    var requestBlocks = function(cid, oid, block_ids) {
        return $.ajax({
            url: window.js_storage.ajax_attached_block,
            type: 'GET',
            data: {
                cid: cid,
                oid: oid,
                block_ids: block_ids.join(',')
            },
            dataType: 'json',
            success: function(response) {
                if ((cid !== undefined) && (oid !== undefined)) {
                    var $blocks = $('.async-block[data-cid="' + cid + '"][data-oid="' + oid + '"]');
                } else {
                    $blocks = $('.async-block[data-cid=""][data-oid=""]');
                }

                for (var block_id in response) {
                    if (response.hasOwnProperty(block_id)) {
                        $blocks.filter('[data-id="' + block_id + '"]').replaceWith(response[block_id]);
                    }
                }
            }
        });
    };

    $(document).ready(function() {
        var $blocks = $('.async-block');

        // собираем все ID блоков, сгруппированных по ContentType и ObjectID
        $blocks.each(registerBlocksPlaceholder);
        if ($.isEmptyObject(keyMap)) {
            // callback event
            $(document).trigger('loaded.ajax_blocks');
            return;
        }

        // отправляем запросы на получение блоков
        var requests = [];
        for (var map_id in keyMap) {
            if (keyMap.hasOwnProperty(map_id)) {
                var cid, oid;
                if (map_id === UNDEFINED_KEY) {
                    cid = oid = undefined;
                } else {
                    var cid_oid = map_id.split('_');
                    cid = cid_oid[0];
                    oid = cid_oid[1];
                }

                requests.push(requestBlocks(cid, oid, keyMap[map_id]));
            }
        }

        var requestCount = requests.length;
        var requestsDone = 0;
        var resolveOrReject = function() {
            requestsDone++;
            if (requestsDone === requestCount) {
                // callback event
                $(document).trigger('loaded.ajax_blocks');
            }
        };

        for (var i=0, l=requestCount; i<l; i++) {
            var request = requests[i];
            request.always(resolveOrReject);
        }
    });

})(jQuery);
