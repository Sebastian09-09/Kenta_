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

    $.backstretch(bgImgs, {duration: 5000, fade: 1500});

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
    0: ['kissmanga.org.png' , '70' , 'Read manga online in high quality for free, fast update, daily update Unique reading type All pages just need to scroll to read next page, and many more.' , 'Kiss Manga' , 'https://kissmanga.org/'],
    1: ['mangakakalot.png' , '70' , 'Read manga online free at Mangakakalot.com, update fastest, most full, synthesized 24h free with high-quality images and be the first one to publish new chapters.' , 'MangaKakalot' , 'https://mangakakalot.com/'],
    2: ['manganelo.png' , '70' ,'Read manga online free at MangaNato, update fastest, most full, synthesized 24h free with high-quality images. We hope to bring you happy moments. Join and discuss','MangaNato' , 'https://manganato.com/'],
    //3: ['nhentai.webp' , '200' ,'nHentai is a free and frequently updated hentai manga and doujinshi reader packed with thousands of multilingual comics for reading and downloading.','nhentai' , 'https://nhentai.com/'],
    3: ['mangaread.org.png' , '70' , 'Welcome to the world of manga. Latest novelties manga to read online. A daily updated directory of the manga. Read along with us.','Mangaread.org' , 'https://mangaread.org/'],
    4: ['readm.org.png' , '70' , 'Biggest manga library on the web. Absolutely free and daily updated English translated manga online for free!','Readm.org' , 'https://readm.org/'],
    5: ['webtoon.jpg' , '70' , 'WEBTOON is home to thousands of stories across 23 genres including romance, comedy, action, fantasy, and horror. Read comics, webcomics, manga, and manhwa online or download the WEBTOON app.','Webtoon.com' , 'https://webtoon.com/'],
};
function increment(){
    if (currentWebpage < 5){
        currentWebpage = currentWebpage + 1
        document.getElementById('currentWebsite').innerHTML = String(currentWebpage + 1)+'/6'
        document.getElementById('logo').src = '/static/img/supportedWebsites/'+self.websites[currentWebpage][0]
        document.getElementById('logo').height = self.websites[currentWebpage][1]
        document.getElementById('about').innerHTML = self.websites[currentWebpage][2]
        document.getElementById('title').innerHTML =  '<a class="links" href="' + String(self.websites[currentWebpage][4]) + '" target="_blank">' + String(self.websites[currentWebpage][3]) + '</a>'
        fixit()
    }
}
function decrement(){
    if (currentWebpage >= 1){
        currentWebpage = currentWebpage - 1
        document.getElementById('currentWebsite').innerHTML = String(currentWebpage + 1)+'/6'
        document.getElementById('logo').src = '/static/img/supportedWebsites/'+self.websites[currentWebpage][0]
        document.getElementById('logo').height = self.websites[currentWebpage][1]
        document.getElementById('about').innerHTML = self.websites[currentWebpage][2]
        document.getElementById('title').innerHTML =  '<a class="links" href="' + String(self.websites[currentWebpage][4]) + '" target="_blank">' + String(self.websites[currentWebpage][3]) + '</a>'
        fixit()
    }
}
function fix(){
    document.getElementById("grab").style.height = "100%";
}
function Start() {
    if (document.getElementById("checkbox_").checked){
        textSequence(0);
        document.getElementById("loading").style.display = "block";
        //document.getElementById("contact-form").submit();
    }
}
function Fetch() {
    textSequence(0);
    document.getElementById("loading").style.display = "block";
}

var loading = ['Loading', 'lOading', 'loAding', 'loaDing' , 'loadIng', 'loadiNg' , 'loadinG'];


function textSequence(i) {
  if (loading.length > i) {
    setTimeout(function() {
      document.getElementById("seq").innerHTML = loading[i];
      textSequence(++i);
    }, 130);
  } else if (loading.length == i) { // Loop
    textSequence(0);
  }
}

function readMore() {
    var dots = document.getElementById("dots");
    var moreText = document.getElementById("more");
    var btnText = document.getElementById("myBtn");
  
    if (dots.style.display === "none") {
      dots.style.display = "inline";
      btnText.innerHTML = "Read more"; 
      moreText.style.display = "none";
    } else {
      dots.style.display = "none";
      btnText.innerHTML = "Read less"; 
      moreText.style.display = "inline";
    }

    fixit()
}

function fixit() {
    if (document.body.scrollWidth >= 768){
        var height = document.getElementById('grab').clientHeight;
        document.getElementById("handle").style.borderTop = String(height)+'px solid transparent';
        document.getElementById("handle").style.borderLeft = 0;
    }else{
        var width = document.getElementById('grab').clientWidth;
        document.getElementById("handle").style.borderLeft = String(width)+'px solid transparent';
        document.getElementById("handle").style.borderTop = 0;
    }
    fix()
}

function toggleLink(checkBox)
{
    var link = document.getElementById("start");
    
    if (checkBox.checked){
        link.style.display = "inline";
    }else{
        link.style.display = "none";
    }
    fixit()
}


function toggleDownload(checkBox)
{
    var hide = document.getElementById("hide");
    
    if (checkBox.checked){
        hide.style.display = "none";
    }else{
        hide.style.display = "inline";
    }
    fixit()
}



window.onresize = fixit;