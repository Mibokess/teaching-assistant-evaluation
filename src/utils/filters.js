export function getAvg(arr, field) {
  // I really need to code avg myself??
  if (arr.length < 1) return null;
  var total = 0;
  for(var i = 0; i < arr.length; i++) {
      total += arr[i][field];
  }
  return total / arr.length;  
}
