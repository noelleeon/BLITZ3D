//https://www.sitepoint.com/community/t/hover-on-desktop-and-click-on-mobile-touch-devices-for-ui-component-content-reveal/404694/4
//https://stackoverflow.com/questions/36695438/detect-click-outside-div-using-javascript
//https://stackoverflow.com/questions/38990163/how-can-i-add-and-remove-an-active-class-to-an-element-in-pure-javascript
document.addEventListener('click', function (event) {
    const menuField = document.querySelector('.menuField');
    const flagMenu = document.querySelector('.flagMenu');

    // Check if the click happened outside of the menuField and flagMenu
    if (menuField === event.target) {
        menuField.classList.toggle('active');
        flagMenu.classList.toggle('active');
    } else if (!menuField.contains(event.target) && !flagMenu.contains(event.target)) {
        // If the click is directly on the menuField, toggle the menu
        menuField.classList.remove('active');
        flagMenu.classList.remove('active');
    }
});

