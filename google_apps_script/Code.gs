/**
 * Handles GET requests from Home Assistant REST sensor.
 * Returns the first unanswered question row from the active Google Sheet.
 */
function doGet(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  const data = sheet.getDataRange().getValues();
  
  // Find the first row (starting from row 2) with a question in column A and empty answer in column B (ID 1)
  for (let i = 1; i < data.length; i++) {
    if (data[i][0] !== "" && data[i][1] === "") {
      return ContentService.createTextOutput(JSON.stringify({
        row: i + 1,
        question: data[i][0]
      })).setMimeType(ContentService.MimeType.JSON);
    }
  }
  
  // If all questions are answered, return the last question
  const lastRow = data.length;
  return ContentService.createTextOutput(JSON.stringify({
    row: lastRow,
    question: data[lastRow - 1][0]
  })).setMimeType(ContentService.MimeType.JSON);
}

/**
 * Handles POST requests from the Python Serial Bridge.
 * Logs incoming student answers (e.g., ID1 / ID01 -> A/B) into the active question row.
 */
function doPost(e) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheets()[0];
  const data = sheet.getDataRange().getValues();
  const payload = JSON.parse(e.postData.contents);
  const studentId = payload.student_id.toUpperCase();
  const answer = payload.answer;
  
  const colMap = {
    "ID1": 2, "ID01": 2,
    "ID2": 3, "ID02": 3,
    "ID3": 4, "ID03": 4,
    "ID4": 5, "ID04": 5,
    "ID5": 6, "ID05": 6
  };
  
  const col = colMap[studentId];
  if (!col) {
    return ContentService.createTextOutput("Unknown student ID").setMimeType(ContentService.MimeType.TEXT);
  }
  
  // Locate the first active question row where column A has text and column B (ID 1) is empty
  let targetRow = data.length;
  for (let i = 1; i < data.length; i++) {
    if (data[i][0] !== "" && data[i][1] === "") {
      targetRow = i + 1;
      break;
    }
  }
  
  sheet.getRange(targetRow, col).setValue(answer);
  
  return ContentService.createTextOutput("OK").setMimeType(ContentService.MimeType.TEXT);
}
