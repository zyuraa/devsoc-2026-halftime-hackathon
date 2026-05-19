
import { useState, useRef, useEffect } from "react";

import Map, { Marker } from "react-map-gl/mapbox";
import type { MapRef } from "react-map-gl/mapbox";
import type { MapMouseEvent } from "react-map-gl/mapbox";

import "mapbox-gl/dist/mapbox-gl.css";

import { SearchBox } from "@mapbox/search-js-react";
import { useNavigate, useParams } from "react-router-dom";
import type { Gym } from "../types";

const MAPBOX_TOKEN: string = import.meta.env.VITE_API_KEY ?? "";

export default function GymSearcher() {

  const { id } = useParams();

  const [gyms, setGyms] = useState<Gym[]>([]);

  // map variables to pass to mapbox api
  const mapRef = useRef<MapRef>(null);
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
      setGyms(data);

      console.log("Server response:", data);

    } catch (error) {
      console.error("Error:", error);
    }
  }

  const navigate = useNavigate();

  const selectGym = (gymId: string) => {
    navigate(`/home/${id}/gym/${gymId}`);
  };

  return (
    <div className="w-200 min-h-screen flex flex-col items-center gap-4 p-4 bg-white rounded-2xl">
      <h2 className="text-center">
        Enter location to search for gyms!
      </h2>

      <div className="flex gap-8 items-center">
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
            Search for max {numGyms} gyms
          </p>
        </div>

        <div>
          <input type="range" 
            min='0' 
            max="50" 
            step='1' 
            value={radius}
            className='accent-blue-500' 
            id="myRange" 
            onChange={(e)=> {
              setRadius(Number(e.target.value))
            }}
            />
          <p>
            Within {radius}km
          </p>
        </div>

      </div>

      <div className="relative w-full h-[500px]">    
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
          onLoad={() => {
            mapRef.current?.resize();
          }}
          style={{
            width: "100%",
            height: "100%",
          }}
          onClick={clickMap}
        >

          <Marker
            latitude={marker.latitude}
            longitude={marker.longitude}
          />

        </Map>
      </div>
      
      <button 
        onClick={() =>
          requestGyms(
            marker.longitude,
            marker.latitude,
            radius,
            radius
          )
        }
        className="w-100 bg-blue-500 hover:bg-blue-700 text-white p-3 rounded-lg font-semibold transition"
      >
        Get Gyms
      </button>

      <div className="max-h-[400px] overflow-y-auto">
      <h2>Select a Gym</h2>

      {gyms.map((gym) => (
        <div
          key={gym.id}
          onClick={() => selectGym(gym.id)}
          style={{
            padding: "12px",
            margin: "8px 0",
            border: "1px solid #ccc",
            borderRadius: "8px",
            cursor: "pointer",
            backgroundColor: "#f9f9f9",
          }}
        >
          <h3>{gym.name}</h3>
            {/* {gym.groups !== undefined && (
              <p>{gym.groups.length} groups available</p>
            )} */}
          </div>
        ))}
      </div>
    </div>
  );
}