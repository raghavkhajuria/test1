$(document).ready(function() {
    var $input = $('input.form-control.content-group');
    var $send = $('button.btn.bg-teal-400.btn-primary');
    var $chatcontainer = $('ul.media-list.chat-list.content-group');
    var $todaydate = $('li.media.date-step span');
    var session = null;

    // var today = new Date();
    // var month = today.getMonth() + 1;
    // var today_date = today.getFullYear()+"-"+month+"-"+today.getDate();
    // document.getElementById('expiry-date').value = today_date;
    // console.log('INSIDE JS');

    $todaydate.text(new Date());

    new PNotify({
            title: 'New Chat Session',
            text: 'Hello Uber Rider! \n You have begun a new chat.',
            icon: 'icon-bubble-notification',
            addclass: 'bg-info notice-chat'
        });

    // new PNotify({
    //         title: 'Primary notice',
    //         text: 'Check me out! I\'m a notice.',
    //         icon: 'icon-warning22',
    //         addclass: 'bg-info notice-nlp'
    //     });
    //
    // new PNotify({
    //         title: 'Primary notice',
    //         text: 'Check me out! I\'m a notice.',
    //         icon: 'icon-warning22',
    //         addclass: 'bg-info notice-sample'
    //     });

    var form_data = function () {
        var data = {};
        var all_forms = $('.extract').serializeArray();
        for(var i=0; i<all_forms.length; i++) {
            data[all_forms[i].name] = all_forms[i].value;
        }
        console.log(data);
        return data;
    };

    function getTimestamp() {
        time_current = new Date();
        return time_current.getHours() + ':' + time_current.getMinutes();
    }

    function sendMessage(msg, data) {
        console.log(msg);
        if (msg) {
            printMessage("Customer", msg, 0, getTimestamp());
            data = JSON.stringify({
                "message": msg,
                "data": data,
                "sessionId": session
            });
            $input.val('');
            $.ajax({
                type: "POST",
                url: "/api/v1/messages",
                data: data,
                contentType: "application/json; charset=utf-8",
                dataType: "json",
                success: function (data) {
                    printMessage("Bot", data.response, data.score, getTimestamp());
                    displayVariables(data.intent, data.entities);
                    highlight(data.highlighted);
                    session = data.sessionId;
                }
            });
        }
    }

    function displayVariables(intent, entities) {

        var i = document.getElementById('intent-value');
        if (i) {
            i.innerHTML = intent;
        }
        var $entity = $('#entity-value');
        try {
            $entity.empty();
        }
        catch (err){
            console.log(err);
        }

        $entity.append('<ul id="entities"></ul>');
        for (var key in entities) {
            if (entities.hasOwnProperty(key)) {
                $("#entities").append($('<li>' + key + " : " + entities[key] + '</li>'));
            }
        }
    }
    
    function highlight(varnames) {
        $('.extract').find("input").each(function (index, element) {
            if(varnames) {
                if (varnames.indexOf(element.name) > -1) {
                    console.log(element.name);
                    $(element).css('background', '#E6EE9C');
                }
            }
            else {
                $(element).css('background', '#FFF');
            }
        })
    }

    function printMessage(fromUser, message, score, timestamp) {
        if (message) {
            var $msg_block = $('<div class="media-body"></div>'),
                $msg = $('<div class="media-content"></div>').text(message),
                $annotation = $('<span class="media-annotation display-block mt-10"></span>'),
                $img,
                $container;
            console.log($msg);
            if (fromUser == 'Customer') {
                $annotation.text(timestamp);
                $container = $('<li class="media reversed"></li>');
                $img = $('<div class="media-right"><img src="static/images/customer.jpg" class="img-square" alt=""></div>');
                $msg_block.append($msg);
                $msg_block.append($annotation);
                $container.append($msg_block);
                $container.append($img);
            }

            else {
                $annotation.text(timestamp + ", Score: " + score * 100 + "%");
                $img = $('<div class="media-left"><img src="static/images/uber.jpg" class="img-square" alt=""></div>');
                $container = $('<li class="media"></li>');
                $msg_block.append($msg);
                $msg_block.append($annotation);
                $container.append($img);
                $container.append($msg_block);

            }
            $chatcontainer.append($container);
            $chatcontainer.scrollTop($chatcontainer[0].scrollHeight);
            // $chatcontainer.scrollTop();
        }
    }

    $input.on('keydown', function(e) {
        if (e.keyCode === 13) {
            sendMessage($input.val(), form_data());
        }
    });
    $send.click(function() {
        sendMessage($input.val(), form_data());

    });
});