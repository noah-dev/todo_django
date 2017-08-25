//On document load, populate the left-hand side with the first item from
//the right-hand side.
$(function() {
  get_item();
});

function get_item(){
  //Get the first item from the list. If no item exists, display an empty form.

  //item_id is equivalent to the item's pk in the database.
  if ( $( ".item" ).length ) {
    item_id = $( ".item:first" ).get(0).id
    item_ajax(item_id)
  } else {
    //If no item, then empty out left-side
    $("#json_title_text").text("Empty List");
    $("#json_desc_text").text('Please Add An Item');
    $("#json_impact_text").text('');
    $("#json_due_date").text('');
    $("#json_start_date").text('');
    $("#json_add_date").text('');
    $('input[name="item_complete"]').prop('checked', false);
    $(".todo_item").removeAttr('id');
  }
}

//Retrive an item from the right-hand side list based on item_id
//item_id is equivalent to items'pk in the database.
function item_ajax(item_id) {
  //Animation. .todo_item holds the elements that display the item's information
  //Begin with a fade to 0 opacity (disappear), wait a bit and then
  //reappear with fade to 1 opacity
  $(".todo_item").fadeTo(400, 0, function() {
    $(".todo_item").delay(400);
    $(".todo_item").fadeTo(400, 1);
  })

  //In order to give time for the animation, delay the ajax request by 600 ms
  setTimeout(function(){
    //Setup the ajax request and send it off - handled by urls.py
    $.ajax({
      url: 'show_item/',
      data: {
        'id': item_id
      },
      dataType: 'json',

      //When it returns, populate the fields in .todo_item
      success: function (data) {
        //Parse the data as JSON and begin assigning attributes to the elements
        data = JSON.parse(data);
        $("#json_title_text").text(data['title_text']);

        $("#json_desc_text").text(data['desc_text']);
        $("#json_impact_text").text(data['impact_text']);

        //Instead of everything, just get the month, date and year
        $("#json_due_date").text(date_format(data['due_date']));
        $("#json_start_date").text(date_format(data['start_date']));
        $("#json_add_date").text(date_format(data['add_date']));

        //Retrive the checkbox element.
        //If the item is complete, then check it
        //If the item is not complete, do not check it.
        var checkbox = $('input[name="item_complete"]')
        if (data['complete'] == false) {
          checkbox.prop('checked', false);
        } else if (data['complete'] == true) {
          checkbox.prop('checked', true);
        } else {
          alert("ERROR WITH CHECKBOX")
        }
        //Assign an pk to todo_item. This is used when the user clicks the
        //checkbox and the record in the database needs to be updated.
        $(".todo_item").attr('id', item_id);
      }
    });
  }, 600);
}

function date_format(datetime){
  var date = datetime.split('-');
  return date[1] + '/' + date[2].slice(0,2) + '/' + date[0]
}

//When an item is clicked on from the right-hand side lists, display that item
//on the left-hand side.
$(".item").click(function () {
  //Retrive the elements id, equivalent to the item's pk in the database
  var id = $(this).get(0).id;
  item_ajax(id)
});


//When the checkbox is clicked, this function is called.
//Two things are accomplished: 1) The database is updated
//2) The item's complete status on the right-hand side is updated
$('input[name="item_complete"]').on('change', function () {
  //Get it's item_id, equivalent to item's pk in database
  var item_id = $(".todo_item").get(0).id;

  //Retrive the checkbox element
  var checkbox = $('input[name="item_complete"]')
  var complete = checkbox.is(':checked');

  //Setup the ajax request and send it off - handled by urls.py
  $.ajax({
    url: 'complete_item/',
    data: {
      'id': item_id,
      'complete': complete
    },
    dataType: 'json',

    //When it returns, the database has been updated. Now the frontend
    //neeeds to be updated. Find the item from the right-hand side and
    //assign the appropriate html markup depending on if it is complete
    //or not complete
    success: function (data) {
      var item_complete_element = $("#" + item_id +".complete_info");
      var complete_status = item_complete_element.find("span");
      if (complete){
        complete_status.css("color","#ecececff");
        setTimeout(function(){
          complete_status.text("True");
          complete_status.css("color","green");
        }, 500);
      } else if (!complete){
        complete_status.css("color","#ecececff");
        setTimeout(function(){
          complete_status.text("False");
          complete_status.css("color","red");
      }, 500);
      } else {
        console.log("ERROR WITH CHECKBOX JS")
      }
    }
  });

});

var countdown
//
$('#delete_button').click(function (){
  //Reveal confirmation button and show 
  var delete_button = $('#delete_button');
  var del_confirm_button = $('#del_confirm_button');
  delete_button.attr('disabled','disabled');

  //Set timeout for how long before confirm button disappers
  var timeout = 5; 
  delete_button.text(timeout);
  countdown = setInterval(function(){
    timeout = timeout-1; 
    delete_button.text(timeout)
  },1000);

  del_confirm_button.css('visibility','visible')
  del_confirm_button.css('opacity','1')

  //If the confirm button is not pressed, renable delete button
  setTimeout(function(){
    reset_delete_buttons();
  }, timeout*1000);
});

function reset_delete_buttons(){
  //Called to reset the buttons (both delete & confirm) if either timeout or item is deleted. 
  clearInterval(countdown);
  var delete_button = $('#delete_button');
  var del_confirm_button = $('#del_confirm_button');
  delete_button.text('Delete Item')
  delete_button.removeAttr('disabled')
  //visibility disables the button's functionality
  //opacity enables transitions. Without visiblity set to hidden, button could still be pressed
  del_confirm_button.css('visibility','hidden')
  del_confirm_button.css('opacity','0')
}


$('#del_confirm_button').click(function (){
  //After the user has clicked the delete button, wait for the confirmation before deleting.

  //Get it's item_id, equivalent to item's pk in database
  var item_id = $(".todo_item").get(0).id;

  //Setup the ajax request and send it off - handled by urls.py
  $.ajax({
    url: 'delete_item/'+item_id,
    data: {
      'id': item_id,
    },
    dataType: 'json',

    //Upon completion, remove the item from the right-side and reload left-side
    success: function (data) {
      $("#"+item_id+".item").remove();

      get_item();

      reset_delete_buttons();
    }
  });

});

//Show/hide overlay form for new items
$("#add").click(function (){
  $("#new_item").css('display', 'block');
});
$("#cancel_button").click(function (){
  $("#new_item").css('display', 'none');
});

//Sidenav Code

var show = '12%';
var hide = '3%';
var nav_expanded = false;
$("#nav").css('width', show)
$("#content").css('margin-left', show);

$("#nav_toggle").click(function () {
  var nav = $("#nav");
  var content = $("#content");
  var nav_icon = $(".nav_icon");
  var nav_toggle = $("#nav_toggle");
  if (nav_expanded) {
    nav.css('width', show)
    content.css('margin-left', show);
    nav_icon.css('padding', '10%');
    nav_toggle.toggleClass( "mirror_img" );
    nav_expanded = false;
  } else {
    nav.css('width', hide)
    content.css('margin-left', hide);
    nav_icon.css('padding', '10%');
    nav_toggle.toggleClass( "mirror_img" );
    nav_expanded = true;
  }
});


//Datepicker Code
var picker = new Pikaday({
    field: document.getElementById('start_date'),
    format: 'M/D/YYYY',
    toString(date, format) {
        const day = date.getDate();
        const month = date.getMonth() + 1;
        const year = date.getFullYear();
        return `${month}/${day}/${year}`;
    },
});

var picker = new Pikaday({
    field: document.getElementById('due_date'),
    format: 'M/D/YYYY',
    toString(date, format) {
        const day = date.getDate();
        const month = date.getMonth() + 1;
        const year = date.getFullYear();
        return `${month}/${day}/${year}`;
    },
});
