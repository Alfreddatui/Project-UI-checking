//Object to store the upload CSV
var datahit = {
  HITId : [],
  PictureURL: [],
  destinID: [],
  AssignmentId:[],
  Approve:[],
  Reject:[],
  x1: [],
  width: [],
  y1: [],
  height: [],
  label: []
};

//To keep track the index of the HIT
var count = 1;

///////////////////////////////////////////Additional Feature/////////////////////////////////////////////
document.addEventListener('keydown', function(event) {
    if(event.keyCode == 13) {
        acceptButton();
        console.log("Accepting");
    }
    else if(event.keyCode == 46) {
        declineButton();
        console.log("Declining");
    }
    else if(event.keyCode == 37) {
        backButton();
        console.log("Going back");
    }

    else if(event.keyCode == 39) {
        nextButton();
        console.log("Go Next");
    }
});

////////////////////////////////////////All the buttons////////////////////////////////////////////////////////////////////////////
function acceptButton() {
  if (count >= datahit.HITId.length-1) {
    document.getElementById('previewimage').src = datahit.destinID[count];
    document.getElementById('category').innerHTML = datahit.label[count];
    document.getElementById('bbox').style.left = datahit.x1[count]+"px";
    document.getElementById('bbox').style.top = datahit.y1[count]+"px";
    document.getElementById('bbox').style.width = datahit.width[count] + "px";
    document.getElementById('bbox').style.height = datahit.height[count] + "px";
    document.getElementById('number').innerHTML = count+1;
    datahit.Approve[count]='x';
    datahit.Reject[count]='';
  } else {
    count+=1;
    document.getElementById('number').innerHTML = count;  
    document.getElementById('previewimage').src = datahit.destinID[count];
    document.getElementById('category').innerHTML = datahit.label[count];
    document.getElementById('bbox').style.left = datahit.x1[count]+"px";
    document.getElementById('bbox').style.top = datahit.y1[count]+"px";
    document.getElementById('bbox').style.width = datahit.width[count] + "px";
    document.getElementById('bbox').style.height = datahit.height[count] + "px";
    datahit.Approve[count-1]='x';
    datahit.Reject[count-1]='';
  }
  console.log('x');
  
}

function declineButton() {
  if (count >= datahit.HITId.length-1) {
    document.getElementById('previewimage').src = datahit.destinID[count];
    document.getElementById('category').innerHTML = datahit.label[count];
    document.getElementById('bbox').style.left = datahit.x1[count]+"px";
    document.getElementById('bbox').style.top = datahit.y1[count]+"px";
    document.getElementById('bbox').style.width = datahit.width[count] + "px";
    document.getElementById('bbox').style.height = datahit.height[count] + "px";
    document.getElementById('number').innerHTML = count+1;
    datahit.Reject[count]='The bounding box(es) that you have drawn do not adhere to our criteria. The bounding box(es) are either trucanted, drawn on objects that are incorrectly orientated(meaning the clothing articles may be folded or not facing the front), or labelled with the wrong category. Label the bounding boxes as "NotIncluded" if you are unsure of which category the clothing article belongs to, or the clothing article is folded or is not squarely facing the front(we still check the result)';
    datahit.Approve[count]='';
  } else {
    count+=1;
    document.getElementById('number').innerHTML = count; 
    document.getElementById('previewimage').src = datahit.destinID[count];
    document.getElementById('category').innerHTML = datahit.label[count];
    document.getElementById('bbox').style.left = datahit.x1[count]+"px";
    document.getElementById('bbox').style.top = datahit.y1[count]+"px";
    document.getElementById('bbox').style.width = datahit.width[count]+ "px";
    document.getElementById('bbox').style.height = datahit.height[count] + "px";
    datahit.Reject[count-1]='The bounding box(es) that you have drawn do not adhere to our criteria. The bounding box(es) are either trucanted, drawn on objects that are incorrectly orientated(meaning the clothing articles may be folded or not facing the front), or labelled with the wrong category. Label the bounding boxes as "NotIncluded" if you are unsure of which category the clothing article belongs to, or the clothing article is folded or is not squarely facing the front(we still check the result)';
    datahit.Approve[count-1]='';
  }
  console.log(datahit.Reject[count-1])
}

function backButton() {
  if (count === 1) {
    document.getElementById('previewimage').src = datahit.destinID[count];
    document.getElementById('category').innerHTML = datahit.label[count];
    document.getElementById('bbox').style.left = datahit.x1[count]+"px";
    document.getElementById('bbox').style.top = datahit.y1[count]+"px";
    document.getElementById('bbox').style.width = datahit.width[count] + "px";
    document.getElementById('bbox').style.height = datahit.height[count] + "px";
  } else {
    count-=1;
    document.getElementById('number').innerHTML = count; 
    document.getElementById('previewimage').src = datahit.destinID[count];
    document.getElementById('category').innerHTML = datahit.label[count];
    document.getElementById('bbox').style.left = datahit.x1[count]+"px";
    document.getElementById('bbox').style.top = datahit.y1[count]+"px";
    document.getElementById('bbox').style.width = datahit.width[count] + "px";
    document.getElementById('bbox').style.height = datahit.height[count] + "px";
  }
}

function nextButton() {
  if (datahit.Approve[count] != "" || datahit.Reject[count] != ""){
    if (count >= datahit.HITId.length-1) {
      document.getElementById('previewimage').src = datahit.destinID[count];
      document.getElementById('category').innerHTML = datahit.label[count];
      document.getElementById('bbox').style.left = datahit.x1[count]+"px";
      document.getElementById('bbox').style.top = datahit.y1[count]+"px";
      document.getElementById('bbox').style.width = datahit.width[count] + "px";
      document.getElementById('bbox').style.height = datahit.height[count] + "px";
    } else {
      count+=1;
      document.getElementById('number').innerHTML = count; 
      document.getElementById('previewimage').src = datahit.destinID[count];
      document.getElementById('category').innerHTML = datahit.label[count];
      document.getElementById('bbox').style.left = datahit.x1[count]+"px";
      document.getElementById('bbox').style.top = datahit.y1[count]+"px";
      document.getElementById('bbox').style.width = datahit.width[count] + "px";
      document.getElementById('bbox').style.height = datahit.height[count] + "px";
    }
  }
}

function csvButton() {
  let fileName = 'Resultcsv.csv';
  var data = [];
  let lengthID = datahit.HITId.length;
  for (var number =0; number < lengthID; number++) {
    data[number] = [];
    var check = checksame(data,datahit.HITId[number]);
    if (check) {
      if (data[check][2] === 'x' && datahit.Approve[number] != 'x') {
        data[check][2] = '';
        data[check][3] = datahit.Reject[number];
      }
    }
    data[number][0] = datahit.HITId[number];
    data[number][1] = datahit.AssignmentId[number];
    data[number][2] = datahit.Approve[number];
    data[number][3] = datahit.Reject[number];
  }
  // console.log(data);
  exportToCsv(fileName,data);
}

function checksame(data,HITId) {
  for (var row=0; row<data.length; row++){
    if (data[row][0] === HITId){
      return row; //row is the index of the HITId which is equal to true
    } 
  }
  return false;

}
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



//////////////////////////////////////////////////////////////////////////////FUNCTION TO READ THE CSV//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function handleFiles(files) {
  // Check for the various File API support.
  if (window.FileReader) {
      // FileReader are supported.
      getAsText(files[0]);
      document.getElementById('inputfile').style.display="none";
  } else {
      alert('FileReader are not supported in this browser.');
  }
}

function getAsText(fileToRead) {
  var reader = new FileReader();
  // Read file into memory as UTF-8      
  reader.readAsText(fileToRead);
  // Handle errors load
  reader.onload = loadHandler;
  reader.onerror = errorHandler;
}

function loadHandler(event) {
  var csv = event.target.result;
  processData(csv);
}

function processData(csv) {
    var allTextLines = csv.split(/\r\n|\n/);
    var lines = [];
    for (var i=0; i<allTextLines.length; i++) {
        var data = allTextLines[i].split(';');
            var tarr = [];
            for (var j=0; j<data.length; j++) {
                tarr.push(data[j]);
            }
            lines.push(tarr);
    }
  listoflines(lines);
}

function errorHandler(evt) {
  if(evt.target.error.name == "NotReadableError") {
      alert("Canno't read file !");
  }
}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


//////////////////////////////////////Putting the Data on our object//////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function listoflines(l_array) {
    let arraylength = l_array.length;
    for (var i=0; i<l_array.length-1; i++) {
        temp = l_array[i][0].split(",");
        datahit.HITId.push(temp[4]);
        datahit.AssignmentId.push(temp[5]);
        datahit.Reject.push(temp[7]);
        datahit.Approve.push(temp[6]);
        datahit.PictureURL.push(temp[2]);
        datahit.x1.push(temp[8]);
        datahit.width.push(temp[10]);
        datahit.y1.push(temp[9]);
        datahit.height.push(temp[11]);
        datahit.label.push(temp[12]);
        datahit.destinID.push(temp[13]);

    }
    document.getElementById('previewimage').src = datahit.destinID[count];
    document.getElementById('category').innerHTML = datahit.label[count];
    document.getElementById('bbox').style.left = datahit.x1[count]+"px";
    document.getElementById('bbox').style.top = datahit.y1[count]+"px";
    document.getElementById('bbox').style.width = datahit.width[count]+"px";
    document.getElementById('bbox').style.height = datahit.height[count]+"px";
    document.getElementById('number').innerHTML = count;
    document.getElementById('totals').innerHTML =  datahit.HITId.length;  
    console.log(datahit.Approve)
}//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////









//////////////////////////////////////DOWNLOAD CSV FILES//////////////////////////////////////////////////////////////////////////

function exportToCsv(filename, rows) {
        var processRow = function (row) {
            var finalVal = '';
            for (var j = 0; j < row.length; j++) {
                var innerValue = row[j] === null ? '' : row[j].toString();
                if (row[j] instanceof Date) {
                    innerValue = row[j].toLocaleString();
                };
                var result = innerValue.replace(/"/g, '""');
                if (result.search(/("|,|\n)/g) >= 0)
                    result = '"' + result + '"';
                if (j > 0)
                    finalVal += ',';
                finalVal += result;
            }
            return finalVal + '\n';
        };

        var csvFile = '';
        for (var i = 0; i < rows.length; i++) {
            csvFile += processRow(rows[i]);
        }

        var blob = new Blob([csvFile], { type: 'text/csv;charset=utf-8;' });
        if (navigator.msSaveBlob) { // IE 10+
            navigator.msSaveBlob(blob, filename);
        } else {
            var link = document.createElement("a");
            if (link.download !== undefined) { // feature detection
                // Browsers that support HTML5 download attribute
                var url = URL.createObjectURL(blob);
                link.setAttribute("href", url);
                link.setAttribute("download", filename);
                link.style.visibility = 'hidden';
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }
        }
    }
///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////