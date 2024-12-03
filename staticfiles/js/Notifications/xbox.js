// notifications.js
function createNotification(message) {
    const notificationContainer = document.createElement('div');
    notificationContainer.className = 'notification-container';

    notificationContainer.innerHTML = `
        <div class="achievement">
            <div class="animation">
                <div class="circle">
                    <div class="img trophy_animate trophy_img">
                        <img class="trophy_1" src="/static/img/notifications/trophy_full.svg"/>
                        <img class="trophy_2" src="/static/img/notifications/trophy_no_handles.svg">
                    </div>
                    <div class="img xbox_img">
                        <img src="/staticimg/notifications/xbox.svg"/>
                    </div>
                </div>
                <div class="banner-outer">
                    <div class="banner">
                        <div class="achieve_disp">
                            <span class="unlocked xbox_span" style="font-size: 10pt !important;">Достижение разблокировано:</span>
                            <div class="score_disp">
                                <span class="achiev_name xbox_span" style="font-weight: bold">
                                    ${message}
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;

    document.body.appendChild(notificationContainer);

    setTimeout(() => {
        const circle = notificationContainer.querySelector('.circle');
        const banner = notificationContainer.querySelector('.banner');
        const achieveDisp = notificationContainer.querySelector('.achieve_disp');

        circle.classList.add('circle_animate');
        banner.classList.add('banner-animate');
        achieveDisp.classList.add('achieve_disp_animate');

        setTimeout(() => {
            circle.classList.remove('circle_animate');
            banner.classList.remove('banner-animate');
            achieveDisp.classList.remove('achieve_disp_animate');
            document.body.removeChild(notificationContainer);
        }, 12000);
    }, 100);
}

document.addEventListener("DOMContentLoaded", () => {
    const notificationMessages = document.querySelectorAll('.notification-message');
    notificationMessages.forEach(element => {
        createNotification(element.textContent);
        element.remove();  // Удаляем элемент после создания уведомления
    });
});

document.addEventListener("DOMContentLoaded", () => {
    console.log("DOM loaded in base.html");
    const debugMessages = document.getElementById('debug-messages');
    if (debugMessages) {
        console.log("Debug messages:", debugMessages.innerHTML);
    }
    const notificationMessages = document.querySelectorAll('.notification-message');
    console.log("Found notification messages:", notificationMessages.length);
    notificationMessages.forEach(element => {
        console.log("Creating notification for:", element.textContent);
        createNotification(element.textContent);
        element.remove();
    });
});
