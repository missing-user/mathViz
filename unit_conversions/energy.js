const input = document.getElementById('input')
const output = document.getElementById('output')

const comparisions = {
  'approximate kinetic energy of a flying mosquito': 1.6e-7,
  'acoustic energy of a whisper': 1e-2,
  'a single calorie': 4.19,
  'energy of an amateur punch': 40,
  'as much as a handgun bullet': 400,
  'an F1 grenade': 251000,
  'a kg of TNT': 4.2e6,
  'enough TNT to blow up a church': 5.021e7,
  'released by total fission of 1g of Uranium': 8.2e10,
  'little Boy nuclear bomb': 6e13,
  'released by a hurricane in one second': 62e14,
  'impact energy of the forming Meteor Crater, Arizona': 1e16,
  'US yearly energy production': 8.357e19,
  'yearly global energy production': 5.369e20,
  'gravitational binding energy of the earth': 2.49e32,
  'energy released by the sun in a year': 1.21e34,
  'supernova explosion': 10e44,
  "mass-energy equivalent of the galaxy's visible mass": 4e58,
  'estimated mass-energy equivalent of ALL OF the universe': 2e69
}

var values = []
var descriptions = []

for (let [key, value] of Object.entries(comparisions)) {
  values.push(value)
  descriptions.push(key)
}
console.log(values)


function convert() {
  var energy = parseFloat(input.value)
  console.log('order of mag: ', orderOfMagnitude(energy));
  var compe = findClosest(energy)
  console.log('comparision value', values[compe]);
  var desc = descriptions[compe]
  compe = values[compe]

  output.textContent = (energy / compe).toPrecision(2) + ' times ' + desc
}

function findClosest(ref) {
  var index = getKindaClose(ref)
  var before = values[index]
  var after = values[index + 1]

  console.log('before diff', orderOfMagnitude(before / ref));
  console.log('after diff', orderOfMagnitude(after / ref));
  if (Math.abs(orderOfMagnitude(before / ref)) >= Math.abs(orderOfMagnitude(after / ref))) {
    return index + 1;
  } else {
    return index;
  }
}

function orderOfMagnitude(inp) {
  return Math.round(Math.log10(inp));
}

function getKindaClose(ref) {
  for (var i = 0; i < values.length; i++) {
    if (values[i] > ref)
      return i - 1;
  }
  return values.length - 1;
}
