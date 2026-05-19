
import { useState, useRef, useEffect } from "react";

import Map, { Marker } from "react-map-gl/mapbox";
import type { MapRef } from "react-map-gl/mapbox";
import type { MapMouseEvent } from "react-map-gl/mapbox";

import "mapbox-gl/dist/mapbox-gl.css";

import { SearchBox } from "@mapbox/search-js-react";
import { useParams } from "react-router-dom";

const MAPBOX_TOKEN: string = import.meta.env.VITE_API_KEY ?? "";

export default function GymSearcher() {

  const { id } = useParams();

  const mapRef = useRef<MapRef>(null);

  // default location
  const [marker, setMarker] = useState({
    latitude: -33.8688,
    longitude: 151.2093,
  });

  const [radius, setRadius] = useState(10);

  const [numGyms, setNumGyms] = useState(5);

  // set location to physical
  useEffect(() => {
  navigator.geolocation.getCurrentPosition((pos) => {
    setMarker({
      latitude: pos.coords.latitude,
      longitude: pos.coords.longitude,
    });
  });
}, []);

  // when user clicks map
  const clickMap = (e: MapMouseEvent) => {

    const lat = e.lngLat.lat;
    const lng = e.lngLat.lng;

    setMarker({
      latitude: lat,
      longitude: lng,
    });

    console.log("Clicked:", lat, lng);
  };

  const requestGyms = async (
    longitude: number,
    latitude: number,
    limit: number,
    radius: number
  ) => {

    try {
      const response = await fetch(`http://localhost:8000/${id}/search`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          longitude,
          latitude,
          limit,
          radius
        }),
      });

      const data = await response.json();

      console.log("Server response:", data);

    } catch (error) {
      console.error("Error:", error);
    }
  }

  return (
    <div className="w-full h-screen relative">
      <h2 className="text-left">
        Enter location to search for gyms!
      </h2>

      <div>
        <input type="range" 
          min='0' 
          max="50" 
          step='1' 
          value={radius}
          className='slider' 
          id="myRange" 
          onChange={(e)=> {
            setRadius(Number(e.target.value))
          }}/>
        <p>
          {radius}km
        </p>
      </div>

      <div>
        <input
          type="range"
          min={1}
          max={10}
          value={numGyms}
          onChange={(e) =>
            setNumGyms(Number(e.target.value))
          }
          className="accent-blue-500"
        />
        <p>
          Search for {numGyms} gyms
        </p>
      </div>

      <div className="absolute z-10 w-96 m-4">

        <SearchBox
          accessToken={MAPBOX_TOKEN}
          options={{
            proximity: {
              lng: marker.longitude,
              lat: marker.latitude,
            },
          }}
          onRetrieve={(res) => {

            const feature = res.features[0];

            const [lng, lat] =
              feature.geometry.coordinates;

            setMarker({
              latitude: lat,
              longitude: lng,
            });

            mapRef.current?.flyTo({
              center: [lng, lat],
              zoom: 14,
            });

            console.log("Search:", lat, lng);
          }}
        />

      </div>

      <Map
        ref={mapRef}
        mapboxAccessToken={MAPBOX_TOKEN}
        initialViewState={{
          latitude: marker.latitude,
          longitude: marker.longitude,
          zoom: 12,
        }}
        mapStyle="mapbox://styles/mapbox/dark-v11"
        style={{
          width: "75%",
          height: "50%",
        }}
        onClick={clickMap}
      >

        <Marker
          latitude={marker.latitude}
          longitude={marker.longitude}
        />

      </Map>

      <button 
        onClick={() =>
          requestGyms(
            marker.longitude,
            marker.latitude,
            radius,
            radius
          )
        }
        className="w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-lg font-semibold transition"
      >
        Get Gyms
      </button>

    </div>
  );
}