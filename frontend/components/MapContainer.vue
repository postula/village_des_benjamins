<template>
  <div style="width: 100%; height: 100%;">
    <div ref="map-root" style="width: 100%; height: 100%;"/>
  </div>
</template>

<script>
import View from 'ol/View';
import Map from 'ol/Map';
import Overlay from 'ol/Overlay';
import TileLayer from 'ol/layer/Tile';
import VectorLayer from 'ol/layer/Vector';
import OSM from 'ol/source/OSM';
import Vector from 'ol/source/Vector';
import Feature from 'ol/Feature';
import Point from 'ol/geom/Point';
import {Style, Icon} from 'ol/style';
import {toSize} from 'ol/size';
import {fromLonLat} from 'ol/proj';


import 'ol/ol.css';


export default {
  name: "MapContainer",
  mounted() {
    const lat_lon = [5.50624, 50.63867]
    const iconFeature = new Feature({
      geometry: new Point(fromLonLat(lat_lon)),
    });
    const iconStyle = new Style({
      image: new Icon({
        anchor: [0.5, 1],
        anchorXUnits: 'fraction',
        anchorYUnits: 'fraction',
        src: require('@/assets/brand/marker.png'),
        scale: 0.1
      })
    });
    iconFeature.setStyle(iconStyle)
    const vectorSource = new Vector({
      features: [iconFeature],
    });
    const vectorLayer = new VectorLayer({
      source: vectorSource,
    })
    const rasterLayer = new TileLayer({
      source: new OSM()
    });

    const map = new Map({
      target: this.$refs['map-root'],
      layers: [
          rasterLayer, vectorLayer
      ],
      view: new View({
        zoom: 16,
        maxZoom: 18,
        center: fromLonLat(lat_lon),
      })
    });
  }
}
</script>

<style scoped>

</style>
