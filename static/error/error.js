$(document).ready(function() {
    // 에러 메시지가 있으면 모달 팝업 창을 표시함.
    {% if form.errors %}
      $('#error-modal').css('display', 'block');
    {% endif %}
  
    // 모달 팝업 창을 닫기위한 함수 짰음. 
    $('.close').click(function() {
      $('#error-modal').css('display', 'none');
    });
  });