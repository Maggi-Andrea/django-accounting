$(function() {
    $('.line-formset-form').formset({
        prefix: 'lines',
        addText: 'add another line',
        deleteText: 'remove line',
        addCssClass: 'btn btn-primary btn-sm',
        deleteCssClass: 'btn btn-danger btn-sm',
        formCssClass: 'dynamic-form-lines',
        added: function($row) {
            // update line title
            var index = $row.index('.line-formset-form') + 1;
            $row.find('.counter').text(index);
        }
    });
});

$(function() {
    $('.contribution-formset-form').formset({
        prefix: 'contributions',
        addText: 'add another contribution',
        deleteText: 'remove contribution',
        addCssClass: 'btn btn-primary btn-sm',
        deleteCssClass: 'btn btn-danger btn-sm',
        formCssClass: 'dynamic-form-contributions',
        added: function($row) {
            // update line title
            var index = $row.index('.contribution-formset-form') + 1;
            $row.find('.counter').text(index);
        }
    });
});

