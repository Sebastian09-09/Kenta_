const initBg = (autoplay = true) => {
    var values = [0,1,2],
    valueToUse = values[Math.floor(Math.random() * values.length)];
    if ( valueToUse == 0 ){
        var bgImgsNames = ['bg0/bakugo.jpg', 'bg0/shoyohinata.jpg', 'bg0/kira.jpg','bg0/mob.jpg','bg0/foodwars.jpg'];
    }
    if ( valueToUse == 1 ){
        var bgImgsNames = ['bg1/0.jpg', 'bg1/1.jpg', 'bg1/2.jpg','bg1/3.jpg','bg1/4.jpg'];
    }
    if ( valueToUse == 2 ){
        var bgImgsNames = ['bg2/0.jpg', 'bg2/1.jpg', 'bg2/2.jpg','bg2/3.jpg','bg2/4.png'];
    }
    const bgImgs = bgImgsNames.map(img => "../static/img/" + img);

    $.backstretch(bgImgs, {duration: 4000, fade: 1000});

    if(!autoplay) {
      $.backstretch('pause');  
    }    
}

const setBg = id => {
    $.backstretch('show', id);
}

const setBgOverlay = () => {
    const windowWidth = window.innerWidth;
    const bgHeight = $('body').height();
    const tmBgLeft = $('.tm-bg-left');

    $('.tm-bg').height(bgHeight);

    if(windowWidth > 768) {
        tmBgLeft.css('border-left', `0`)
                .css('border-top', `${bgHeight}px solid transparent`);                
    } else {
        tmBgLeft.css('border-left', `${windowWidth}px solid transparent`)
                .css('border-top', `0`);
    }
}

$(document).ready(function () {
    const autoplayBg = true;	// set Auto Play for Background Images
    initBg(autoplayBg);    
    setBgOverlay();

    const bgControl = $('.tm-bg-control');            
    bgControl.click(function() {
        bgControl.removeClass('active');
        $(this).addClass('active');
        const id = $(this).data('id');                
        setBg(id);
    });

    $(window).on("backstretch.after", function (e, instance, index) {        
        const bgControl = $('.tm-bg-control');
        bgControl.removeClass('active');
        const current = $(".tm-bg-controls-wrapper").find(`[data-id=${index}]`);        
        current.addClass('active');
    });

    $(window).resize(function() {
        setBgOverlay();
    });
});