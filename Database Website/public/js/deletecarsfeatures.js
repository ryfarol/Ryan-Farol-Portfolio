function deleteCarsFeatures(id){
    $.ajax({
        url: '/cars-features/' + id,
        type: 'DELETE',
        success: function(result){
            window.location.reload(true);
        }
    })
};