$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('#imagePreview').css('background-image', 'url(' + e.target.result + ')');
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
            $('#predict').empty();
        }
    }
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        $('#result').text('');
        $('#result').hide();
        readURL(this);
    });

    // Predict
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();
        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.loader').hide();
                $('#result').fadeIn(600);
                // create an image
                path = '/static/results.jpg' + '?rand=' + Math.random();
                var tempData = JSON.parse(data);
                console.log('Success!' + tempData);

                $('#result').css('background-image', 'url(' + path + ')');

                $('#predict').append("<div class='msg'>"+tempData["Title"]+"</div>");
                var list = $('<ul />')
                $('#predict').append(list);
                $.each(tempData["Product"], function(index, value) {
                    //console.log(index, value);
                    var item = $('<ul class="item" />');
                    item.append($('<li />', {text: 'Name: ' + value['Name']}));
                    item.append($('<li />', {text: 'Ingredient: ' + value['Ingredient']}));
                    item.append($('<li />', {text: 'Info: ' + value['Info']}));
                    item.appendTo(list);

                });
            },
        });
    });

});
