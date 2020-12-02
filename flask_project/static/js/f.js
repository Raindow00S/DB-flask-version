/// <reference path="jquery-1.9.1.min.js" />

$(function () {
    $(".Js_closeBtn").click(function () {
        $(".adduser,.f_delete").fadeOut(200);
    });
    $(".Js_edit").click(function () {

        var inst_id = $(this).parents("tr").find("#inst-id");    // 将有仪器ID的表格存为变量
        $("#input-inst-id").val(inst_id.text()); // 将表格中的文本放到输入框里
        inst_id.css('background-color', 'red');   // 将变量所表示的元素背景变为红色，debug用的，让你知道变量到底存了哪个元素

        var inst_name = $(this).parents("tr").find("#inst-name");   // 仪器名称
        $("#input-inst-name").val(inst_name.text());

        var inst_type = $(this).parents("tr").find("#inst-type");   // 型号规格
        $("#input-inst-type").val(inst_type.text());

        var inst_desc = $(this).parents("tr").find("#inst-desc");   // 功能描述
        $("#input-inst-desc").val(inst_desc.text());

        $(".adduser").fadeIn(200);
    });
    $(".Js_delete").click(function () {
        $(".f_delete").fadeIn(200);
    });

    // 编辑-确定
    $("#edit-submit").click(function () {
        $(this).css('background-color', 'red');
        var inst_id = $("#input-inst-id").val();    // 取输入框的值
        var inst_name = $("#input-inst-name").val();
        var inst_type = $("#input-inst-type").val();
        var inst_desc = $("#input-inst-desc").val();
        // 向后端传数据
        $.ajax({
            async: "false",
            type: "POST",
            url: "/demo",   // 要传给的url
            data: { // 要传的数据
                "inst_id": inst_id,
                "inst_name": inst_name,
                "inst_type": inst_type,
                "inst_desc": inst_desc
            },
            success: function (data) {
                alert('仪器信息编辑成功！');
                window.location.reload();
            }
        });
    });

        //左侧菜单
        //$(".Js_MenuList").click(function () {
        //    if ($(".Js_leftBox").css("left") == "0px") {
        //        $(".Js_RightBox").css("width", "96%");
        //        $(".Js_leftBox").animate({ left: "-13%" }, 200);
        //        $(".Js_RightBox").animate({ left: "0" }, 200);
        //    } else {
        //        $(".Js_RightBox").css("width", "83%");
        //        $(".Js_leftBox").animate({ left: "0" }, 200);
        //        $(".Js_RightBox").animate({ left: "13%" }, 200);

        //    }
        //});

        //返回顶部
        $(window).on("scroll", function () {
            if ($(this).scrollTop() > 300) {
                $('.back-to-top').fadeIn();
            } else {
                $('.back-to-top').fadeOut();
            }
        });

        $('.back-to-top').on("click", function () {
            $("html, body").animate({ scrollTop: 0 }, 600);
            return false;
        });

    });