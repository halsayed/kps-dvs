namespace = '/stream';
let socket = io(namespace);

socket.on('connect', function () {
    socket.emit('my_event', {data: 'I\'m connected!'});
});

socket.on('dashboard_insert', function (msg, cb) {
    for (let key in msg) {
        document.getElementById(key).innerHTML = msg[key] + document.getElementById(key).innerHTML
        console.log('inserted cards in location: ' + key)
    }
    if (cb)
        cb();
});

socket.on('dashboard_update', function (msg, cb) {
    for (var key in msg) {
        let oldCard = document.getElementById(key)
        console.log(oldCard)
        oldCard.outerHTML = msg[key]
        console.log('updated cards: ' + key)
    }
    if (cb)
        cb();
});