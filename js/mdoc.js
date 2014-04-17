function init_sidebar_section(sidebar_file) {
    $.get(sidebar_file, function(data) {
        $("#sidebar").html(marked(data));
    }, "text").fail(function() {
        alert("Opps! can't find the sidebar file to display!");
    });
}

function init_content_section(content_file) {
    $.get(content_file, function(data) {
        $("#content").html(marked(data));
    }, "text").fail(function() {
        alert("Opps! can't find the default index file to display!");
    });
}

function init_back_to_top_button() {
    $("#back_to_top").on("click", function() {
        $("html body").animate({
            scrollTop: 0
        }, 200);
    });
}

function init_edit_button(base_url) {
    $("#edit").on("click", function() {
        var hash = location.hash.replace("#", "/");

        if (hash === "") {
            hash = "/README.md";
        }

        window.open(base_url + hash);
        // open is better than redirecting, as the previous page history with
        // redirect is a bit messed up
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
    return text.replace(/[&\/\\#,+=()$~%.'":*?<>{}\ ]/g, "_");
}

function li_create_linkage(li_tag, header_level) {
    // add custom id and class attributes
    html_safe_tag = replace_symbols(li_tag.text());
    li_tag.attr("id", html_safe_tag);
    li_tag.attr("class", "link");

    // add click listener - on click scroll to relevant header section
    $("#content li#" + li_tag.attr("id")).click(function() {
        // scroll to relevant section
        var header = $("#content h" + header_level + "." + li_tag.attr("id"));
        $('html, body').animate({
            scrollTop: header.offset().top
        }, 200);

        // highlight the relevant section
        original_color = header.css("color");
        header.animate({ color: "#ED1C24", }, 500, function() {
            $(this).animate({color: original_color}, 2500);
        });
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

    // otherwise get the markdown and render it
    $.get(path, function(data) {
        $("#content").html(marked(data));
        create_page_anchors();
    }).fail(show_error);
}

$(document).ready(function() {
    // initialization
    init_sidebar_section("pages/sidebar.md");
    init_content_section("README.md");
    init_back_to_top_button();
    init_edit_button("https://github.com/chutsu/playground/tree/gh-pages");

    // page router
    router();
    $(window).on('hashchange', router);
});
