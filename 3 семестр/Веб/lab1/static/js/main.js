const resultTable = document.getElementById("resultsTable") 

document.getElementById("pointForm").addEventListener("submit", async function (ev) {
    ev.preventDefault();

    const params = new URLSearchParams({
        x: x,
        y: y,
        listR: listR,
    });
    console.log("Sending request with params:", params.toString());

    const response = await fetch(`/fcgi-bin/FastCGIApp.jar/calculate?${params.toString()}`, {
        method: 'GET',
        headers: {
            'Accept': 'application/json'
        }
    });

    const results = {
        x: x,
        y: y,
        r: null,
        execTime: "",
        time: "",
        result: false,
    };
    
    if (response.ok) {
        const result = await response.json();

        drawGraph();  
        for (let i = 0; i < listR.length; i++) {
            const newRow = resultTable.insertRow(-1);
            const rowX = newRow.insertCell(0);
            const rowY = newRow.insertCell(1);
            const rowR = newRow.insertCell(2);
            const rowResult = newRow.insertCell(3);
            const rowTime = newRow.insertCell(4);
            const rowExecTime = newRow.insertCell(5);

            results.r = listR[i].toString(),
            results.result = result.results[i].toString();
            results.time = new Date(result.now).toLocaleString();
            results.execTime = `${result.time} ns`;
     
            drawPoint(x, y, result.results[i], listR[i]);

            const prevResults = JSON.parse(localStorage.getItem("results") || "[]");
            localStorage.setItem("results", JSON.stringify([...prevResults, results]));

            rowX.innerText = results.x.toString();
            rowY.innerText = results.y.toString();
            rowR.innerText = results.r.toString();
            rowTime.innerText = results.time;
            rowExecTime.innerText = results.execTime;
            rowResult.innerText = results.result;
        }
    } else {
        const newRow = resultTable.insertRow(-1);
        const rowX = newRow.insertCell(0);
        const rowY = newRow.insertCell(1);
        const rowR = newRow.insertCell(2);
        const rowResult = newRow.insertCell(3);
        const rowTime = newRow.insertCell(4);
        const rowExecTime = newRow.insertCell(5);
        if (response.status === 400) {
            const result = await response.json();

            results.time = new Date(result.now).toLocaleString();
            results.execTime = "N/A";
            results.result = `error: ${result.message}`;

            rowTime.innerText = results.time;
            rowExecTime.innerText = results.execTime;
            rowResult.innerText = results.result;
        } else {
            results.time = "N/A";
            results.execTime = "N/A";
            results.result = "error"

            rowTime.innerText = results.time;
            rowExecTime.innerText = results.execTime;
            rowResult.innerText = results.result;
        }
    }
});


function addResultToTable(x, y, r, result, requestTime, executionTime) {
    const tbody = document.getElementById('resultsBody');
    
    const row = tbody.insertRow(-1);
    

    row.insertCell(0).textContent = x;
    row.insertCell(1).textContent = y;
    row.insertCell(2).textContent = r;
    
    const resultCell = row.insertCell(3);
    resultCell.textContent = result ? 'Попадание' : 'Непопадание';
    resultCell.className = result ? 'result-hit' : 'result-miss';
    
    row.insertCell(4).textContent = requestTime;
    row.insertCell(5).textContent = executionTime;
    
    row.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

