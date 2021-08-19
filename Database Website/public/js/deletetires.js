function deleteTires(id){
    $.ajax({
        url: '/tires/' + id,
        type: 'DELETE',
        success: function(result){
            window.location.reload(true);
        }
    })
};