const elements = {

    m_speed_element : null,
    m_engineRPM_element : null,
    m_engineTemperature_element : null,
    
    init : function() {
        this.m_speed_element = document.querySelector("#m_speed");
        this.m_engineRPM_element = document.querySelector("#m_engineRPM");
        this.m_engineTemperature_element = document.querySelector("#m_engineTemperature");
    },

};

const request = {

    telemetry : () => {
        let telemetry_promise = new Promise((resolve, reject) => {
            let request = new XMLHttpRequest();

            request.open("GET", "src/backend/data.py");

            request.onload = () => {
                if (request.status == 200) {
                    resolve(request.response);
                } else {
                    reject("Not able to process.");
                }
            }

            request.send();
        });

        telemetry_promise.then(
            (value) => { 
                value = value.split("HTTP")[0];
                telemetry_data = JSON.parse(value);
                elements.m_speed_element.innerHTML = telemetry_data["m_speed"];
            },
            (error) => { console.log(error); }
        );
    },

};

document.addEventListener("DOMContentLoaded", (event) => {
    elements.init();
});