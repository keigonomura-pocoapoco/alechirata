$(function(){
    $('.portfolio').slick({
        autoplay: true,
        autoplaySpeed: 3000,
        variableWidth: true,
        speed: 2000,
        centerMode: true,
        centerPadding: '20%',
        responsive: [{
            breakpoint: 520,
            settings: {
                variableWidth: false,
                centerMode: false,
                centerPadding: 0,
                arrows: false,
            }
        }]
    });
});

$(function(){
    var $projectSlider = $('.project-show').on('init', function(event, slick) {
        $('.current').text(slick.currentSlide + 1);
        $('.total').text(slick.slideCount);
      })
      .slick({
        infinite: true,
        slidesToShow: 1,
        fade: true,
        centerMode: true,
        focusOnSelect: true,
        arrows: false,
        adaptiveHeight: true,
    })
    .on('beforeChange', function(event, slick, currentSlide, nextSlide) {
        $('.current').text(nextSlide + 1);

        if(slick.currentSlide + 1 == slick.slideCount - 1){
            $('.commentary-check').text('解説/Commentary');
        }
    });

    $projectSlider.find(".slick-slide").on("click", function(){
        $projectSlider.slick("slickNext");
     });

    
});
