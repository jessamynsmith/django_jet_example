var $ = jet.jQuery;

var doAjax = function(url, method, itemId, data, callback) {
    console.log("Calling " + method + " on item " + itemId + " ...");
    if (itemId !== null) {
        url += itemId + '/';
    }

    var ajaxParams = {
        url: url,
        contentType: 'application/json',
        type: method,
        beforeSend: function(jqXHR, settings) {
            jqXHR.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
        },
        success: function(data, textStatus, jqXHR) {
            console.log(method + " on " + itemId + " succeeded");
            if (callback) {
              callback(data);
            }

        }
    }

    if (data) {
      ajaxParams.data = JSON.stringify(data);
    }

    $.ajax(ajaxParams);
};

$(document).ready(function() {

    var dialog,
      form,
      personId,
      tag = $( ".tag" ),
      allFields = $( [] ).add( tag );

    $('.dialog-form').dialog({
          autoOpen: false,
          width: 350,
          modal: true,
          buttons: {
            "Send": sendTag,
            Cancel: function() {
              dialog.dialog( "close" );
            }
          },
          close: function() {
            allFields.removeClass( "ui-state-error" );
          }
        });

    function updateTips( t ) {
      var tips = dialog.find('.validateTips');
      tips
        .text( t )
        .addClass( "ui-state-highlight" );
      setTimeout(function() {
        tips.removeClass( "ui-state-highlight", 1500 );
      }, 500 );
    }

    function checkLength( o, n, min, max ) {
      if ( o.val().length > max || o.val().length < min ) {
        o.addClass( "ui-state-error" );
        updateTips( "Length of " + n + " must be between " +
          min + " and " + max + "." );
        return false;
      } else {
        return true;
      }
    }

    function sendTag() {
        var valid = true;
        allFields.removeClass( "ui-state-error" );
        var tagField = dialog.find('input[name="tag"]');
        valid = valid && checkLength( tagField, "tag", 2, 160 );

      if ( valid ) {
        console.log("VALID");


        var data = {
          tag_value: tagField.val(),
          person: personId
        };
        doAjax("/api/v1/persontag/", "POST", null, data);
        personId = null;
        dialog.dialog( "close" );
      }
      return valid;
    }

    form = $( ".tag_form" );
    form.on( "submit", function( event ) {
      event.preventDefault();
      sendTag();
    });

    $('.tag_button').on('click', function(evt) {
        // Get the to phone number for this row
        var row = $(this).closest('tr[class^="row"]');
        personId = row.find('[name="_selected_action"]').val();

        // populate the to number in the form and open the dialog
        dialog = $($('.dialog-form')[0]);
        dialog.find('input[name="to_number"]').val(personId);
        dialog.dialog( "open" );
    });
});
