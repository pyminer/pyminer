window.MathJax = {
    tex: {
        inlineMath: [['$', '$']],
        displayMath: [['$$', '$$']],
        processEnvironments: true,
        processRefs: true
    },
    options: {
        skipHtmlTags: ['noscript', 'style', 'textarea', 'pre', 'code'],
        ignoreHtmlClass: 'tex2jax_ignore',
        renderActions: {
            find_script_mathtex: [10, function (doc) {
                for (const node of document.querySelectorAll('script[type^="math/tex"]')) {
                    const display = !!node.type.match(/; *mode=display/);
                    const math = new doc.options.MathItem(node.textContent, doc.inputJax[0], display);
                    const text = document.createTextNode('');
                    node.parentNode.replaceChild(text, node);
                    math.start = { node: text, delim: '', n: 0 };
                    math.end = { node: text, delim: '', n: 0 };
                    doc.math.push(math);
                }
            }, '']
        }
    },
    svg: {
        fontCache: 'global'
    }
};

function toggleNav(){
    var nav = document.getElementById("navigation");
    var display = window.getComputedStyle(nav)["display"];
    if (display == "none") {
        nav.style.display = "block";
    }else{
        nav.style.display = "none";
    }
}