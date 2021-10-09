$(function(){
    $('.pictures-test').slick({
        autoplay: true,
        autoplaySpeed: 3000,
        speed: 2000,
        centerMode: true,
        centerPadding: '20%',
        responsive: [{
            breakpoint: 520,
            settings: {
                centerMode: false,
                centerPadding: 0,
                arrows: false,
            }
        }]
    });
});
