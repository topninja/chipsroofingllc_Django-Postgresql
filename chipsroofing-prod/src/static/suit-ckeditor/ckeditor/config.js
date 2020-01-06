/**
 * @license Copyright (c) 2003-2013, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.html or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function(config) {
    // Define changes to default configuration here. For example:
    config.linkShowAdvancedTab = false;
    config.linkShowTargetTab = false;
    config.dataIndentationChars = '  ';
    config.tabSpaces = 2;
    config.extraAllowedContent = '*(*);img[*]';

    config.format_tags = "p;h2;h3";

    config.plugins = "basicstyles,contextmenu,dialog,dialogadvtab,elementspath," +
        "enterkey,entities,format,htmlwriter,indent,justify,pastefromword,pastetext," +
        "list,link,removeformat,sourcearea,specialchar,stylescombo,tab,toolbar,undo,wysiwygarea,blockquote";

    config.forcePasteAsPlainText = true;
    config.autoGrow_maxHeight = 540;
    config.dialog_noConfirmCancel = true;

    CKEDITOR.on('instanceReady', function(ev) {
        var blockTags = ['div', 'p', 'pre', 'ul', 'ol', 'li'];
        var rules = {
            indent: true,
            breakBeforeOpen: false,
            breakAfterOpen: true,
            breakBeforeClose: true,
            breakAfterClose: true
        };

        for (var i = 0; i < blockTags.length; i++) {
            ev.editor.dataProcessor.writer.setRules(blockTags[i], rules);
        }

        ev.editor.dataProcessor.writer.setRules('img', {
            indent: true,
            breakBeforeOpen: true,
            breakAfterOpen: true,
            breakBeforeClose: true,
            breakAfterClose: true
        });

        ev.editor.dataProcessor.writer.setRules('a', {
            indent: true
        });

        ev.editor.dataProcessor.writer.setRules('span', {
            indent: true,
            breakBeforeOpen: true,
            breakAfterOpen: false,
            breakBeforeClose: false,
            breakAfterClose: true
        });
    });
};

CKEDITOR.stylesSet.add('default', [
    // Block Styles
    {name: 'Default', element: ['p', 'h2', 'h3', 'h4'], attributes: {'class': ' '}},
    {name: 'No margin', element: ['p', 'h2', 'h3', 'h4'], attributes: {'class': 'no-margin'}},
    {name: 'Two columns', element: ['div', 'ol', 'ul'], attributes: {'class': 'two-columns'}},
    {name: 'Block quote', element: ['blockquote'], attributes: {'class': 'quote'}}
]);


// Утилиты
CKEDITOR.utils = {
    getAllowedStyles: function(editor, tagName) {
        var result = [];
        editor.getStylesSet(function(styleSet) {
            if (styleSet) {
                for (var i = 0; i < styleSet.length; i++) {
                    var isAllowed = true;
                    var style = styleSet[i];

                    if (tagName) {
                        var allowedTags = $.isArray(style.element) ? style.element : [style.element];
                        isAllowed = isAllowed && allowedTags.map(function(item) {
                                return item.toLowerCase()
                            }).indexOf(tagName.toLowerCase()) >= 0;
                        if (!isAllowed) continue;
                    }

                    result.push(style);
                }
            }
        });
        return result;
    },
    getActiveStyle: function(editor, element) {
        var result;
        editor.getStylesSet(function(styleSet) {
            if (!styleSet) return;
            for (var i = 0; i < styleSet.length; i++) {
                var isAllowed = true;
                var style = $.extend(true, {}, styleSet[i]);

                // проверка тэга
                var currentTag = element.$.tagName.toLowerCase();
                if (style.element) {
                    var allowedTags = $.isArray(style.element) ? style.element : [style.element];
                    isAllowed = isAllowed && allowedTags.map(function(item) {
                            return item.toLowerCase()
                        }).indexOf(currentTag) >= 0;
                    if (!isAllowed) continue;
                }
                style.element = currentTag;

                // проверка класса
                if (style.attributes && style.attributes.class) {
                    isAllowed = isAllowed && element.hasClass(style.attributes.class);
                    if (!isAllowed) continue;
                    delete style.attributes.class;
                }

                // проверка стилей
                var styleObj = new CKEDITOR.style(style);
                isAllowed = isAllowed && styleObj.checkElementMatch(element);
                if (isAllowed) {
                    result = style;
                    return false;
                }
            }
        });
        return result;
    }
};