function contact_request() {
    var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    var url = $("#contact_request").attr("data-ajax-target")
    $.post(url)
    console.log(url)
};

function ask_enrollment() {
    $('.ask_enrollment').on("click", function(e) {
        e.preventDefault()
        course = $(this).attr('data-slug')
        console.log(course, 'course_slug')
            // txt = document.getElementById('example').value
        data = {
            course: course
        }
        $.ajax({
            type: "POST",
            url: '{% url "enrollments:create" %}',
            data: data,
            // success: function(data) {
            //     $('#cart_count').html(data.cart_total)
            // }
        })
    })
}