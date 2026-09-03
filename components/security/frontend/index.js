const Streamlit = window.Streamlit;

let violationSent = false;


// ========================================
// COMPONENT READY
// ========================================

function sendReady() {
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight(1);
}


// ========================================
// SEND VIOLATION
// ========================================

function reportViolation(reason) {

    if (violationSent) {
        return;
    }

    violationSent = true;

    Streamlit.setComponentValue({
        violation: true,
        reason: reason
    });
}


// ========================================
// INTERVIEW TAB / PAGE CHANGE
// ========================================

document.addEventListener(
    "visibilitychange",
    function () {

        // Interview tab/page background me chala gaya
        if (document.visibilityState === "hidden") {

            reportViolation(
                "Candidate left the interview page"
            );

        }

    }
);


// ========================================
// STREAMLIT RENDER
// ========================================

Streamlit.events.addEventListener(
    Streamlit.RENDER_EVENT,
    sendReady
);


sendReady();