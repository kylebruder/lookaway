// Show image upload preview
// https://stackoverflow.com/questions/4459379/preview-an-image-before-it-is-uploaded
var loadFile = function(event) {
  var output = document.getElementById('output');
  output.src = URL.createObjectURL(event.target.files[0]);
  output.onload = function() {
    URL.revokeObjectURL(output.src) // free memory
  }
};

// Searchable select field
// https://stackoverflow.com/questions/18796221/creating-a-select-box-with-a-search-option/57809086#57809086
$(document).ready(function () {
    $('select').selectize({
        sortField: 'text'
    });
});
