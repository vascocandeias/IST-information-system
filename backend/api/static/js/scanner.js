function secretariatTemplate(secretariat) {
    return `
    <h1>Secretariat: ${secretariat.name}</h1>
    <h4>Information:</h4>
    <p> Location:</p> 
    <p>${secretariat.location}</p><br>
    <p> Description: </p>
    <p>${secretariat.description}</p><br>
    <p> Working Hours: </p>
    <p>${secretariat.hours}</p>
    `;
}

function printDate(event) {
    if(date == event.day) return "";
    date = event.day;
    return `<li> Day: ${event.day}</li>`
}

function printLesson(lesson) {
    return `
    ${printDate(lesson)}
    <p> ${lesson.start} to ${lesson.end}: ${lesson.course.acronym} - ${lesson.info} - ${lesson.course.name}</p>
    `;
}

function printTest(event) {
    return `
    ${printDate(event)}
    <p>${event.start} to ${event.end}</p>
    <ul>
    ${event.courses.map(printCourses).join("")}
    </ul>
    `;
}

function printGeneric(event) {
    return `
    ${printDate(event)}
    <p>${event.start} to ${event.end}: ${event.title}</p>
    `;
}

function printCourses(course) {
    return `
    <li> ${course.acronym} - ${course.name} </li>
    `;
}

function compareDates(a ,b) {
    var dateParts = a.day.split("/");
    var aDate = new Date(+dateParts[2], dateParts[1] - 1, +dateParts[0]); 
    dateParts = b.day.split("/");
    var bDate = new Date(+dateParts[2], dateParts[1] - 1, +dateParts[0]);

    if(aDate - bDate != 0) return aDate - bDate;
    dateParts = a.start.split(":");
    var aHours = dateParts[0];
    var aMinutes = dateParts[1];
    dateParts = b.start.split(":");
    var bHours = dateParts[0];
    var bMinutes = dateParts[1];
    if(aHours != bHours) return aHours - bHours;
    return aMinutes - bMinutes;
}

function lessons(events) {
    return `
    <h3>Lessons</h3>
    <ul>
    ${events.filter(event => event.type == "LESSON").sort(compareDates).map(printLesson).join("")}
    </ul>
    `;
}

function tests(events) {
    return `
    <h3>Tests</h3>
    <ul>
    ${events.filter(event => event.type == "TEST").sort(compareDates).map(printTest).join("<br>")}
    </ul>
    `;
}

function generics(events) {
    return `
    <h3>Generics</h3>
    <ul>
    ${events.filter(event => event.type == "GENERIC").sort(compareDates).map(printGeneric).join("")}
    </ul>
    `;
}

function hasTests(room) {
    for (const event of room.events) {
        if (event.type == "TEST") {
           return true;
        }
    }
    return false;
}

function hasGeneric(room) {
    for (const event of room.events) {
        if (event.type == "GENERIC") {
           return true;
        }
    }
    return false;
}

function hasLessons(room){
    for (const event of room.events) {
        if (event.type == "LESSON") {
           return true;
        }
    }
    return false;
}

function roomTemplate(room) {
    return `
    <h1>Rooms</h1>
    <p>ID: ${room.id}</p>
    <p>Name and Location: ${room.name}, ${room.building}, ${room.topLevelSpace.name}</p>
    ${hasLessons(room) ? lessons(room.events) : ""}
    ${hasTests(room) ? tests(room.events) : ""}
    ${hasGeneric(room) ? generics(room.events) : ""}
    `;
} 

var date;
let scanner = new Instascan.Scanner({ video: document.getElementById('preview'), scanPeriod: 5 });

scanner.addListener('scan', function (content) {
    jQuery.getJSON(content, function(data, status){
        if (data.type == "ROOM")
            document.getElementById("divDestiny").innerHTML = `${roomTemplate(data)}`;
        else if (data.type == "SECRETARIAT")
            document.getElementById("divDestiny").innerHTML = `${secretariatTemplate(data)}`;
        else
            document.getElementById("divDestiny").innerHTML = `<h1>Unknown Type</h1><br><pre>${JSON.stringify(data, null, 2)}</pre>`;
        console.log(data.type)
    });
});

Instascan.Camera.getCameras().then(function (cameras) {
    if (cameras.length > 0) {
        scanner.start(cameras[0]);
    } else {
        console.error('No cameras found.');
    }
}).catch(function (e) {
    console.error(e);
});