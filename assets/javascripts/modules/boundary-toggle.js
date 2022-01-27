function LPABoundaryControl ($module, layers) {
  this.$module = $module
  this.layers = layers || []
}

LPABoundaryControl.prototype.init = function (params) {
  this.setupOptions(params)

  this.enabled = this.enabledOnInitialisation
  this.toggleLayers(this.enabled)

  const boundOnClickHandler = this.onClickHandler.bind(this)
  this.$module.addEventListener('click', boundOnClickHandler)

  return this
}

LPABoundaryControl.prototype.addLayer = function (layer) {
  this.layers.push(layer)
}

LPABoundaryControl.prototype.onClickHandler = function (e) {
  const setTo = !this.enabled
  this.toggleLayers(setTo)
  this.enabled = setTo
}

LPABoundaryControl.prototype.switchLayersOff = function () {
  this.layers.forEach(function (layer) {
    if (layer.map.getLayer(layer.name)) {
      layer.map.setLayoutProperty(layer.name, 'visibility', 'none')
    }
  })
}

LPABoundaryControl.prototype.switchLayersOn = function () {
  this.layers.forEach(function (layer) {
    if (layer.map.getLayer(layer.name)) {
      layer.map.setLayoutProperty(layer.name, 'visibility', 'visible')
    }
  })
}

LPABoundaryControl.prototype.toggleLayers = function (enable) {
  if (enable) {
    // switch them on
    this.switchLayersOn()
  } else {
    // switch them off
    this.switchLayersOff()
  }
  this.updateText(enable)
}

LPABoundaryControl.prototype.updateText = function (enabled) {
  this.$module.textContent = (enabled) ? 'Switch LPA boundary off' : 'Switch LPA boundary on'
}

LPABoundaryControl.prototype.setupOptions = function (params) {
  const _params = params || {}
  this.enabledOnInitialisation = _params.enabledOnInitialisation || true
}

export default LPABoundaryControl
