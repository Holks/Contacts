$(document).ready(function(){
    $(document).on('dblclick', '#list_view tbody tr', function(){        
        var $this = $(this);
        var contact_id = $this.closest("tr").children('td:eq(0)').prop('textContent');
        console.log(contact_id);
        $.get("contact/"+contact_id, function(data, status){
            document.open();
            document.write(data);
            document.close();
        });
    });
});