(function($) {
    'use strict';

    /*
        Модуль для работы с inline-формами на клиенте.

        Требует:
            jquery.utils.js

        Параметры:
            prefix              - Django-префикс форм
            formsListSelector   - селектор контейнера, в который будут добавляться новые формы.
            formSelector        - селектор каждого блока формы в контейнере
            formTemplate        - селектор контейнера пустой формы

            showSpeed           - скорость показа новой формы при добавлении
            hideSpeed           - скорость скрытия формы при удалении

            canAddForm          - событие, вызываемое перед добавлением новой формы.
                                  Если вернёт false, форма не будет добавлена
            canDeleteForm       - событие, вызываемое перед удалением формы.
                                  Если вернёт false, форма не будет удалена

        События:
            // новая форма добавлена, но еще не видна (до анимации)
            before_add($form)

            // новая форма добавлена и видна (после анимации)
            after_add($form)

            // форма удалена, но еще видна (до анимации)
            before_delete($form)

            // форма удалена и не видна (после анимации)
            after_delete($form, removed_dom)

        Пример:
            HTML:
              <div id="formset">
                  {{ formset.management_form }}

                  <div class="forms">
                    {% for form in formset %}
                      <div class="form">
                        {{ form }}
                      </div>
                    {% endfor %}
                  </div>

                  <script type="text/template" class="form-template">
                     <div class="form">
                        {{ formset.empty_form }}
                     </div>
                  </script>
              </div>

            JS:
              fs = Formset('#formset', {
                  prefix: 'inlines'
              });

              // добавление формы
              var $form = fs.addForm();

              // удаление формы
              fs.deleteForm($form);
     */

    /*
        Замена "__prefix__" в форме на реальный индекс формы
     */
    var prefix_regexp = /__prefix__/i;
    var setElementIndex = function(element, index) {
        // label tag
        var for_value = element.getAttribute('for');
        if (for_value) {
            element.setAttribute('for', for_value.replace(prefix_regexp, index));
        }

        // ID attr
        if (element.id) {
            element.id = element.id.replace(prefix_regexp, index);
        }

        // Class attr
        if (element.className) {
            element.className = element.className.replace(prefix_regexp, index);
        }

        // name attr
        if (element.name) {
            element.name = element.name.replace(prefix_regexp, index);
        }
    };

    window.ManagementForm = Class(Object, function ManagementForm(cls, superclass) {
        cls.init = function(root, prefix) {
            this.$root = $(root).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            if (!prefix) {
                return this.raise('prefix required');
            }

            this.$total_forms = this.$root.find('#id_' + prefix + '-TOTAL_FORMS');
            this.$initial_forms = this.$root.find('#id_' + prefix + '-INITIAL_FORMS');
            this.$min_num_forms = this.$root.find('#id_' + prefix + '-MIN_NUM_FORMS');
            this.$max_num_forms = this.$root.find('#id_' + prefix + '-MAX_NUM_FORMS');

            if (!this.$total_forms.length) {
                return this.raise('not found TOTAL_FORMS field');
            }
            if (!this.$initial_forms.length) {
                return this.raise('not found INITIAL_FORMS field');
            }
            if (!this.$min_num_forms.length) {
                return this.raise('not found MIN_NUM_FORMS field');
            }
            if (!this.$max_num_forms.length) {
                return this.raise('not found MAX_NUM_FORMS field');
            }
        };

        cls.getTotalFormCount = function() {
            return parseInt(this.$total_forms.val()) || 0;
        };

        cls.getInitialFormCount = function() {
            return parseInt(this.$initial_forms.val()) || 0;
        };

        cls.getMinFormCount = function() {
            return parseInt(this.$min_num_forms.val()) || 0;
        };

        cls.getMaxFormCount = function() {
            return parseInt(this.$max_num_forms.val()) || 1000;
        };
    });

    window.Formset = Class(EventedObject, function Formset(cls, superclass) {
        cls.defaults = {
            prefix: '',
            formsListSelector: '.forms',
            formSelector: '.form',
            formTemplate: '.empty-form',
            showSpeed: 300,
            hideSpeed: 300,
            canAddForm: function() {
                return this.getFormCount() < this.management.getMaxFormCount();
            },
            canDeleteForm: function() {
                return this.getFormCount() > this.management.getMinFormCount()
            }
        };

        cls.DATA_KEY = 'formset';


        cls.init = function(root, options) {
            superclass.init.call(this);
            this.$root = $(root).first();
            if (!this.$root.length) {
                return this.raise('root element not found');
            }

            this.opts = $.extend({}, this.defaults, options);
            if (!this.opts.prefix) {
                return this.raise('prefix required');
            }

            // management form
            this.management = window.ManagementForm(this.$root, this.opts.prefix);
            if (!this.management) {
                return false;
            }

            // контейнер форм
            this.$formContainer = this.$root.find(this.opts.formsListSelector);
            if (!this.$formContainer.length) {
                return this.raise('forms container not found');
            }

            // шаблон форм
            this.$template = this.$root.find(this.opts.formTemplate);
            if (!this.$template.length) {
                return this.raise('form template not found');
            }

            // все формы
            var $forms = this.getForms();
            if ($forms.length !== this.management.getTotalFormCount()) {
                return this.raise('management TOTAL_FORMS is not equal to real form count');
            }

            // начальные формы
            this.$initial_forms = $forms.slice(0, this.management.getInitialFormCount());
            if (this.$initial_forms.length !== this.management.getInitialFormCount()) {
                return this.raise('management INITIAL_FORMS is not equal to real form count');
            }

            // отвязывание старого экземпляра
            var old_instance = this.$root.data(this.DATA_KEY);
            if (old_instance) {
                old_instance.destroy();
            }

            // индекс следующей добавляемой формы
            this._nextFormIndex = this.$initial_forms.length;

            this.$root.data(this.DATA_KEY, this);
        };

        /*
            Освобождение ресурсов
         */
        cls.destroy = function() {
            this.$root.removeData(this.DATA_KEY);
            superclass.destroy.call(this);
        };

        /*
            Получение всех форм
         */
        cls.getForms = function() {
            return this.$formContainer.find(this.opts.formSelector);
        };

        /*
            Получение поля удаления формы
         */
        cls.getDeleteField = function(form) {
            var $form = $(form).first();
            if (!$form.length) {
                this.error('form not found');
                return false;
            }

            var $field = $form.find('[name^="' + this.opts.prefix + '-"][name$="-DELETE"]');
            return $field.first();
        };

        /*
            Является ли форма начальной
         */
        cls.isInitial = function(form) {
            var $form = $(form).first();
            if (!$form.length) {
                this.error('form not found');
                return false;
            }

            return this.$initial_forms.toArray().indexOf($form.get(0)) >= 0;
        };

        /*
            Получение кол-ва активных форм
         */
        cls.getFormCount = function() {
            var that = this;
            var $forms = this.getForms();
            return $forms.filter(function(i, form) {
                var $df = that.getDeleteField($(form));
                if ($df.length) {
                    return !$df.prop('checked');
                } else {
                    // that.warn('"delete" field not found');
                    return true
                }
            }).length
        };

        /*
            Получение новой формы
         */
        cls.getEmptyForm = function() {
            var that = this;
            var $form = $(this.$template.html());
            $form.find('*').each(function() {
                setElementIndex(this, that._nextFormIndex);
            });
            this._nextFormIndex++;
            return $form;
        };


        /*
            Добавление новой формы.

            Возвращает jQuery-объект новой формы или false
         */
        cls.addForm = function() {
            if (this.opts.canAddForm.call(this) === false) {
                return false
            }

            var $form = this.getEmptyForm();
            $form.hide().appendTo(this.$formContainer);

            // увеличиваем TOTAL_FORMS
            var total_forms = this.management.getTotalFormCount();
            this.management.$total_forms.val(total_forms + 1);

            this.trigger('before_add', $form);

            // анимация показа
            var that = this;
            $form.slideDown({
                duration: this.opts.showSpeed,
                complete: function() {
                    that.trigger('after_add', $form);
                }
            });

            return $form;
        };

        /*
            Удаление формы. Устанавливает поле DELETE, если оно есть.

            Возвращает jQuery-объект удаленной формы или false
         */
        cls.deleteForm = function(form) {
            var $form = $(form).first();
            if (!$form.length) {
                this.error('form not found');
                return false
            }

            if (this.opts.canDeleteForm.call(this, $form) === false) {
                return false
            }

            var $df = this.getDeleteField($form);
            if ($df.length) {
                // форма уже удалена
                if ($df.prop('checked')) {
                    return $form;
                }

                $df.prop('checked', true);
            } else {
                // this.warn('"delete" field not found');
            }

            this.trigger('before_delete', $form);

            // анимация удаления
            var that = this;
            $form.slideUp({
                duration: that.opts.hideSpeed,
                complete: function() {
                    var remove_dom = !that.isInitial($form);
                    if (remove_dom) {
                        $form.remove();

                        // уменьшаем TOTAL_FORMS
                        var total_forms = that.management.getTotalFormCount();
                        that.management.$total_forms.val(total_forms - 1);
                    }

                    that.trigger('after_delete', $form, remove_dom);
                }
            });

            return $form;
        };
    });

})(jQuery);
