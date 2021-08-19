function updatecar(id){
    $.ajax({
        url: '/cars/' + id,
        type: 'PUT',
        data: $('#update-car').serialize(),
        success: function(result){
            window.location.replace("//db-auto.herokuapp.com/cars");
        }
    })
};