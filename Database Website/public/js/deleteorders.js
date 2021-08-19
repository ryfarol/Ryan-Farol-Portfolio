function deleteOrders(id){
    $.ajax({
        url: '/orders/' + id,
        type: 'DELETE',
        success: function(result){
            window.location.reload(true);
        }
    })
};