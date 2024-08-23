// Map.jsx
import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

// Styling
import "./ResourceDistributionMap.scss";

const center = [37.7749, -122.4194]; // Center of the map

const points = [
    [37.7749, -122.4194],
    [37.969, -121.4124],
    [37.6149, -122.4224],
    [37.6144, -121.4134],
    // Add more points as needed
];

const ResourceDistributionMap = () => {
    return (
        <section className="map mb-12">
            <h2>2D Map</h2>
            <div className="flex-align-center mb-12">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" className="size-6 mr-12">
                    <path strokeLinecap="round" strokeLinejoin="round" d="m11.25 11.25.041-.02a.75.75 0 0 1 1.063.852l-.708 2.836a.75.75 0 0 0 1.063.853l.041-.021M21 12a9 9 0 1 1-18 0 9 9 0 0 1 18 0Zm-9-3.75h.008v.008H12V8.25Z" />
                </svg>
                <span>Visualization of resource distribution</span>
            </div>
            <MapContainer center={center} zoom={10} style={{ height: '500px', width: '100%' }}>
                <TileLayer
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                {points.map((point, index) => (
                    <Marker key={index} position={point}>
                        <Popup>Point {index + 1}</Popup>
                    </Marker>
                ))}
            </MapContainer>
        </section>
    );
};

export default ResourceDistributionMap;