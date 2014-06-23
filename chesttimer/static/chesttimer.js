$('body').ajaxStart(function () {
  $('div.loading').removeClass('hide');
});

$('body').ajaxStop(function () {
  $('div.loading').addClass('hide');
});
