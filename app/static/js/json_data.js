"use strict";
function formToJSON( formData ) {
  var object = {};
  formData.forEach(function(value, key, element){

    object[key] = value;
  });
  var json_obj = JSON.stringify(object);

  return json_obj;
};