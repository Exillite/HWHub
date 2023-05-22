function onopenMiro(share_link) {
    // https://miro.com/app/board/uXjVMQ_om3w=/?share_link_id=870054768292
    let lnk = share_link.split("/");
    var is_next = false;
    let board_id;
    lnk.forEach((element) => {
        if (is_next) {
            board_id = element;
            is_next = false;
        }

        if (element === "board") {
            is_next = true;
        }
    });

    console.log(board_id);

    var miroFrame = document.getElementById("miroFrame");
    var miroInputFrame = document.getElementById("miroInputFrame");

    // miroFrame.src = `https://miro.com/app/live-embed/${board_id}/?embedAutoplay=true`
}

onopenMiro(
    "https://miro.com/app/board/uXjVMQ_om3w=/?share_link_id=870054768292"
);

if (location.hash === "#init") {
    navigator.mediaDevices
        .getUserMedia({ video: true, audio: true })
        .then((stream) => {
            let is_camera = true;
            let is_mic = true;
            var peer = new SimplePeer({
                initiator: location.hash === "#init",
                trickle: false,
                stream: stream,
            });
            var ws = new WebSocket(
                `ws://${location.hostname}/api/ws/${location.search.split("=")[1]}`
            );

            var localVideo = document.getElementById("localVideo");

            if (this && "srcObject" in this) {
                localVideo.srcObject = stream;
            } else {
                localVideo.srcObject = stream;
            }

            localVideo.play();

            peer.on("signal", function(data) {
                ws.send(
                    JSON.stringify({ type: "new_connection", data: JSON.stringify(data) })
                );
            });

            document.getElementById('sendMessage').addEventListener('click', function() {
                var yourMessage = document.getElementById('yourMessage').value
                if (!yourMessage) return;
                var rqst = {
                    type: 'chat-message',
                    is_init: location.hash === "#init",
                    text: yourMessage,
                }
                peer.send(JSON.stringify(rqst))

                let chatArea = document.getElementById('chatArea')
                var msg = document.createElement('div')
                chatArea.appendChild(msg)
                msg.innerHTML += yourMessage
                msg.classList.add('message')
                msg.classList.add('my-message')

                chatArea.scrollTop = chatArea.scrollHeight;

                document.getElementById('yourMessage').value = ''
            })

            document.getElementById('yourMessage').addEventListener("keydown", function(e) {
                if (e.code === "Enter") {
                    var yourMessage = document.getElementById('yourMessage').value
                    if (!yourMessage) return;

                    var rqst = {
                        type: 'chat-message',
                        is_init: location.hash === "#init",
                        text: yourMessage,
                    }
                    peer.send(JSON.stringify(rqst))

                    let chatArea = document.getElementById('chatArea')
                    var msg = document.createElement('div')
                    chatArea.appendChild(msg)
                    msg.innerHTML += yourMessage
                    msg.classList.add('message')
                    msg.classList.add('my-message')

                    chatArea.scrollTop = chatArea.scrollHeight;

                    document.getElementById('yourMessage').value = ''
                }
            })

            peer.on("data", function(data) {
                let rsp = JSON.parse(data);
                let chatArea = document.getElementById("chatArea");
                var msg = document.createElement("div");
                chatArea.appendChild(msg);
                msg.innerHTML += rsp.text;
                msg.classList.add("message");

                chatArea.scrollTop = chatArea.scrollHeight;
            });

            document.getElementById("mutebtn").addEventListener("click", function() {
                if (is_mic) {
                    stream.getTracks().forEach(function(track) {
                        if (track.kind === "audio") track.enabled = false;
                    });
                    document.getElementById("mutebtn").classList.add("footer-btn-off");
                    document
                        .getElementById("mutebtn")
                        .getElementsByTagName("img")[0].src = "assets/Icons/AudioOff.png";
                } else {
                    stream.getTracks().forEach(function(track) {
                        if (track.kind === "audio") track.enabled = true;
                    });
                    document.getElementById("mutebtn").classList.remove("footer-btn-off");
                    document
                        .getElementById("mutebtn")
                        .getElementsByTagName("img")[0].src = "assets/Icons/Audio.png";
                }
                is_mic = !is_mic;
            });

            document
                .getElementById("novideobtn")
                .addEventListener("click", function() {
                    if (is_camera) {
                        stream.getTracks().forEach(function(track) {
                            if (track.kind === "video") track.enabled = false;
                        });
                        document
                            .getElementById("novideobtn")
                            .classList.add("footer-btn-off");
                        document
                            .getElementById("novideobtn")
                            .getElementsByTagName("img")[0].src =
                            "assets/Icons/CameraOff.png";

                        localVideo.hidden = true;
                    } else {
                        stream.getTracks().forEach(function(track) {
                            if (track.kind === "video") track.enabled = true;
                        });
                        document
                            .getElementById("novideobtn")
                            .classList.remove("footer-btn-off");
                        document
                            .getElementById("novideobtn")
                            .getElementsByTagName("img")[0].src = "assets/Icons/Camera.png";
                        localVideo.hidden = false;
                    }
                    is_camera = !is_camera;
                });

            peer.on("stream", function(stream) {
                var video = document.getElementById("remouteVideo");

                // video.src = window.URL.createObjectURL(stream)

                if ("srcObject" in this) {
                    video.srcObject = stream;
                } else {
                    video.srcObject = stream;
                }

                video.play();
            });

            ws.onmessage = function(event) {
                console.log(event.data);

                let dt = event.data;
                dt = JSON.parse(dt);
                if (dt.type === "connect_final") {
                    peer.signal(dt.data);
                }
            };
        })
        .catch((err) => {
            console.log(err);
        });
} else {
    navigator.mediaDevices
        .getUserMedia({ video: true, audio: true })
        .then((stream) => {
            let is_camera = true;
            let is_mic = true;
            var peer = new SimplePeer({
                initiator: location.hash === "#init",
                trickle: false,
                stream: stream,
            });
            var ws = new WebSocket(
                `ws://${location.hostname}/api/ws/${location.search.split("=")[1]}`
            );

            var localVideo = document.getElementById("localVideo");

            if (this && "srcObject" in this) {
                localVideo.srcObject = stream;
            } else {
                localVideo.srcObject = stream;
            }

            localVideo.play();

            peer.on("signal", function(data) {
                ws.send(
                    JSON.stringify({ type: "connect", data: JSON.stringify(data) })
                );
            });

            // peer.on('data', function(data) {
            //     document.getElementById('messages').textContent += data + '\n'
            // })

            document.getElementById('sendMessage').addEventListener('click', function() {
                var yourMessage = document.getElementById('yourMessage').value
                var rqst = {
                    type: 'chat-message',
                    is_init: location.hash === "#init",
                    text: yourMessage,
                }
                peer.send(JSON.stringify(rqst))

                let chatArea = document.getElementById('chatArea')
                var msg = document.createElement('div')
                chatArea.appendChild(msg)
                msg.innerHTML += yourMessage
                msg.classList.add('message')
                msg.classList.add('my-message')

                chatArea.scrollTop = chatArea.scrollHeight;

                document.getElementById('yourMessage').value = ''
            })

            document.getElementById('yourMessage').addEventListener("keydown", function(e) {
                if (e.code === "Enter") {
                    var yourMessage = document.getElementById('yourMessage').value
                    var rqst = {
                        type: 'chat-message',
                        is_init: location.hash === "#init",
                        text: yourMessage,
                    }
                    peer.send(JSON.stringify(rqst))

                    let chatArea = document.getElementById('chatArea')
                    var msg = document.createElement('div')
                    chatArea.appendChild(msg)
                    msg.innerHTML += yourMessage
                    msg.classList.add('message')
                    msg.classList.add('my-message')

                    chatArea.scrollTop = chatArea.scrollHeight;

                    document.getElementById('yourMessage').value = ''
                }
            })

            peer.on("data", function(data) {
                let rsp = JSON.parse(data);
                let chatArea = document.getElementById("chatArea");
                var msg = document.createElement("div");
                chatArea.appendChild(msg);
                msg.innerHTML += rsp.text;
                msg.classList.add("message");

                chatArea.scrollTop = chatArea.scrollHeight;
            });

            peer.on("stream", function(stream) {
                var video = document.getElementById("remouteVideo");

                // video.src = window.URL.createObjectURL(stream)

                if ("srcObject" in this) {
                    video.srcObject = stream;
                } else {
                    video.srcObject = stream;
                }

                video.play();
            });

            document.getElementById("mutebtn").addEventListener("click", function() {
                if (is_mic) {
                    stream.getTracks().forEach(function(track) {
                        if (track.kind === "audio") track.enabled = false;
                    });
                    document.getElementById("mutebtn").classList.add("footer-btn-off");
                    document
                        .getElementById("mutebtn")
                        .getElementsByTagName("img")[0].src = "assets/Icons/AudioOff.png";
                } else {
                    stream.getTracks().forEach(function(track) {
                        if (track.kind === "audio") track.enabled = true;
                    });
                    document.getElementById("mutebtn").classList.remove("footer-btn-off");
                    document
                        .getElementById("mutebtn")
                        .getElementsByTagName("img")[0].src = "assets/Icons/Audio.png";
                }
                is_mic = !is_mic;
            });

            document
                .getElementById("novideobtn")
                .addEventListener("click", function() {
                    if (is_camera) {
                        stream.getTracks().forEach(function(track) {
                            if (track.kind === "video") track.enabled = false;
                        });
                        document
                            .getElementById("novideobtn")
                            .classList.add("footer-btn-off");
                        document
                            .getElementById("novideobtn")
                            .getElementsByTagName("img")[0].src =
                            "assets/Icons/CameraOff.png";
                        localVideo.hidden = true;
                    } else {
                        stream.getTracks().forEach(function(track) {
                            if (track.kind === "video") track.enabled = true;
                        });
                        document
                            .getElementById("novideobtn")
                            .classList.remove("footer-btn-off");
                        document
                            .getElementById("novideobtn")
                            .getElementsByTagName("img")[0].src = "assets/Icons/Camera.png";
                        localVideo.hidden = false;
                    }
                    is_camera = !is_camera;
                });

            ws.onmessage = function(event) {
                console.log(event.data);
                // console.log(event);

                let dt = event.data;
                dt = JSON.parse(dt);
                if (dt.type === "connect_response") {
                    peer.signal(dt.data);
                }
            };

            ws.onopen = (event) => {
                ws.send(JSON.stringify({ type: "connection_request" }));
            };
        })
        .catch((err) => {
            console.log(err);
        });
}