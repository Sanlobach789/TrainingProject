function getCheckedCheckBoxes() {
  let checkboxes = document.getElementsByClassName('checkbox');
  let checkboxesChecked = {};
  for (let index = 0; index < checkboxes.length; index++) {
     if (checkboxes[index].checked) {
         attrId = parseInt(checkboxes[index].dataset.filterid);
         filterValue = checkboxes[index].dataset.value;
         if (checkboxesChecked[attrId]) {
             const buffer = checkboxesChecked[attrId];
             buffer.push(filterValue);
         }
         else {
             checkboxesChecked[attrId] = [filterValue];
         }
     }
  }
  console.log(checkboxesChecked)
  return checkboxesChecked;
}

$( document ).ready(function() {
    $('.product_filters').on('input', (event)=> {
        filterSet = getCheckedCheckBoxes();
        result = filterSet

        $.post(URL, result, function (response) {
            if(response == 'success'){ console.log(response); }
            else{ alert('Error! :('); }
        })
        // $.ajax({
        //     url: "/products/filters/" + filter_id + "/" + filter_value + "/" + action + "/",
        //
        //     success: function (data) {
        //         console.log(data.result)
        //     }
        // });
    })
});
