/* global maplibregl, turf, DLMaps */

function AppMap (mapId, $zoomControls) {
  this.mapId = mapId
  this.$zoomControls = $zoomControls
}

AppMap.prototype.init = function (params) {
  this.setupOptions(params)
  this.initialMapLoaded = false
  this.sources = []
  this.layers = []
  this.datasetLayers = {}
  this.clickableLayers = undefined
  this._highlightFeatures = false

  // create the maplibre map
  this.map = this.createMap()

  this._container = this.map.getContainer().closest(this.mapContainerSelector)

  const boundOnMapLoad = this.onMapLoad.bind(this)
  this.map.on('load', boundOnMapLoad)

  return this
}

AppMap.prototype.addClickListener = function (clickHandler) {
  const boundClickHandler = clickHandler.bind(this)
  this.map.on('click', boundClickHandler)
}

AppMap.prototype.highlightFeaturesOn = function () {
  this._highlightFeatures = true
  const highlightLayers = []
  // a filter to show zero features?
  const initFilter = ['==', 'entity', '']
  for (const dataset in this.datasetLayers) {
    console.log(dataset)
    const layerId = dataset + 'Highlight' + 'Fill'
    if (this.layers.indexOf(layerId) === -1) {
      // create layer
      this.createVectorLayer(layerId, this.sourceName, dataset, 'fill', {
        'fill-color': '#912b88',
        'fill-opacity': 0.5
      })
      this.map.setFilter(layerId, initFilter)
      console.log(this.layers)
      highlightLayers.push(layerId)
    }
  }
  const that = this
  this.map.on('click', function (e) {
    const bbox = [[e.point.x - 5, e.point.y - 5], [e.point.x + 5, e.point.y + 5]]
    console.log('clickable', that.clickableLayers)
    const features = that.intersectBBox(bbox, that.clickableLayers) // here is not working!
    const entities = features.map(function (f) { return f.properties.entity })
    console.log('entities', entities, features)
    if (entities.length) {
      highlightLayers.forEach(function (hlLayer) {
        that.map.setFilter(hlLayer, ['match', ['get', 'entity'], entities, true, false])
      })
    } else {
      highlightLayers.forEach(function (hlLayer) {
        that.map.setFilter(hlLayer, initFilter)
      })
    }
  })
}

AppMap.prototype.addSource = function (name, tiles, minZoom, maxZoom) {
  const sourceName = name || this.sourceName
  if (!this.map.getSource(sourceName)) {
    this.map.addSource(sourceName, {
      type: 'vector',
      tiles: tiles || [this.vectorSource],
      minzoom: minZoom || this.minMapZoom,
      maxzoom: maxZoom || this.maxMapZoom
    })
    this.sources.push(sourceName)
  }
}

AppMap.prototype.createMap = function () {
  const map = new maplibregl.Map({
    container: this.mapId, // container id
    style: this.baseTileStyleFilePath, // open source tiles
    center: this.mapStartPos.center, // starting position [lng, lat]
    zoom: this.mapStartPos.zoom // starting zoom
  })

  // add fullscreen control
  if (this.allowFullscreen) {
    map.addControl(new maplibregl.FullscreenControl({
      container: document.querySelector(this.mapContainerSelector)
    }), 'bottom-left')
  }
  return map
}

// should this be part of component that extends AppMap?
AppMap.prototype.createDatasetLayers = function (dataset, _type, filter, options) {
  console.log("firing")
  const _options = Object.assign({
    style: this.styleProperties
  }, options || {})
  let layers
  // polygons need a fill and a line
  if (_type === 'polygon') {
    layers = [this.createFillLayer(dataset, _options), this.createLineLayer(dataset, _options)]
    if (filter) {
      this.setFilter([dataset + 'Fill', dataset + 'Line'], filter)
    }
  } else if (_type === 'point') {
    layers = [this.createCircleLayer(dataset, _options)]
    if (filter) {
      this.setFilter([dataset], filter)
    }
  }
  this.datasetLayers[dataset] = layers
}

AppMap.prototype.createCircleLayer = function (layerId, options) {
  const layerOptions = Object.assign({
    source: this.sourceName,
    sourceLayer: layerId,
    style: {
      colour: this.styleProperties.colour,
      opacity: this.styleProperties.opacity,
      weight: this.styleProperties.weight
    }
  }, options || {})
  this.createVectorLayer(layerId, layerOptions.source, layerOptions.sourceLayer, 'circle', {
    'circle-color': layerOptions.style.colour,
    'circle-opacity': layerOptions.style.opacity,
    'circle-radius': {
      base: 1.5,
      stops: [
        [6, 1],
        [22, 180]
      ]
    },
    'circle-stroke-color': layerOptions.style.colour,
    'circle-stroke-width': layerOptions.style.weight
  })
  return layerId
}

AppMap.prototype.createFillLayer = function (layerId, options) {
  // NEEDS Polyfill for IE
  const layerOptions = Object.assign({
    source: this.sourceName,
    sourceLayer: layerId,
    style: {
      colour: this.styleProperties.colour,
      opacity: this.styleProperties.opacity
    }
  }, options || {})
  // create fill layer
  const layerName = layerId + 'Fill'
  this.createVectorLayer(layerName, layerOptions.source, layerOptions.sourceLayer, 'fill', {
    'fill-color': layerOptions.style.colour,
    'fill-opacity': layerOptions.style.opacity
  })
  return layerName
}

AppMap.prototype.createLineLayer = function (layerId, options) {
  // NEEDS Polyfill for IE
  const layerOptions = Object.assign({
    source: this.sourceName,
    sourceLayer: layerId,
    style: {
      colour: this.styleProperties.colour,
      weight: this.styleProperties.weight
    }
  }, options || {})
  const layerName = layerId + 'Line'
  this.createVectorLayer(layerId + 'Line', layerOptions.source, layerOptions.sourceLayer, 'line', {
    'line-color': layerOptions.style.colour,
    'line-width': layerOptions.style.weight
  })
  return layerName
}

AppMap.prototype.createVectorLayer = function (layerId, source, sourceLayer, _type, paintOptions) {
  this.map.addLayer({
    id: layerId,
    type: _type,
    source: source,
    'source-layer': sourceLayer,
    paint: paintOptions
  })
  this.layers.push(layerId)
}

AppMap.prototype.defaultClickHandler = function (e) {
  const bbox = [[e.point.x - 5, e.point.y - 5], [e.point.x + 5, e.point.y + 5]]
  const clickableLayers = this.getClickableLayers()
  const features = this.intersectBBox(bbox, clickableLayers)
  console.log('clicked features', features)
}

AppMap.prototype.flyToDataset = function (dataset, filter, options) {
  const _options = Object.assign({
    source: this.sourceName,
    returnFeatures: false
  }, options || {})

  const matchedFeatures = this.map.querySourceFeatures(_options.source, {
    filter: filter,
    sourceLayer: dataset
  })

  if (matchedFeatures.length) {
    const collection = turf.featureCollection(matchedFeatures)
    const envelope = turf.envelope(collection)
    const bbox = envelope.bbox
    this.map.fitBounds([[bbox[0], bbox[1]], [bbox[2], bbox[3]]])
  }

  if (_options.returnFeatures) {
    // will contain duplicates
    return matchedFeatures
  }
}

AppMap.prototype.getClickableLayers = function () {
  if (this.clickableLayers) {
    return this.clickableLayers
  }
  return this.getDefaultClickableLayers()
}

AppMap.prototype.getDefaultClickableLayers = function () {
  const clickableLayers = []
  for (const dataset in this.datasetLayers) {
    if (Object.prototype.hasOwnProperty.call(this.datasetLayers, dataset)) {
      console.log(dataset)
      if (this.datasetLayers[dataset].length === 1) {
        clickableLayers.push(dataset)
      } else {
        clickableLayers.push(dataset + 'Fill')
      }
    }
  }
  return clickableLayers
}

AppMap.prototype.getDatasetLayers = function () {
  return this.datasetLayers
}

AppMap.prototype.getSources = function () {
  return this.sources
}

AppMap.prototype.getMap = function () {
  return this.map
}

AppMap.prototype.intersectBBox = function (bbox, layers) {
  return this.map.queryRenderedFeatures(bbox, {
    layers: layers
  })
}

AppMap.prototype.onMapLoad = function () {
  console.log('map has loaded')
  this.initialMapLoaded = true

  // add source to map
  this.addSource()
  this.zoomControl = new DLMaps.ZoomControls(this.$zoomControls, this.map, this.map.getZoom()).init({})

  // do we want to be able to click on the features?
  if (this.clickableFeatures) {
    this.addClickListener(this.defaultClickHandler)
  }

  const that = this
  if (this.onLoadCallback) {
    // const boundOnLoadCallback = this.onLoadCallback.bind(this);
    this.onLoadCallback(that)
  }
}

AppMap.prototype.hasMapLoaded = function () {
  return this.initialMapLoaded
}

// customise which layers are clickable
// provide array of lyaer names (ids)
AppMap.prototype.setClickableLayers = function (layers) {
  this.clickableLayers = layers
}

AppMap.prototype.setFilter = function (layerName, filter) {
  const that = this
  if (Array.isArray(layerName)) {
    layerName.forEach(function (l) {
      that.map.setFilter(l, filter)
    })
  } else {
    // TO DO: check if layer exists first
    this.map.setFilter(layerName, filter)
  }
}

AppMap.prototype.setupOptions = function (params) {
  params = params || {}
  this.mapStartPos = params.mapStartPos || {
    center: [0, 52],
    zoom: 6
  }
  this.baseTileStyleFilePath = params.baseTileStyleFilePath || './base-tile.json'
  this.mapContainerSelector = params.mapContainerSelector || '.dl-map__wrapper'
  this.allowFullscreen = params.allowFullscreen || true
  this.sourceName = params.sourceName || 'dl-vectors'
  this.vectorSource = params.vectorSource || 'https://datasette-tiles.digital-land.info/-/tiles/dataset_tiles/{z}/{x}/{y}.vector.pbf'
  this.minMapZoom = params.minMapZoom || 5
  this.maxMapZoom = params.maxMapZoom || 15

  // this will only work if all 3 are passed in
  this.styleProperties = params.styleProperties || {
    colour: '#003078',
    opacity: 0.5,
    weight: 2
  }
  this.clickableFeatures = params.clickableFeatures || true
  this.onLoadCallback = params.onLoadCallback || undefined

  this.baseURL = params.baseURL || 'https://digital-land.github.io'
  // this.flyToDataset = params.flyToDataset || 'local-authority-district';
  this.popupWidth = params.popupWidth || '260px'
  this.popupMaxListLength = params.popupMaxListLength || 10
}

export default AppMap
