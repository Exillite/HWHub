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

const is_initiator = location.hash === "#init";

if (is_initiator) {
    navigator.mediaDevices
        .getUserMedia({ video: true, audio: true })
        .then((stream) => {
            let is_camera = true;
            let is_mic = true;
            var peer = new SimplePeer({
                initiator: is_initiator,
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

            document.getElementById("marksbtn").hidden = false;

            document
                .getElementById("sendMessage")
                .addEventListener("click", function() {
                    var yourMessage = document.getElementById("yourMessage").value;
                    if (!yourMessage) return;
                    var rqst = {
                        type: "chat-message",
                        is_init: is_initiator,
                        text: yourMessage,
                    };
                    peer.send(JSON.stringify(rqst));

                    let chatArea = document.getElementById("chatArea");
                    var msg = document.createElement("div");
                    chatArea.appendChild(msg);
                    msg.innerHTML += yourMessage;
                    msg.classList.add("message");
                    msg.classList.add("my-message");

                    chatArea.scrollTop = chatArea.scrollHeight;

                    document.getElementById("yourMessage").value = "";
                });

            document
                .getElementById("yourMessage")
                .addEventListener("keydown", function(e) {
                    if (e.code === "Enter") {
                        var yourMessage = document.getElementById("yourMessage").value;
                        if (!yourMessage) return;

                        var rqst = {
                            type: "chat-message",
                            is_init: is_initiator,
                            text: yourMessage,
                        };
                        peer.send(JSON.stringify(rqst));

                        let chatArea = document.getElementById("chatArea");
                        var msg = document.createElement("div");
                        chatArea.appendChild(msg);
                        msg.innerHTML += yourMessage;
                        msg.classList.add("message");
                        msg.classList.add("my-message");

                        chatArea.scrollTop = chatArea.scrollHeight;

                        document.getElementById("yourMessage").value = "";
                    }
                });

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

            document
                .getElementById("chouseHomeworkBtn")
                .addEventListener("click", function() {
                    document.getElementById("editZone").hidden = true;

                    let table = document.getElementById("poinsTabel");
                    table.innerHTML = "";

                    var homework_select = document.getElementById("chouseHomework");
                    var value = homework_select.value;
                    if (!value) return;

                    ws.send(
                        JSON.stringify({ type: "get_submisssion", homework_id: value })
                    );
                });

            let sub_id = "";
            let poinst_len = 0;

            document
                .getElementById("EditSubBtn")
                .addEventListener("click", function() {
                    let dt = { points: [] };
                    for (let i = 0; i < poinst_len; i++) {
                        let point = document.getElementById(`point-${i}`).value / 100;
                        dt.points.push(point);
                    }

                    dt.fine = document.getElementById("fine").value;

                    ws.send(
                        JSON.stringify({
                            type: "edit_submisssion",
                            data: dt,
                            submission_id: sub_id,
                        })
                    );
                });

            ws.onmessage = function(event) {
                console.log(event.data);

                let dt = event.data;
                dt = JSON.parse(dt);
                if (dt.type === "connect_final") {
                    document.getElementById("title").innerHTML = dt.title;
                    ws.send(JSON.stringify({ type: "get_homeworks" }));
                    peer.signal(dt.data);
                }
                if (dt.type === "get_homeworks_response") {
                    let select = document.getElementById("chouseHomework");
                    dt.data.forEach((homework) => {
                        let option = document.createElement("option");
                        option.innerHTML = `${homework.title}`;
                        option.value = homework.id;
                        select.appendChild(option);
                    });
                }
                if (dt.type === "get_submisssion_response") {
                    let table = document.getElementById("poinsTabel");
                    sub_id = dt.data.id;
                    poinst_len = dt.data.homework.points.length;
                    for (let i = 0; i < dt.data.points.length; i++) {
                        let tr = document.createElement("tr");
                        tr.innerHTML = `<th scope="row">${i + 1}</th>
                        <td>${dt.data.homework.points[i]}</td>
                        <td>
                            <input id="point-${i}" value="${
              dt.data.points[i] * 100
            }" type="number" class="form-control" min="0" max="100" onchange="if (this.value > 100) this.value = 100; if (this.value < 0) this.value = 0;">
                        </td>`;
                        table.appendChild(tr);
                    }

                    document.getElementById("fine").value = dt.data.fine;

                    document.getElementById("editZone").hidden = false;
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
                initiator: is_initiator,
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

            document
                .getElementById("sendMessage")
                .addEventListener("click", function() {
                    var yourMessage = document.getElementById("yourMessage").value;
                    if (!yourMessage) return;

                    var rqst = {
                        type: "chat-message",
                        is_init: is_initiator,
                        text: yourMessage,
                    };
                    peer.send(JSON.stringify(rqst));

                    let chatArea = document.getElementById("chatArea");
                    var msg = document.createElement("div");
                    chatArea.appendChild(msg);
                    msg.innerHTML += yourMessage;
                    msg.classList.add("message");
                    msg.classList.add("my-message");

                    chatArea.scrollTop = chatArea.scrollHeight;

                    document.getElementById("yourMessage").value = "";
                });

            document
                .getElementById("yourMessage")
                .addEventListener("keydown", function(e) {
                    if (e.code === "Enter") {
                        var yourMessage = document.getElementById("yourMessage").value;
                        if (!yourMessage) return;

                        var rqst = {
                            type: "chat-message",
                            is_init: is_initiator,
                            text: yourMessage,
                        };
                        peer.send(JSON.stringify(rqst));

                        let chatArea = document.getElementById("chatArea");
                        var msg = document.createElement("div");
                        chatArea.appendChild(msg);
                        msg.innerHTML += yourMessage;
                        msg.classList.add("message");
                        msg.classList.add("my-message");

                        chatArea.scrollTop = chatArea.scrollHeight;

                        document.getElementById("yourMessage").value = "";
                    }
                });

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
                    document.getElementById("title").innerHTML = dt.title;
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