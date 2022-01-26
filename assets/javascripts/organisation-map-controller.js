/* global DLMaps, maplibregl, turf */
function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function OrgMapController($layerControlsList, $zoomControls, datasets, organisationId, statisticalGeography) {
  this.$layerControlsList = $layerControlsList;
  this.$zoomControls = $zoomControls;
  this.datasets = datasets || [];
  this.organisationId = organisationId;
  this.statisticalGeography = statisticalGeography;
}

OrgMapController.prototype.init = function (params) {
  // check maplibregl is available
  // if not return
  this.setupOptions(params); // create the maplibre map

  this.map = this.createMap(); // perform setup once map is loaded

  var boundSetup = this.setup.bind(this);
  this.map.on('load', boundSetup); // run debugging code

  this.debug();
  return this;
};

OrgMapController.prototype.createMap = function () {
  var mappos = DLMaps.Permalink.getMapLocation(6, [0, 52]);
  var map = new maplibregl.Map({
    container: this.mapId,
    // container id
    style: this.baseTileStyleFilePath,
    // open source tiles?
    center: [0, 52],
    // starting position [lng, lat]
    zoom: 6// starting zoom

  });
  DLMaps.Permalink.setup(map); // add fullscreen control

  map.addControl(new maplibregl.FullscreenControl({
    container: document.querySelector(this.mapContainerSelector)
  }), 'bottom-left');
  return map;
};

OrgMapController.prototype.setup = function () {
  // add source to map
  this.addSource();
  this.zoomControl = new DLMaps.ZoomControls(this.$zoomControls, this.map, this.map.getZoom()).init({}); // setup layers

  // create layers based on datasets provided
  this.layers = this.createAllFeatureLayers()
  console.log(this.layers)

  // if organisation id has been provided then set the filters
  // must be added after layers have been set up
  if (this.organisationId) {
    this.setFilters();
  }

  var boundClickHandler = this.clickHandler.bind(this);
  this.map.on('click', boundClickHandler); 
  
  // if org id provided and flyToDataset
  if (this.organisationId) {
    this.registerInitialFlyTo();
  }
};

OrgMapController.prototype.getDatasets = function () {
  console.log("datasets", this.datasets)
  return this.datasets.map(function (d) {
    //return d.name;
    return d.dataset
  });
};

OrgMapController.prototype.addSource = function () {
  var sourceName = this.sourceName;
  this.map.addSource(sourceName, {
    type: 'vector',
    tiles: [this.vectorSource],
    minzoom: this.minMapZoom,
    maxzoom: this.maxMapZoom
  });
};

OrgMapController.prototype.createVectorLayer = function (layerId, datasetName, _type, paintOptions) {
  this.map.addLayer({
    id: layerId,
    type: _type,
    source: this.sourceName,
    'source-layer': datasetName,
    paint: paintOptions
  })
}

OrgMapController.prototype.createAllFeatureLayers = function () {
  const datasetLayers = {}
  const that = this
  const styleProps = {
    colour: '#003078',
    opacity: 0.5,
    weight: 2
  }

  this.datasets.forEach(function (dataset) {
    let layers

    console.log("attempting to add layer for", dataset)

    if (dataset.type === 'point') {
      // set options for points as circle markers
      const paintOptions = {
        'circle-color': styleProps.colour,
        'circle-opacity': styleProps.opacity,
        'circle-radius': {
          base: 1.5,
          stops: [
            [6, 1],
            [22, 180]
          ]
        },
        'circle-stroke-color': styleProps.colour,
        'circle-stroke-width': styleProps.weight
      }
      // create the layer
      that.createVectorLayer(dataset.dataset, dataset.dataset, 'circle', paintOptions)
      layers = [dataset.dataset]
    } else {
      // create fill layer
      that.createVectorLayer(dataset.dataset + 'Fill', dataset.dataset, 'fill', {
        'fill-color': styleProps.colour,
        'fill-opacity': styleProps.opacity
      })
      // create line layer
      that.createVectorLayer(dataset.dataset + 'Line', dataset.dataset, 'line', {
        'line-color': styleProps.colour,
        'line-width': styleProps.weight
      })
      layers = [dataset.dataset + 'Fill', dataset.dataset + 'Line']
    }
    datasetLayers[dataset.dataset] = layers
  })
  return datasetLayers
}


OrgMapController.prototype.setFilters = function () {
  var that = this;
  var datasets = this.datasets.filter(function (d) {
    return d.dataset !== 'local-authority-district';
  });
  console.log(datasets)
  datasets.forEach(function (d) {
    if (d.type === 'point') {
      // single filter for points
      that.map.setFilter(d.dataset, ['==', 'organisation', that.organisationId]);
    } else {
      // filter both fills and lines for polygons
      that.map.setFilter(d.dataset + 'Fill', ['==', 'organisation', that.organisationId]);
      that.map.setFilter(d.dataset + 'Line', ['==', 'organisation', that.organisationId]);
    }
  }); // local authority district filter on statistical geography

  // this.map.setFilter('local-authority-districtFill', ['in', this.statisticalGeography, ['get', 'slug']]);
  // this.map.setFilter('local-authority-districtLine', ['in', this.statisticalGeography, ['get', 'slug']]);
}; // uses the feature's sourceLayer to return the set colour for data of that type


OrgMapController.prototype.getFillColour = function (feature) {
  var l = this.layerControlsComponent.getControlByName(feature.sourceLayer);
  var styles = this.layerControlsComponent.getStyle(l);
  return styles.colour;
}; // sometimes the same feature can appear multiple times in a list for features
// return only unique features


OrgMapController.prototype.removeDuplicates = function (features) {
  var uniqueIds = [];
  console.log("features", features);
  return features.filter(function (feature) {
    if (uniqueIds.indexOf(feature.id) === -1) {
      uniqueIds.push(feature.id);
      return true;
    }

    return false;
  });
};

OrgMapController.prototype.createFeaturesPopup = function (features) {
  var wrapperOpen = '<div class="dl-popup">';
  var wrapperClose = '</div>';
  var headingHTML = "<h3 class=\"dl-popup-heading\">".concat(features.length, " features selected</h3>");

  if (features.length > this.popupMaxListLength) {
    headingHTML = '<h3 class="dl-popup-heading">Too many features selected</h3>';
    var tooMany = "<p class=\"govuk-body-s\">You clicked on ".concat(features.length, " features.</p><p class=\"govuk-body-s\">Zoom in or turn off layers to narrow down your choice.</p>");
    return wrapperOpen + headingHTML + tooMany + wrapperClose;
  }

  var itemsHTML = '<ul class="dl-popup-list">\n';
  var that = this;
  features.forEach(function (feature) {
    var featureType = capitalizeFirstLetter(feature.sourceLayer).replaceAll('-', ' ');
    var fillColour = that.getFillColour(feature);
    var itemHTML = ["<li class=\"dl-popup-item\" style=\"border-left: 5px solid ".concat(fillColour, "\">"), "<p class=\"secondary-text govuk-!-margin-bottom-0 govuk-!-margin-top-0\">".concat(featureType, "</p>"), '<p class="dl-small-text govuk-!-margin-top-0 govuk-!-margin-bottom-0">', "<a href=\"".concat(this.baseURL).concat(feature.properties.slug, "\">").concat(feature.properties.name, "</a>"), '</p>', '</li>'];
    itemsHTML = itemsHTML + itemHTML.join('\n');
  });
  itemsHTML = headingHTML + itemsHTML + '</ul>';
  return wrapperOpen + itemsHTML + wrapperClose;
};

OrgMapController.prototype.clickHandler = function (e) {
  var map = this.map;
  console.log('click location', e);
  var bbox = [[e.point.x - 5, e.point.y - 5], [e.point.x + 5, e.point.y + 5]];
  var that = this; // returns a list of layer ids we want to be 'clickable'

  var clickableLayers = []
  this.datasets.forEach(function (dataset) {
    console.log("layers", that.layers)
    console.log("dataset", dataset)
    console.log("dataset layers", that.layers[dataset.dataset], that.layers[dataset.dataset].length)
    
    if (that.layers[dataset.dataset].length == 1) {
      clickableLayers.push(dataset.dataset)
    } else {
      clickableLayers.push(dataset.dataset + "Fill")
    }
  });

  console.log('Clickable layers: ', clickableLayers);
  var features = map.queryRenderedFeatures(bbox, {
    layers: clickableLayers
  });
  var coordinates = e.lngLat;
  console.log("clicked features", features)
  // var popupHTML = that.createFeaturesPopup(this.removeDuplicates(features));
  // var popup = new maplibregl.Popup({
  //   maxWidth: this.popupWidth
  // }).setLngLat(coordinates).setHTML(popupHTML).addTo(map);
};

OrgMapController.prototype.flyToFeatureSet = function (dataset, filter, returnFeatures) {
  let layerName = dataset
  if (this.layers[dataset].length > 1) {
    layerName = dataset + "Fill"
  }
  var matchedFeatures = this.map.querySourceFeatures(this.sourceName, {
    filter: filter,
    sourceLayer: dataset
  });

  if (matchedFeatures.length) {
    var collection = turf.featureCollection(matchedFeatures);
    var envelope = turf.envelope(collection);
    var bbox = envelope.bbox;
    this.map.fitBounds([[bbox[0], bbox[1]], [bbox[2], bbox[3]]]);
  }

  if (returnFeatures) {
    return matchedFeatures;
  }
};

OrgMapController.prototype.registerInitialFlyTo = function () {
  var flownTo = false;
  var that = this;
  var sourceName = this.flyToDataset + '-source';
  console.log("here", sourceName)
  this.map.on('sourcedata', function (e) {
    if (!flownTo) {
      if (that.map.getSource(sourceName) && that.map.isSourceLoaded(sourceName)) {
        var filter = that.flyToDataset === 'local-authority-district' ? ['in', that.statisticalGeography, ['get', 'slug']] : ['==', 'organisation', that.organisationId];
        var features = that.flyToFeatureSet(that.flyToDataset, filter, true);

        if (features.length) {
          flownTo = true;
        }
      }
    }
  });
};

OrgMapController.prototype.getMap = function () {
  return this.map;
};

OrgMapController.prototype.setupOptions = function (params) {
  params = params || {};
  this.mapId = params.mapId || 'mapid';
  this.mapContainerSelector = params.mapContainerSelector || '.dl-map__wrapper';
  this.sourceName = params.sourceName || 'dl-vectors';
  this.vectorSource = params.vectorSource || 'https://datasette-tiles.digital-land.info/-/tiles/dataset_tiles/{z}/{x}/{y}.vector.pbf';
  this.minMapZoom = params.minMapZoom || 5;
  this.maxMapZoom = params.maxMapZoom || 15;
  this.baseURL = params.baseURL || 'https://digital-land.github.io';
  this.baseTileStyleFilePath = params.baseTileStyleFilePath || './base-tile.json';
  this.flyToDataset = params.flyToDataset || 'local-authority-district';
  this.popupWidth = params.popupWidth || '260px';
  this.popupMaxListLength = params.popupMaxListLength || 10;
};

OrgMapController.prototype.debug = function () {
  var that = this;

  function countFeatures(layerName) {
    var l = that.map.getLayer(layerName);

    if (l) {
      return that.map.queryRenderedFeatures({
        layers: [layerName]
      }).length;
    }

    return 0;
  }

  this.map.on('moveend', function (e) {
    console.log('moveend');
    console.log('Brownfield', countFeatures('brownfield-land'));
    console.log('LA boundaries', countFeatures('local-authority-districtFill'));
    console.log('conservation area', countFeatures('conservation-areaFill'));
  });
};

window.OrgMapController = OrgMapController