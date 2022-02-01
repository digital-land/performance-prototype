# Maps info

We are using maplibre.

We have set up a tile server for our data.
The tile server has a named layer for every dataset.

### Add a source first

You need to set up the source first.

```
$map.addSource(<sourceName>, {
  type: 'vector',
  tiles: <vectorSource>,
  minzoom: <minZoom>,
  maxzoom: <maxZoom>
})
```

**$map** - is your maplibre map
**sourceName** - we usually call it `dl-vectors`
**vectorSource** - uri to our tile server `https://datasette-tiles.digital-land.info/-/tiles/dataset_tiles/{z}/{x}/{y}.vector.pbf`
**minZoom** - our tiles work up to zoom level 5
**maxZoom** - our tiles work down to zoom level 15

The max and min zoom levels can be changed via the [tiles builder](https://github.com/digital-land/tiles-builder).

### Showing complete dataset

The easiest thing to show is complete datasets

To do so you need to add a maplibre layer that specifies the source layer you are interested in. The source layer will be the same as the dataset id, e.g. `conservation-area`.

The general way to add a layer is

```
map.addLayer({
  id: <layerId>,
  type: <_type>,
  source: <source>,
  'source-layer': <sourceLayer>,
  paint: <paintOptions>
})
```

**layerId** - is the name you are giving it. E.g. `conservation-areaFill`
**_type** - the type of layer, can be `fill`, `line`, `circle`. See mapbox documentation for more [layer type options](https://docs.mapbox.com/mapbox-gl-js/style-spec/layers/)
**source** - this is the name you gave the source, in our case, usually `dl-vectors`
**sourceLayer** - the name of the layer at source, usually the dataset id
**paintOptions** - these differ depending on the type of layer 

#### Displaying point data

We have some datasets that are point data, such as `brownfield-land`. To display that data it's best to create a `circle` layer.

E.g.
```
map.addLayer({
  id: 'brownfield-land`,
  type: 'circle',
  source: 'dl-vectors',
  'source-layer': 'brownfield-land`,
  paint: {
    'circle-color': '#003078',
    'circle-opacity': 0.5,
    'circle-radius': {
      base: 1.5,
      stops: [
        [6, 1],
        [22, 180]
      ]
    },
    'circle-stroke-color': '#003078',
    'circle-stroke-width': 2
  }
})
```

TICKET - sizing points dynamically
Ticket - polygon svg for dataset icons on national map

#### Displaying shapes

Most of the datasets are shape data. To display this we need to use `fill`, `line` or both type layers.

Normally, to display a filled in shape with a border create 2 layers, a `fill` and a `line`.

For example, a Fill for `conservation-area`
```
map.addLayer({
  id: 'conservation-areaFill',
  type: 'fill',
  source: 'dl-vectors',
  'source-layer': 'conservation-area',
  paint: {
    'fill-color': '#003078',
    'fill-opacity': 0.5
  }
})
```

and a Line
For example, for `conservation-area`
```
map.addLayer({
  id: 'conservation-areaLine',
  type: 'line',
  source: 'dl-vectors',
  'source-layer': 'conservation-area',
  paint: {
    'line-color': '#003078',
    'line-width': 2
  }
})
```

### Showing subsets

You can show subsets of data but using filters. Filters are applied to a layer. So if you are filtering the data for a shape dataset annd have added 2 layers (a fill and a line) to display it then you'll have to filter each layer too.

Filters uses mapbox's [expression syntax](https://docs.mapbox.com/help/tutorials/mapbox-gl-js-expressions/).
```
$map.setFilter(layerName, filter)
```

#### Get all entities published by an LPA

Firstly, you will need the entity number for the organisation. For example, Lambeth is 192.

Then you can use that to look for the entities that have been published by that LPA, using the universally available `organisation_entity` property.

```
filter = ['==', 'organisation-entity', '192']
$map.setFilter('conservation-areaFill', filter)
```

You can use similar filters to this example to match on any available properties.

#### Showing a single entity

There are cases where you might want to filter to display a single entity. For example, if you have a layer you are using to highlight an entity the user clicks on.

You need to get the entity number of the entity you'd like to show.

Then you can set a filter to only show that entity. E.g.
```
filter = ['match', ['get', 'entity'], [entity_number], true, false]
$map.setFilter('conservation-areaFill', filter)
```

This will check to see if all the potential entities match the one you are interested in. If it does it'll show it. If not, it won't.

#### Showing a set of entities

You can use the above technique to show a set of entities too. The only difference is you provide a list of entity numbers instead of one. For example, I do this to show all the entities inside a boundary - I fetch the list from the API, then provide an array of the entity numbers to a filter like this.

```
filter = ['match', ['get', 'entity'], ['332098', '3330871', '345145', ...], true, false]
$map.setFilter('conservation-areaFill', filter)
```

I wonder if this particular filter might be better to use a [within filter](https://docs.mapbox.com/mapbox-gl-js/style-spec/expressions/#within) but it works for now.

Note, only the vectors tiles that would be displayed in the current map viewport are fetched from the tile server.

### Hiding layers

You might need to do this if you are toggling a layer on or off after you've already added the layer to the map.

One approach is to remove the layer with `removelayer(<id>)`. And then when reenabling it you can use `addLayer({})` as you did before.

An alternative is to hide the layer visually. You can do this may setting one of the layout properties for the layer. 

For example to hide a layer
```
map.setLayoutProperty(layerName, 'visibility', 'none')
```

And to show it
```
map.setLayoutProperty(layerName, 'visibility', 'visible')
```
