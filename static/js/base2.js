// 데스크톱에서 화면 크기를 일반 사이즈로 resize할 때 메뉴를 정상적으로 보이게 한다.
$(window).resize(function() {
    if($(window).width() > 768) {
        $('#nav-menu').removeAttr('style');
    }
});

// 데스크톱 sm 사이즈 혹은 모바일, 테블릿에서 버튼을 클릭하면 드롭다운 메뉴를 보여준다.
$("#nav-button > button").on({
    click: function() {
        $("#nav-menu").slideToggle(250);
    }
});