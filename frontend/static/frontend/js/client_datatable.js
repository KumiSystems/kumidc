function editclient(element) {
    var clientid = $(element).parent().parent().children()[2].innerText;
    document.location.href = clientid + "/edit/";
};