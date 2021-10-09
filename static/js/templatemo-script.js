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

var currentWebpage = 0;
var websites = {
    0: ['kissmanga.org.png' , '350' , 'Read manga online in high quality for free, fast update, daily update Unique reading type All pages just need to scroll to read next page, and many more.' , 'Kiss Manga'],
    1: ['mangakakalot.png' , '215' , 'Read manga online free at Mangakakalot.com, update fastest, most full, synthesized 24h free with high-quality images and be the first one to publish new chapters.' , 'MangaKakalot'],
    2: ['manganelo.png' , '215' ,'Read manga online free at MangaNato, update fastest, most full, synthesized 24h free with high-quality images. We hope to bring you happy moments. Join and discuss','MangaNato'],
    3: ['mangaowl.png' , '70' , 'Read english manga online free with a huge collections at Manga Owl, update fastest, most full, synthesized, translate free with high-quality images. The best place to read the updated latest, greatest, best-quality english manga for FREE with our best service. Enjoy!' , 'MangaOwl'],
    4: ['nhentai.webp' , '200' ,'nHentai is a free and frequently updated hentai manga and doujinshi reader packed with thousands of multilingual comics for reading and downloading.','nhentai'],
    5: ['readm.org.png' , '210' , 'Biggest manga library on the web. Absolutely free and daily updated English translated manga online for free!','Readm.org'],
};
function increment(){
    if (currentWebpage < 5){
        currentWebpage = currentWebpage + 1
        document.getElementById('currentWebsite').innerHTML = String(currentWebpage + 1)+'/6'
        document.getElementById('logo').src = '/static/img/supportedWebsites/'+self.websites[currentWebpage][0]
        document.getElementById('logo').width = self.websites[currentWebpage][1]
        document.getElementById('about').innerHTML = self.websites[currentWebpage][2]
        document.getElementById('title').innerHTML = self.websites[currentWebpage][3]
        document.getElementById("grab").style.height = "100%";
    }
}
function decrement(){
    if (currentWebpage >= 1){
        currentWebpage = currentWebpage - 1
        document.getElementById('currentWebsite').innerHTML = String(currentWebpage + 1)+'/6'
        document.getElementById('logo').src = '/static/img/supportedWebsites/'+self.websites[currentWebpage][0]
        document.getElementById('logo').width = self.websites[currentWebpage][1]
        document.getElementById('about').innerHTML = self.websites[currentWebpage][2]
        document.getElementById('title').innerHTML = self.websites[currentWebpage][3]
        document.getElementById("grab").style.height = "100%";
    }
}
function fix(){
    document.getElementById("grab").style.height = "100%";
}
function Start() {
    if (document.getElementById("checkbox_").checked){
        document.getElementById("loading").style.display = "block";
        document.getElementById("grab").style.height = "100%";
    }
}
function Fetch() {
    document.getElementById("loading").style.display = "block";
    document.getElementById("grab").style.height = "100%";
}