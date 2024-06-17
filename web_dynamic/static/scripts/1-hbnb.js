$(function () {
  """ Object to store selected amenities"""
  const amen = {};

  """Event listener for changes on checkboxes with id 'check_amen"""
  $('input#check_amen').change(function () {
    """Check if the checkbox is checked"""
    if ($(this).is(':checked')) {
      """Add the amenity to the object"""
      amen[$(this).attr('data-name')] = $(this).attr('data-id');
    } else {
      """Remove the amenity from the object"""
      delete amen[$(this).attr('data-name')];
    }

    """ Get the list of amenity names, sort them, and display them in h4 element"""
    const objNames = Object.keys(amen);
    $('.amenities h4').text(objNames.sort().join(', '));
  });
});
