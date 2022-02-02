function FlyToBoundary ($button, appMap) {
  this.$button = $button
  this.appMap = appMap
}

FlyToBoundary.prototype.init = function () {
  this.boundary = undefined

  this.$button.classList.add('js-hidden')

  const boundClickHandler = this.clickHandler.bind(this)
  this.$button.addEventListener('click', boundClickHandler)

  return this
}

FlyToBoundary.prototype.clickHandler = function (e) {
  if (typeof this.boundary !== 'undefined') {
    this.fly()
  } else {
    console.log('No boundary defined')
  }
}

FlyToBoundary.prototype.fly = function () {
  console.log("boundary", this.boundary)
  const bbox = this.appMap.getBBox(this.boundary)
  console.log("bbox", bbox)
  this.appMap.map.fitBounds([[bbox[0], bbox[1]], [bbox[2], bbox[3]]])
}

FlyToBoundary.prototype.setBoundary = function (feature) {
  this.boundary = feature
  this.$button.classList.remove('js-hidden')
}

export default FlyToBoundary
