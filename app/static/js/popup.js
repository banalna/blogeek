$(function() {
    var timer = null;
    var xhr = null;
    $('.user_popup').hover(
        function(event) {
            // обработчик события mouse in
            var elem = $(event.currentTarget);
            timer = setTimeout(function() {
                timer = null;
                xhr = $.ajax(
                    '/user/' + elem.first().text().trim() + '/popup').done(
                        function(data) {
                            xhr = null;
                            elem.popover({
                                trigger: 'manual',
                                animation: false,
                                html:true,
                                container: elem,
                                content: data,
                                title:elem.first().html()
                            }).popover('show');
                            $('.popover-body').html(data)
                            flask_moment_render_all();
                        }
                    );
            }, 500);
        },
        function(event) {
            // обработчик события mouse out
            var elem = $(event.currentTarget);
            if (timer) {
                clearTimeout(timer);
                timer = null;
            }
            else if (xhr) {
                xhr.abort();
                xhr = null;
            }
            else {
                elem.popover('hide');
            }
        }
    )
});