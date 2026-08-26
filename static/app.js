const map = new ol.Map({

    target: "map",
    Layers : [
    new ol.layer.Tile({
    source: new ol.source.XYZ({
        url: 'https://{a-c}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png',
        tilePixelRatio: 1
    }),
    transition: 0,
    preload: 0
})
    ],

    view: new ol.View({

        center: ol.proj.fromLonLat([
            -2.24,
            47.725
        ]),

        zoom: 11.8,
		constrainResolution: true,
		extent: ol.proj.transformExtent(
			[-2.6, 47.5, -1.9, 47.9],
			'EPSG:4326',
			'EPSG:3857'
		)
    })
});
console.log("app.js chargé");
const idsIsolees = new Set();
const idsProches = new Set();
const idsUniqueMale = new Set();

Promise.all([
    fetch("/femelles-isolees").then(r => r.json()),
    fetch("/femelles-proches").then(r => r.json()),
    fetch("/femelles-unique-male").then(r => r.json())
])
.then(([isolees, proches,uniqueMale]) => {

    isolees.forEach(f => {
        idsIsolees.add(f.femelle_id);
    });

    proches.forEach(f => {
        idsProches.add(f.femelle_id);
    });

    uniqueMale.forEach(f => {
        idsUniqueMale.add(f.femelle_id);
    });

    chargerHoublons();
});
function chargerHoublons() {
fetch("/carte")
.then(response => response.json())
.then(data => {

    console.log("Données recues :", data);
    const features = [];

    data.forEach(h => {
        if(h.sexe === "M") {

           const centre = ol.proj.fromLonLat([
               h.longitude,
               h.latitude
           ]);

           const cercle1km = new ol.Feature({
              geometry: new ol.geom.Circle(
                  centre,
                  1000
              )
         });
         cercle1km.set("type", "cercle1");

         features.push(cercle1km);

         const cercle3km = new ol.Feature({
            geometry: new ol.geom.Circle(
                centre,
                3000
             )
            });

            cercle3km.set("type", "cercle3");

            features.push(cercle3km);
     }
        const feature = new ol.Feature({

            geometry: new ol.geom.Point(
                ol.proj.fromLonLat([
                    h.longitude,
                    h.latitude
                ])
            ),
            id: h.id,
            nom: h.nom,
            sexe: h.sexe,

            isolee: idsIsolees.has(h.id),
            proche: idsProches.has(h.id),
            unique: idsUniqueMale.has(h.id)
        });

        features.push(feature);
    });

    const source = new ol.source.Vector({
        features: features
    });

    const layer = new ol.layer.Vector({

        source: source,

        style: function(feature) {

            const type = feature.get("type");

            if (type === "cercle3") {

               return new ol.style.Style({

                  stroke: new ol.style.Stroke({
                     color: "rgba(120,120,120,0.5)",
                     width: 1
                  }),

                  fill: new ol.style.Fill({
                     color: "rgba(120,120,120,0.3)"
                  })
              });
            }

            if (type === "cercle1") {

               return new ol.style.Style({

                  stroke: new ol.style.Stroke({
                     color: "rgba(120,120,120,0.6)",
                     width: 2
                  }),

                 fill: new ol.style.Fill({
                     color: "rgba(120,120,120,0.4)"
                 })
              });
           }

            const sexe = feature.get("sexe");
            const isolee = feature.get("isolee");
            const proche = feature.get("proche");
            const unique = feature.get("unique");

            let couleur;

            if (isolee) {
                 couleur = "yellow";
            }
            else if (proche) {
                 couleur = "violet";
            }
	    else if (sexe === "M") {
     		couleur = "blue";
	    }
  	    else if (unique) {
		couleur = "red";
	    }
            else {
                couleur = "orange";
            }

            return new ol.style.Style({

                image: new ol.style.Circle({

                    radius: 6,

                    fill: new ol.style.Fill({

                        color: couleur
                    })
                })
            });
        }
    });

    map.addLayer(layer);

});
}
map.on("click", function(evt) {
    const feature = 
        map.forEachFeatureAtPixel(
            evt.pixel,
            f => f
        );

    if (!feature) {
         popup.setPosition(undefined);
         return;
    }

    popupElement.innerHTML =
                "<b>" + feature.get("nom") + "</b></br><br>" +
                "Sexe : " + feature.get("sexe");
    popup.setPosition(evt.coordinate);
});
const popupElement = 
    document.getElementById("popup");

const popup = new ol.Overlay({
    element: popupElement
});

map.addOverlay(popup);
