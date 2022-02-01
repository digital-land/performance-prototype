
function SelectedEntity (appMap, $panel, $container) {
  this.appMap = appMap // this is an instance of AppMap
  this.$panel = $panel // this should be a panel where entities are displayed
  this.$container = $container // the container that the map and panel are in
}

SelectedEntity.prototype.init = function (params) {
  this.datasetName = params.datasetName
  const that = this
  this.$container.addEventListener('select-entity', function (e) {
    console.log('Container has caught the event', e.detail)
    that.displayEntity(e.detail.entity)
  })

  this.$container.addEventListener('click', function (e) {
    if (!e.target.closest('.entity-item')) {
      that.hideLayer()
    }
  })

  this.createSelectedEntityLayer()
  this.hideLayer()

  const boundPanelClickHandler = this.panelClickHandler.bind(this)
  this.$panel.addEventListener('click', boundPanelClickHandler)

  return this
}

SelectedEntity.prototype.createSelectedEntityLayer = function () {
  console.log(this.appMap)
  this.appMap.createVectorLayer('selectedEntity', 'dl-vectors', this.datasetName, 'line', {
    'line-color': '#000000',
    'line-width': 2
  })
}

SelectedEntity.prototype.displayEntity = function (entityNum) {
  const filter = ['==', 'entity', parseInt(entityNum)]
  console.log('Applying selected', entityNum, filter)
  this.appMap.map.setFilter('selectedEntity', filter)
  this.showLayer()
}

SelectedEntity.prototype.panelClickHandler = function (e) {
  const $entities = Array.prototype.slice.call(this.$panel.querySelectorAll('.entity-item'))
  $entities.forEach(function ($entity) {
    $entity.classList.remove('app-selected-entity')
  })
  if (e.target.closest('.entity-item')) {
    // if entity has been clicked
    const $entity = e.target.closest('.entity-item')
    $entity.classList.add('app-selected-entity')
    console.log($entity.dataset.entity)
    this.$panel.dispatchEvent(new CustomEvent('select-entity', {
      bubbles: true,
      detail: {
        entity: $entity.dataset.entity,
        mapname: this.$panel.dataset.module
      }
    }))
  }
}

SelectedEntity.prototype.hideLayer = function () {
  console.log("hide selected layer visible")
  this.appMap.map.setLayoutProperty('selectedEntity', 'visibility', 'none')
}

SelectedEntity.prototype.showLayer = function () {
  console.log("make selected layer visible")
  this.appMap.map.setLayoutProperty('selectedEntity', 'visibility', 'visible')
}

export default SelectedEntity
