
  $.datetimepicker.setDateFormatter({
      parseDate: function (date, format) {
          var d = moment(date, format);
          return d.isValid() ? d.toDate() : false;
      },
      formatDate: function (date, format) {
          return moment(date).format(format);
      },
  });

  $('.datetime').datetimepicker({
      format:'DD-MM-YYYY hh:mm A',
      formatTime:'hh:mm A',
      formatDate:'DD-MM-YYYY',
      useCurrent: false,
  });

  // Initialise Pusher
  const pusher = new Pusher('b4ab28bc8116e3dceba1', {
      cluster: 'eu',
      encrypted: true
  });

  var channel = pusher.subscribe('table');

  channel.bind('new-record', (data) => {

      const expiry_date = moment(`${data.data.expiry_date}`, 'DD/MM/YYYY hh:mm a').format('YYYY-MM-DD hh:mm:ss a')
     $('#flights').append(`
          <tr id="${data.data.id}">
              <th scope="row"> ${data.data.name} </th>
              <td> ${data.data.quantity} </td>
              <td> ${expiry_date} </td>
          </tr>
     `)
  });

  channel.bind('delete-record', (data) => {
    $(`#${data.data.id}`).remove();
  });

  channel.bind('update-record', (data) => {

      const expiry_date = moment(`${data.data.expiry_date}`, 'DD/MM/YYYY hh:mm a').format('YYYY-MM-DD hh:mm:ss a')
      if (includeEditButton) {
      $(`#${data.data.id}`).html(`
          <th scope="row"> ${data.data.name} </th>
          <td> ${data.data.quantity} </td>
          <td> ${expiry_date} </td>
          <td> <a href="/edit/${ data.data.id }">Edit</a> </td>
      `)
    } else {
      $(`#${data.data.id}`).html(`
          <th scope="row"> ${data.data.name} </th>
          <td> ${data.data.quantity} </td>
          <td> ${expiry_date} </td>
      `)
    }
   });
