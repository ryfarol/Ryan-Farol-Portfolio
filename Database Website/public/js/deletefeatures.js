function deleteFeatures(id){
    $.ajax({
        url: '/features/' + id,
        type: 'DELETE',
        success: function(result){
            window.location.reload(true);
        }
    })
};