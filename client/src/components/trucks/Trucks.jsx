import { useState, useEffect } from "react";
import trucksData from '../../data/trucks.json';

export default function Trucks() {


     // Trucks
     const [selectedTruckItems, setSelectedTruckItems] = useState([]);
     const [isShowingAllTrucks, setIsShowingAllTrucks] = useState(false);
     const [truckFilter, setTruckFilter] = useState('All'); // 'All', 'Available', 'Unavailable'
     const [allTrucksSelected, setAllTrucksSelected] = useState(false); // Track if all items are selected
 
     useEffect(() => {
         // Initialize the state with truck data
         const initialTrucksData = trucksData.map(truck => ({
             id: truck.CarID,
             isChecked: truck.isAvailable,
             capacity: truck.capacity,
             currentLocation: truck.current_location,
             container: truck.container,
             isAvailable: truck.isAvailable
         }));
         setSelectedTruckItems(initialTrucksData);
     }, []);
 
     useEffect(() => {
         // Update the 'allTrucksSelected' state whenever 'selectedTruckItems' changes
         const selectedCount = selectedTruckItems.filter(item => item.isChecked).length;
         const availableCount = selectedTruckItems.filter(item => item.isAvailable).length;
         setAllTrucksSelected(selectedCount === availableCount && availableCount > 0);
     }, [selectedTruckItems]);
 
     const handleSelectAll = () => {
         const newSelectionState = !allTrucksSelected; // Toggle state
         setSelectedTruckItems(selectedTruckItems.map(item => ({
             ...item,
             isChecked: item.isAvailable && newSelectionState // Toggle based on availability
         })));
     };
 
     const handleCheckboxChange = (e, id) => {
         const checked = e.target.checked;
         setSelectedTruckItems(selectedTruckItems.map(item =>
             item.id === id ? { ...item, isChecked: checked } : item
         ));
     };
 
     const handleShowMore = () => {
         setIsShowingAllTrucks(true);
     };
 
     const handleHideMore = () => {
         setIsShowingAllTrucks(false);
     };
 
     const handleTruckFilterChange = (newFilter) => {
         setTruckFilter(newFilter);
         setIsShowingAllTrucks(false); // Hide additional items when truckFilter changes
     };
 
     const truckFilteredTruckItems = selectedTruckItems.filter(item => {
         if (truckFilter === 'Available') return item.isAvailable;
         if (truckFilter === 'Unavailable') return !item.isAvailable;
         return true;
     });
 
     const displayedItems = isShowingAllTrucks ? truckFilteredTruckItems : truckFilteredTruckItems.slice(0, 5);

    return (
        <section className="trucks mb-16">
            <h2>Trucks</h2>
            <div className="mb-16">
                <button
                    className={`btn btn-md mr-12 ${truckFilter === 'All' ? 'btn-1' : 'btn-2'}`}
                    onClick={() => handleTruckFilterChange('All')}
                >
                    All
                </button>
                <button
                    className={`btn btn-md mr-12 ${truckFilter === 'Available' ? 'btn-1' : 'btn-2'}`}
                    onClick={() => handleTruckFilterChange('Available')}
                >
                    Available
                </button>
                <button
                    className={`btn btn-md mr-12 ${truckFilter === 'Unavailable' ? 'btn-1' : 'btn-2'}`}
                    onClick={() => handleTruckFilterChange('Unavailable')}
                >
                    Unavailable
                </button>
            </div>

            <div className="table-container">
                <table className="custom-table">
                    <thead>
                        <tr>
                            <th>
                                <span
                                    className="select-all-text"
                                    onClick={handleSelectAll}
                                >
                                    {allTrucksSelected ? 'Deselect All' : 'Select All'}
                                </span>
                            </th>
                            <th>Status</th>
                            <th>Id</th>
                            <th>Capacity</th>
                            <th>Current Location</th>
                            <th>Container</th>
                        </tr>
                    </thead>
                    <tbody>
                        {displayedItems.map(item => (
                            <tr key={item.id}>
                                <td>
                                    <input
                                        type="checkbox"
                                        checked={item.isChecked}
                                        onChange={(e) => handleCheckboxChange(e, item.id)}
                                        disabled={!item.isAvailable}
                                    />
                                </td>
                                <td>
                                    <span className={`status ${item.isAvailable ? "available" : "unavailable"}`}>{item.isAvailable ? "Available" : "Unavailable"}</span>
                                </td>
                                <td>{`0${item.id}`}</td>
                                <td>{item.capacity}</td>
                                <td>{item.currentLocation}</td>
                                <td>{item.container ? "Loaded" : "Empty"}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {!isShowingAllTrucks && truckFilteredTruckItems.length > 5 && (
                    <div className="show-more flex-align-center flex-justify-center" onClick={handleShowMore} style={{ cursor: 'pointer' }}>
                        <strong className="select-all-text">Show {truckFilteredTruckItems.length - 5} more</strong>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={3} stroke="currentColor" className="size-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="m19.5 8.25-7.5 7.5-7.5-7.5" />
                        </svg>
                    </div>
                )}
                {isShowingAllTrucks && (
                    <div className="show-more flex-align-center flex-justify-center" onClick={handleHideMore} style={{ cursor: 'pointer' }}>
                        <strong>Hide {truckFilteredTruckItems.length - 5} more</strong>
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={3} stroke="currentColor" className="size-6">
                            <path strokeLinecap="round" strokeLinejoin="round" d="m4.5 15.75 7.5-7.5 7.5 7.5" />
                        </svg>
                    </div>
                )}
            </div>
        </section>
    )
}