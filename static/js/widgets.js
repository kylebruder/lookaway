// Show image upload preview
// https://stackoverflow.com/questions/4459379/preview-an-image-before-it-is-uploaded
var loadFile = function(event) {
  var output = document.getElementById('output');
  output.src = URL.createObjectURL(event.target.files[0]);
  output.onload = function() {
    URL.revokeObjectURL(output.src) // free memory
  }
};

// Show video upload preview
// https://stackoverflow.com/questions/36035721/how-can-i-set-preview-of-video-file-selecting-from-input-type-file/40580663
$(document).on("change", ".file_multi_media", function(evt) {
  var source = $('source');
  for(let i = 0; i < source.length; i++){
    source[i].src = URL.createObjectURL(this.files[0]);
    source.parent()[0].load();
  }
});

// Searchable select field
// https://stackoverflow.com/questions/18796221/creating-a-select-box-with-a-search-option/57809086#57809086
$(document).ready(function () {
    $('select').selectize({
        sortField: 'text'
    });
});
