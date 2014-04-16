function init_sidebar(sidebar_file) {
    $.get(sidebar_file, function(data) {
        $("#sidebar").html(marked(data));
    }, "text").fail(function() {
        alert("Opps! can't find the sidebar file to display!");
    });
}

function init_content(content_file) {
    $.get(content_file, function(data) {
        $("#content").html(marked(data));
    }, "text").fail(function() {
        alert("Opps! can't find the default index file to display!");
    });

    $("#back_to_top").on("click", function() {
        $("html body").animate({
            scrollTop: 0
        }, 200);
    });
}

function init_edit(base_url) {
    $("#edit").on("click", function() {
        var hash = location.hash.replace("#", "/");

        if (hash === "") {
            hash = "/README.md";
        }

        window.location.replace(base_url + hash);
    });
}

function show_error(error_file) {
    $.get("404.md", function(data) {
        $("#content").html(marked(data));
    }, "text").fail(function() {
        alert("Opps! can't find the 404 file to display!");
    });
}

function replace_symbols(text) {
    // replace symbols with underscore
    return text.replace(/[&\/\\#,+()$~%.'":*?<>{}]/g, "_");
}

function li_create_linkage(li_tag, header_level) {
    // add custom id and class attributes
    html_safe_tag = replace_symbols(li_tag.text());
    li_tag.attr("id", html_safe_tag);
    li_tag.attr("class", "link");

    // add click listener - on click scroll to relevant header section
    $("#content li#" + li_tag.attr("id")).click(function() {
        var header = $("#content h" + header_level + "." + li_tag.attr("id"));
        $('html body').animate({
            scrollTop: header.offset().top
        }, 200);
    });
}

function create_page_anchors() {
    // create page anchors by matching li's to headers
    // if there is a match, create click listeners
    // and scroll to relevant sections

    // go through header level 2 and 3
    for (var i = 2; i <= 4; i++) {
        // parse all headers
        var headers = [];
        $('#content h' + i).map(function() {
            headers.push($(this).text());
            $(this).addClass(replace_symbols($(this).text()));
        });

        // parse and set links between li and h2
        $('#content ul li').map(function() {
            for (var j = 0; j < headers.length; j++) {
                if (headers[j] === $(this).text()) {
                    li_create_linkage($(this), i);
                }
            }
        });
    }
}

function router() {
    var path = location.hash.replace("#", "./");

    // default page if hash is empty
    if (path === "") {
        path = "README.md";
    }

    $.get(path, function(data) {
        var doc = marked(data);
        $("#content").html(doc);
        create_page_anchors();
    }).fail(show_error);
}

$(document).ready(function() {
    init_sidebar("pages/sidebar.md");
    init_content("README.md");
    init_edit("https://github.com/chutsu/playground/tree/gh-pages");

    router();
    $(window).on('hashchange', router);
});
