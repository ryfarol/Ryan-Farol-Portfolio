function updateorder(id){
    $.ajax({
        url: '/orders/' + id,
        type: 'PUT',
        data: $('#update-order').serialize(),
        success: function(result){
            window.location.replace("//db-auto.herokuapp.com/orders");
        }
    })
};