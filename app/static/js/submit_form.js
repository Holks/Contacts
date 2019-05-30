"use strict";
function submit_form() {
  var formData = new FormData(document.querySelector('#addcontactform'));
  var jsonObj = formToJSON(formData);
  $.ajax({
    method: "POST",
    url: "contact",
    data: jsonObj,
    contentType: "application/json; charset=utf-8",
    cache: false,
    success: function(data, textStatus) {
      document.open();
      document.write(data);
      document.close();
    }
  });
  
  return false;
}
function edit_contact() {
  var formData = new FormData(document.querySelector('#editcontactform'));
  var jsonObj = formToJSON(formData);
  $.ajax({
    method: "PUT",
    url: "contact/" + formData.get('contact_id'),
    data: jsonObj,
    contentType: "application/json; charset=utf-8",
    cache: false,
    success: function(data, textStatus) {
      console.log(data);
      window.location.href = data;
    }
  });  
  return false;
}
function delete_contact() {
  var formData = new FormData(document.querySelector('#editcontactform'));
  var jsonObj = formToJSON(formData);
  $.ajax({
    method: "DELETE",
    url: "contact/" + formData.get('contact_id'),
    data: jsonObj,
    contentType: "application/json; charset=utf-8",
    cache: false,
    success: function(data, textStatus) {
      console.log(data);
      window.location.href = data;
    }
  });  
  return false;
}