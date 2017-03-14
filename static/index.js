$(document).ready(function() {
    var $input = $('.chat input[type="text"]');
    var $send = $('.chat input[type="button"]');
    var $chatcontainer = $('.chat #chatZone');
    var session;

    // var today = new Date();
    // var month = today.getMonth() + 1;
    // var today_date = today.getFullYear()+"-"+month+"-"+today.getDate();
    // document.getElementById('expiry-date').value = today_date;
    // console.log('INSIDE JS');

    var form_data = function () {
        var data = {};
        var all_forms = $('#extract').serializeArray();
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
        console.log(intent);
        console.log(entities);

        var i = document.getElementById('intent-value');
        console.log(i);
        if (i) {
            i.innerHTML = intent;
        }
        // console.log($('#intent-value'));

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

        // document.getElementById('#entity-value').innerHTML = $list;
        $('#response-values').show();
    }
    
    function highlight(varnames) {
        if(varnames) {
            $('#extract').find("input").each(function (index, element) {
                if (varnames.indexOf(element.name) > -1) {
                    console.log(element.name);
                    $(element).css('background', '#FC0');
                }
                else {
                    $(element).css('background', '#FFF');
                }
            })
        }
    }

    function printMessage(fromUser, message, score, timestamp) {
        var $user = $('<div id="username">').text(timestamp+ ' ' + fromUser);
        var $msg = $('<div id="message">').text(message);
        var $container;

        if (fromUser == 'Customer'){
            $container = $('<div id="customer">').append($user).append($msg);
        }

        else {
            var $score = $('<div id="score">').text(score);
            $container = $('<div id="bot">').append($user).append($msg).append($score);

        }
        $chatcontainer.append($container);
        $chatcontainer.scrollTop();
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
