function alternar(id) {
    var el = document.getElementById(id)
    toggleClass(el, 'escondido')
    toggleClass(el.parentElement, 'ressaltar-fraco')
    toggleClass(el.parentElement.getElementsByClassName('item-titulo')[0], 'ressaltar')
}



// http://stackoverflow.com/questions/25543956/toggle-class-on-html-element-without-jquery

function toggleClass(element, toggleClass){
    var currentClass = element.className;
    var newClass;
    if(currentClass.indexOf(toggleClass) > -1){ //has class
        newClass = currentClass.replace(toggleClass,"")
    }else{
        newClass = currentClass + " " + toggleClass;
    }
    element.className = newClass;
}

// ------------------------------------------------------------------------



// http://stackoverflow.com/questions/17534661/make-anchor-link-go-some-pixels-above-where-its-linked-to

function addMargin() {
    window.scrollTo(0, window.pageYOffset - 30);
}

window.addEventListener('hashchange', addMargin);

(function() {
    if (document.location.hash) {
        setTimeout(addMargin , 10);
    }
})();

// ------------------------------------------------------------------------
