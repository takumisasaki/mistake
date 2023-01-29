$(document).ready(function(event){
    $(document).on('click', '#like', function(event){
        console.log('ok')
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: "{% url 'like' %}",
            data: {
                'post.id': $(this).attr('name'),
                'csrfmiddlewaretoken': '{{ csrf_token }}'},
            dataType: 'json',
            success: function(response){
                selector = document.getElementsByName(response.post.id);
                if(response.liked){
                    $(selector).html("<i class='fas fa-lg fa-heart'></i>");
                }
                else {
                    $(selector).html("<i class='far fa-lg fa-heart'></i>");
                }
                selector2 = document.getElementsByName(response.post_id + "-count");
                $(selector2).text(response.count);
            }
        });
    })
})