(function () {
  'use strict'

  feather.replace()
})()

async function onBtnDeleteAllTickets() {
    if (confirm("Clear test data, by deleting tickets?")) {
        await callApi('/api/delete_all_tickets')
    }
}

async function onBtnDeleteAllTicketsAndUsers() {
    if (confirm("Clear test data, by deleting tickets and users?")) {
        await callApi('/api/delete_all')
    }
}

async function onBtnPostReply() {
    alert('looks like ' + inferCurrentTicketId())
}

async function onBtnSetStatus(newStatus) {
   
}

async function onBtnSetTags(newStatus) {
   
}

function inferCurrentTicketId() {
    let currentLocation = window.location.toString()
    const pts = currentLocation.split('tickets/')
    if (pts.length <= 1) {
        alert('Could not find current ticket id')
        throw new Error('Could not find current ticket id')
    }
    if (Number.isNaN(parseInt(pts[1]))) {
        alert('Could not parse current ticket id')
        throw new Error('Could not parse current ticket id')
    }
    
    return parseInt(pts[1])
}

async function callApi(endpoint, method='post', payload=undefined) {
    let options = {
        method: method,
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(payload || {})      
    }

    let response = await fetch(endpoint, options)
    if (response.status >= 200 && response.status < 300) {
        alert('API call succeeded.')
        setTimeout(()=>location.reload(), 100)
    } else {
        let output = await response.text();
        alert('API call failed, details: ' + output)
        setTimeout(()=>location.reload(), 100)
    }
}
